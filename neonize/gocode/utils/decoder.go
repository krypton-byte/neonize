package utils

import (
	"time"

	defproto "github.com/krypton-byte/neonize/defproto"
	"github.com/krypton-byte/neonize/neonize"
	"go.mau.fi/whatsmeow"
	waProto "go.mau.fi/whatsmeow/binary/proto"
	"go.mau.fi/whatsmeow/types"
	"google.golang.org/protobuf/proto"
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
	if reqCreateGroup.GroupParent != nil {
		new_type.GroupParent = DecodeGroupParent(reqCreateGroup.GroupParent)
	}
	if reqCreateGroup.GroupLinkedParent != nil {
		new_type.GroupLinkedParent = DecodeGroupLinkedParent(reqCreateGroup.GroupLinkedParent)
	}
	return new_type
}
func DecodeMessageSource(messageSource *neonize.MessageSource) types.MessageSource {
	return types.MessageSource{
		Chat:               DecodeJidProto(messageSource.Chat),
		Sender:             DecodeJidProto(messageSource.Sender),
		IsFromMe:           *messageSource.IsFromMe,
		IsGroup:            *messageSource.IsGroup,
		BroadcastListOwner: DecodeJidProto(messageSource.BroadcastListOwner),
	}
}
func DecodeVerifiedNameCertificate(verifiedNameCertificate *defproto.VerifiedNameCertificate) *waProto.VerifiedNameCertificate {
	//passing types through protobuf
	var Certificate waProto.VerifiedNameCertificate
	encoded, err := proto.Marshal(verifiedNameCertificate)
	if err != nil {
		panic(err)
	}
	err_decode := proto.Unmarshal(encoded, &Certificate)
	if err_decode != nil {
		panic(err)
	}
	return &Certificate

}

func DecodeVerifiedNameDetails(verifiedNameDetails *defproto.VerifiedNameCertificate_Details) *waProto.VerifiedNameCertificate_Details {
	var details waProto.VerifiedNameCertificate_Details
	encoded, err := proto.Marshal(verifiedNameDetails)
	if err != nil {
		panic(err)
	}
	err_decode := proto.Unmarshal(encoded, &details)
	if err_decode != nil {
		panic(err_decode)
	}
	return &details
}
func DecodeVerifiedName(verifiedName *neonize.VerifiedName) *types.VerifiedName {
	verifiednametypes := types.VerifiedName{}
	if verifiedName.Certificate != nil {
		verifiednametypes.Certificate = DecodeVerifiedNameCertificate(verifiedName.Certificate)
	}
	if verifiedName.Details != nil {
		verifiednametypes.Details = DecodeVerifiedNameDetails(verifiedName.Details)
	}
	return &verifiednametypes
}
func DecodeDeviceSentMeta(deviceSentMeta *neonize.DeviceSentMeta) *types.DeviceSentMeta {
	return &types.DeviceSentMeta{
		DestinationJID: *deviceSentMeta.DestinationJID,
		Phash:          *deviceSentMeta.Phash,
	}
}
func DecodeMessageInfo(messageInfo *neonize.MessageInfo) *types.MessageInfo {
	ts := *messageInfo.Timestamp
	model := &types.MessageInfo{
		MessageSource: DecodeMessageSource(messageInfo.MessageSource),
		ID:            *messageInfo.ID,
		ServerID:      int(*messageInfo.ServerID),
		Type:          *messageInfo.Type,
		PushName:      *messageInfo.Pushname,
		Timestamp:     time.Unix(ts, 0),
		Category:      *messageInfo.Category,
		Multicast:     *messageInfo.Multicast,
		MediaType:     *messageInfo.MediaType,
		Edit:          types.EditAttribute(*messageInfo.Edit),
	}
	if messageInfo.VerifiedName != nil {
		model.VerifiedName = DecodeVerifiedName(messageInfo.VerifiedName)
	}
	if messageInfo.DeviceSentMeta != nil {
		model.DeviceSentMeta = DecodeDeviceSentMeta(messageInfo.DeviceSentMeta)
	}
	return model
}
