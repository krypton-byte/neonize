package utils

import (
	"fmt"

	"github.com/krypton-byte/neonize/neonize"
	"go.mau.fi/whatsmeow"
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
func DecodeGroupParent(groupParent *neonize.GroupParent) types.GroupParent {
	return types.GroupParent{
		IsParent:                      *groupParent.IsParent,
		DefaultMembershipApprovalMode: *groupParent.DefaultMembershipApprovalMode,
	}
}
func DecodeGroupLinkedParent(groupLinkedParent *neonize.GroupLinkedParent) types.GroupLinkedParent {
	return types.GroupLinkedParent{
		LinkedParentJID: DecodeJidProto(groupLinkedParent.LinkedParentJID),
	}
}
func DecodeReqCreateGroup(reqCreateGroup *neonize.ReqCreateGroup) whatsmeow.ReqCreateGroup {
	participants := []types.JID{}
	for _, participant := range reqCreateGroup.Participants {
		participants = append(participants, DecodeJidProto(participant))
	}
	new_type := whatsmeow.ReqCreateGroup{
		Name:         *reqCreateGroup.Name,
		Participants: participants,
		CreateKey:    *reqCreateGroup.CreateKey,
	}
	fmt.Println("gk tawu", reqCreateGroup.GroupParent)
	if reqCreateGroup.GroupParent != nil {
		new_type.GroupParent = DecodeGroupParent(reqCreateGroup.GroupParent)
	}
	if reqCreateGroup.GroupLinkedParent != nil {
		new_type.GroupLinkedParent = DecodeGroupLinkedParent(reqCreateGroup.GroupLinkedParent)
	}
	return new_type
}
