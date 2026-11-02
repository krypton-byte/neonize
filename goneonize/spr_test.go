package main

import (
	"os"
	"path/filepath"
	"testing"
	"time"

	"go.mau.fi/whatsmeow/proto/waE2E"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"
	"google.golang.org/protobuf/proto"
)

func TestSPRRetryReturnsTargetAndDecoyAcrossRestart(t *testing.T) {
	databasePath := filepath.Join(t.TempDir(), "session.db")
	store := newSPRRetryStore(databasePath)
	entry := sprRetryMessage{
		Group:         "120363000000000000@g.us",
		MessageID:     "message-1",
		Targets:       []string{"628123456789@s.whatsapp.net"},
		TargetMessage: "message A",
		DecoyMessage:  "message B",
	}
	if err := store.put(entry); err != nil {
		t.Fatal(err)
	}

	store = newSPRRetryStore(databasePath)
	group, _ := types.ParseJID(entry.Group)
	target, _ := types.ParseJID(entry.Targets[0])
	targetLID, _ := types.ParseJID("123456789012345@lid")
	other, _ := types.ParseJID("628987654321@s.whatsapp.net")
	if got := store.messageForRetry(target, group, types.MessageID(entry.MessageID)).GetConversation(); got != entry.TargetMessage {
		t.Fatalf("target retry = %q, want %q", got, entry.TargetMessage)
	}
	entry.Targets = append(entry.Targets, targetLID.String())
	if err := store.put(entry); err != nil {
		t.Fatal(err)
	}
	if got := store.messageForRetry(targetLID, group, types.MessageID(entry.MessageID)).GetConversation(); got != entry.TargetMessage {
		t.Fatalf("target LID retry = %q, want %q", got, entry.TargetMessage)
	}
	if got := store.messageForRetry(other, group, types.MessageID(entry.MessageID)).GetConversation(); got != entry.DecoyMessage {
		t.Fatalf("non-target retry = %q, want %q", got, entry.DecoyMessage)
	}

	stat, err := os.Stat(databasePath + ".spr.json")
	if err != nil {
		t.Fatal(err)
	}
	if stat.Mode().Perm() != 0o600 {
		t.Fatalf("retry store permissions = %o, want 600", stat.Mode().Perm())
	}
}

func TestSPRPreRetryPreservesSenderKeyAndMessageContext(t *testing.T) {
	group, _ := types.ParseJID("120363000000000000@g.us")
	target, _ := types.ParseJID("628123456789@s.whatsapp.net")
	other, _ := types.ParseJID("628987654321@s.whatsapp.net")
	targetLID, _ := types.ParseJID("123456789012345@lid")
	store := &sprRetryStore{messages: make(map[string]sprRetryMessage)}
	entry := sprRetryMessage{
		Group:         group.String(),
		MessageID:     "message-2",
		Targets:       []string{target.String()},
		TargetMessage: "message A",
		DecoyMessage:  "message B",
	}
	if err := store.put(entry); err != nil {
		t.Fatal(err)
	}

	senderKey := &waE2E.SenderKeyDistributionMessage{GroupID: proto.String(group.String())}
	messageContext := &waE2E.MessageContextInfo{MessageSecret: []byte("secret")}
	message := &waE2E.Message{
		Conversation:                 proto.String("message A"),
		SenderKeyDistributionMessage: senderKey,
		MessageContextInfo:           messageContext,
	}
	receipt := &events.Receipt{MessageSource: types.MessageSource{Chat: group, Sender: other, IsGroup: true}}
	if !store.beforeRetry(receipt, types.MessageID(entry.MessageID), 1, message) {
		t.Fatal("unexpectedly cancelled decoy retry")
	}
	if message.GetConversation() != entry.DecoyMessage {
		t.Fatalf("retry message = %q, want decoy %q", message.GetConversation(), entry.DecoyMessage)
	}
	if !proto.Equal(message.GetSenderKeyDistributionMessage(), senderKey) {
		t.Fatal("decoy retry lost the sender-key distribution message")
	}
	if !proto.Equal(message.GetMessageContextInfo(), messageContext) {
		t.Fatal("decoy retry lost message context")
	}

	targetMessage := &waE2E.Message{Conversation: proto.String("message B")}
	targetReceipt := &events.Receipt{MessageSource: types.MessageSource{
		Chat: group, Sender: targetLID, SenderAlt: target, IsGroup: true,
	}}
	if !store.beforeRetry(targetReceipt, types.MessageID(entry.MessageID), 1, targetMessage) {
		t.Fatal("unexpectedly cancelled target retry")
	}
	if targetMessage.GetConversation() != entry.TargetMessage {
		t.Fatalf("target retry changed to %q", targetMessage.GetConversation())
	}
}

func TestExpiredSPRRetryCancelsCachedOriginalAndLeavesTombstone(t *testing.T) {
	group, _ := types.ParseJID("120363000000000000@g.us")
	other, _ := types.ParseJID("628987654321@s.whatsapp.net")
	id := types.MessageID("message-expired")
	store := &sprRetryStore{messages: map[string]sprRetryMessage{
		sprRetryKey(group.String(), string(id)): {
			Targets:       []string{"628123456789@s.whatsapp.net"},
			TargetMessage: "message A",
			DecoyMessage:  "message B",
			ExpiresAt:     time.Now().Add(-time.Second),
		},
	}}

	entry, ok := store.get(group.String(), string(id))
	if !ok || !entry.Expired || entry.TargetMessage != "" || entry.DecoyMessage != "" {
		t.Fatalf("expired entry not reduced to tombstone: %+v, exists=%t", entry, ok)
	}
	if got := store.messageForRetry(other, group, id); got != nil {
		t.Fatalf("expired retry unexpectedly returned %q", got.GetConversation())
	}
	message := &waE2E.Message{Conversation: proto.String("cached original A")}
	receipt := &events.Receipt{MessageSource: types.MessageSource{Chat: group, Sender: other, IsGroup: true}}
	if store.beforeRetry(receipt, id, 1, message) {
		t.Fatal("expired cached original retry was not cancelled")
	}
}
