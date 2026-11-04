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
