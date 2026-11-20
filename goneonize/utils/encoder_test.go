package utils

import (
	"testing"
	"time"

	"go.mau.fi/whatsmeow/types"
)

func TestEncodeGroupParticipantAddRequestKeepsExactExpiration(t *testing.T) {
	const expiration int64 = 1793977234

	encoded := EncodeGroupParticipantAddRequest(types.GroupParticipantAddRequest{
		Code:       "invite-code",
		Expiration: time.Unix(expiration, 0),
	})

	if got := int64(encoded.GetExpiration()); got != expiration {
		t.Fatalf("want %d, got %d", expiration, got)
	}
	if got := encoded.GetCode(); got != "invite-code" {
		t.Fatalf("want code %q, got %q", "invite-code", got)
	}
}

func TestEncodeBlocklist(t *testing.T) {
	lid := types.NewJID("12345", types.HiddenUserServer)
	pn := types.NewJID("628123456789", types.DefaultUserServer)

	encoded := EncodeBlocklist(&types.Blocklist{
		DHash: "dhash-1",
		Items: []types.BlocklistItem{
			{LID: lid, Active: true},
			{PN: pn, Active: true},
		},
	})

	if got := encoded.GetDHash(); got != "dhash-1" {
		t.Fatalf("want dhash %q, got %q", "dhash-1", got)
	}
	if len(encoded.JIDs) != 2 {
		t.Fatalf("want 2 JIDs, got %d", len(encoded.JIDs))
	}
	if got := encoded.JIDs[0].GetUser(); got != "12345" {
		t.Fatalf("want first JID user %q, got %q", "12345", got)
	}
	if got := encoded.JIDs[1].GetUser(); got != "628123456789" {
		t.Fatalf("want second JID user %q, got %q", "628123456789", got)
	}
}
