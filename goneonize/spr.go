package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/proto/waE2E"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"
	"google.golang.org/protobuf/proto"
)

const sprRetryRetention = 72 * time.Hour

var sprRetryStores sync.Map

func installSPRRetryHooks(client *whatsmeow.Client, store *sprRetryStore) {
	client.GetMessageForRetry = store.messageForRetry
	client.PreRetryCallback = store.beforeRetry
}

type sprRetryMessage struct {
	Group         string    `json:"-"`
	MessageID     string    `json:"-"`
	Targets       []string  `json:"targets"`
	TargetMessage string    `json:"target_message"`
	DecoyMessage  string    `json:"decoy_message"`
	ExpiresAt     time.Time `json:"expires_at"`
	Expired       bool      `json:"expired,omitempty"`
}

type sprRetryStore struct {
	mu       sync.Mutex
	path     string
	messages map[string]sprRetryMessage
	loadErr  error
}

func sprRetryKey(group, id string) string {
	digest := sha256.Sum256([]byte(group + "\x00" + id))
	return hex.EncodeToString(digest[:])
}

func newSPRRetryStore(databaseName string) *sprRetryStore {
	db := strings.TrimSpace(databaseName)
	path := db + ".spr.json"
	switch {
	case db == "" || db == ":memory:" || strings.HasPrefix(db, "file::memory:"):
		path = ""
	case strings.HasPrefix(db, "postgres://") || strings.HasPrefix(db, "postgresql://"):
		digest := sha256.Sum256([]byte(db))
		path = filepath.Join("storage", "neonize-spr-"+hex.EncodeToString(digest[:8])+".json")
	}
	store := &sprRetryStore{path: path, messages: make(map[string]sprRetryMessage)}
	if path == "" {
		return store
	}
	data, err := os.ReadFile(path)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		store.loadErr = err
		return store
	}
	if len(data) > 0 {
		if err := json.Unmarshal(data, &store.messages); err != nil {
			store.loadErr = fmt.Errorf("invalid SPR retry store %s: %w", path, err)
		}
	}
	if store.pruneLocked(time.Now()) {
		_ = store.persistLocked()
	}
	return store
}

func (s *sprRetryStore) persistLocked() error {
	if s.loadErr != nil {
		return s.loadErr
	}
	if s.path == "" {
		return nil
	}
	if err := os.MkdirAll(filepath.Dir(s.path), 0700); err != nil {
		return err
	}
	data, err := json.Marshal(s.messages)
	if err != nil {
		return err
	}
	tmp := s.path + ".tmp"
	if err = os.WriteFile(tmp, data, 0600); err != nil {
		return err
	}
	if err = os.Chmod(tmp, 0600); err != nil {
		_ = os.Remove(tmp)
		return err
	}
	if err = os.Rename(tmp, s.path); err != nil {
		_ = os.Remove(tmp)
		return err
	}
	return nil
}

func (s *sprRetryStore) pruneLocked(now time.Time) bool {
	changed := false
	for key, message := range s.messages {
		if message.Expired {
			continue
		}
		if !message.ExpiresAt.After(now) {
			// Keep a minimal tombstone permanently. A cached original message can
			// still reach PreRetryCallback after the payload mapping expires; the
			// tombstone makes that callback cancel instead of replaying message A.
			message.Targets = nil
			message.TargetMessage = ""
			message.DecoyMessage = ""
			message.ExpiresAt = time.Time{}
			message.Expired = true
			s.messages[key] = message
			changed = true
		}
	}
	return changed
}

func (s *sprRetryStore) put(message sprRetryMessage) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.loadErr != nil {
		return s.loadErr
	}
	s.pruneLocked(time.Now())
	message.ExpiresAt = time.Now().Add(sprRetryRetention)
	s.messages[sprRetryKey(message.Group, message.MessageID)] = message
	return s.persistLocked()
}

func (s *sprRetryStore) get(group, id string) (sprRetryMessage, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.loadErr != nil {
		return sprRetryMessage{}, false
	}
	if s.pruneLocked(time.Now()) {
		_ = s.persistLocked()
	}
	message, ok := s.messages[sprRetryKey(group, id)]
	return message, ok
}

func sprMessage(text string) *waE2E.Message {
	return &waE2E.Message{Conversation: proto.String(text)}
}

func (s *sprRetryStore) messageForRetry(requester, group types.JID, id types.MessageID) *waE2E.Message {
	entry, ok := s.get(group.String(), string(id))
	if !ok || entry.Expired {
		return nil
	}
	if sprIsTarget(entry.Targets, requester) {
		return sprMessage(entry.TargetMessage)
	}
	return sprMessage(entry.DecoyMessage)
}

func (s *sprRetryStore) beforeRetry(receipt *events.Receipt, id types.MessageID, _ int, message *waE2E.Message) bool {
	if receipt == nil || message == nil || !receipt.IsGroup {
		return true
	}
	entry, ok := s.get(receipt.Chat.String(), string(id))
	if ok && entry.Expired {
		return false
	}
	if !ok {
		return true
	}
	senderKey := message.SenderKeyDistributionMessage
	messageContext := message.MessageContextInfo
	if sprIsTarget(entry.Targets, receipt.Sender, receipt.SenderAlt) {
		*message = *sprMessage(entry.TargetMessage)
	} else {
		*message = *sprMessage(entry.DecoyMessage)
	}
	message.SenderKeyDistributionMessage = senderKey
	message.MessageContextInfo = messageContext
	return true
}

func sprIsTarget(targets []string, requesters ...types.JID) bool {
	for _, requester := range requesters {
		if requester.IsEmpty() {
			continue
		}
		requesterJID := requester.ToNonAD().String()
		for _, target := range targets {
			if target == requesterJID {
				return true
			}
		}
	}
	return false
}
