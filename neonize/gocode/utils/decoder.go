package utils

import (
	"github.com/krypton-byte/neonize/neonize"
	"go.mau.fi/whatsmeow/types"
)

func DecodeJidProto(data *neonize.JID) types.JID {
	return types.JID{
		User:       *data.User,
		RawAgent:   uint8(*data.RawAgent),
		Device:     uint16(*data.Device),
		Integrator: uint16(*data.Integrator),
		Server:     *data.Server,
	}
}
