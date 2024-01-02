package utils

import (
	"C"

	"github.com/krypton-byte/neonize/neonize"
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/types"
	"google.golang.org/protobuf/proto"
)
import "fmt"

func EncodeUploadResponse(response whatsmeow.UploadResponse) neonize.UploadResponse {
	return neonize.UploadResponse{
		Url:           &response.URL,
		DirectPath:    &response.DirectPath,
		Handle:        &response.Handle,
		MediaKey:      response.MediaKey,
		FileEncSHA256: response.FileEncSHA256,
		FileSHA256:    response.FileSHA256,
		FileLength:    proto.Uint32(uint32(response.FileLength)),
	}
}
func EncodeJidProto(data types.JID) *neonize.JID {
	return &neonize.JID{
		User:       &data.User,
		RawAgent:   proto.Uint32(uint32(data.RawAgent)),
		Device:     proto.Uint32(uint32(data.Device)),
		Integrator: proto.Uint32(uint32(data.Integrator)),
		Server:     &data.Server,
	}
}
func EncodeGroupName(groupName types.GroupName) *neonize.GroupName {
	return &neonize.GroupName{
		Name:      &groupName.Name,
		NameSetAt: proto.Int64(groupName.NameSetAt.Unix()),
		NameSetBy: EncodeJidProto(groupName.NameSetBy),
	}
}
func EncodeGroupTopic(topic types.GroupTopic) *neonize.GroupTopic {
	return &neonize.GroupTopic{
		Topic:        &topic.Topic,
		TopicID:      &topic.TopicID,
		TopicSetAt:   proto.Int64(topic.TopicSetAt.Unix()),
		TopicSetBy:   EncodeJidProto(topic.TopicSetBy),
		TopicDeleted: &topic.TopicDeleted,
	}
}
func EncodeGroupLocked(locked types.GroupLocked) *neonize.GroupLocked {
	return &neonize.GroupLocked{
		IsLocked: &locked.IsLocked,
	}
}
func EncodeGroupAnnounce(announce types.GroupAnnounce) *neonize.GroupAnnounce {
	return &neonize.GroupAnnounce{
		IsAnnounce:        &announce.IsAnnounce,
		AnnounceVersionID: &announce.AnnounceVersionID,
	}
}
func EncodeGroupEphemeral(ephemeral types.GroupEphemeral) *neonize.GroupEphemeral {
	return &neonize.GroupEphemeral{
		IsEphemeral:       &ephemeral.IsEphemeral,
		DisappearingTimer: &ephemeral.DisappearingTimer,
	}
}
func EncodeGroupIncognito(incognito types.GroupIncognito) *neonize.GroupIncognito {
	return &neonize.GroupIncognito{
		IsIncognito: &incognito.IsIncognito,
	}
}
func EncodeGroupParent(parent types.GroupParent) *neonize.GroupParent {
	return &neonize.GroupParent{
		IsParent:                      &parent.IsParent,
		DefaultMembershipApprovalMode: &parent.DefaultMembershipApprovalMode,
	}
}
func EncodeGroupLinkedParent(linkedParent types.GroupLinkedParent) *neonize.GroupLinkedParent {
	return &neonize.GroupLinkedParent{
		LinkedParentJID: EncodeJidProto(linkedParent.LinkedParentJID),
	}
}
func EncodeGroupIsDefaultSub(isDefaultSub types.GroupIsDefaultSub) *neonize.GroupIsDefaultSub {
	return &neonize.GroupIsDefaultSub{
		IsDefaultSubGroup: &isDefaultSub.IsDefaultSubGroup,
	}
}
func EncodeGroupParticipantAddRequest(addRequest types.GroupParticipantAddRequest) *neonize.GroupParticipantAddRequest {
	return &neonize.GroupParticipantAddRequest{
		Code:       &addRequest.Code,
		Expiration: proto.Float32(float32(addRequest.Expiration.Unix())),
	}
}
func EncodeGroupParticipant(participant types.GroupParticipant) *neonize.GroupParticipant {
	fmt.Println("encodeparti", participant.JID)
	participant_group := neonize.GroupParticipant{
		LID:          EncodeJidProto(participant.LID),
		JID:          EncodeJidProto(participant.JID),
		IsAdmin:      &participant.IsAdmin,
		IsSuperAdmin: &participant.IsSuperAdmin,
		DisplayName:  &participant.DisplayName,
		Error:        proto.Int32(int32(participant.Error)),
	}
	fmt.Println("JIDSET ? ", participant_group.JID)
	if participant.AddRequest != nil {
		fmt.Println("NILLED")
		participant_group.AddRequest = EncodeGroupParticipantAddRequest(*participant.AddRequest)
	}
	fmt.Println("SETTED")
	// fmt.Println("encoded", participant_group)
	return &participant_group
}

func EncodeGroupInfo(info *types.GroupInfo) neonize.GroupInfo {
	fmt.Println("create list")
	participants := []*neonize.GroupParticipant{}
	fmt.Println("liast created")
	for _, participant := range info.Participants {
		fmt.Println(participant)
		participants = append(participants, EncodeGroupParticipant(participant))
	}
	fmt.Println("listedddd", info.JID)
	return neonize.GroupInfo{
		JID:                  EncodeJidProto(info.JID),
		OwnerJID:             EncodeJidProto(info.OwnerJID),
		GroupName:            EncodeGroupName(info.GroupName),
		GroupTopic:           EncodeGroupTopic(info.GroupTopic),
		GroupLocked:          EncodeGroupLocked(info.GroupLocked),
		GroupAnnounce:        EncodeGroupAnnounce(info.GroupAnnounce),
		GroupEphemeral:       EncodeGroupEphemeral(info.GroupEphemeral),
		GroupIncognito:       EncodeGroupIncognito(info.GroupIncognito),
		GroupParent:          EncodeGroupParent(info.GroupParent),
		GroupLinkedParent:    EncodeGroupLinkedParent(info.GroupLinkedParent),
		GroupIsDefaultSub:    EncodeGroupIsDefaultSub(info.GroupIsDefaultSub),
		GroupCreated:         proto.Float32(float32(info.GroupCreated.Unix())),
		ParticipantVersionID: &info.ParticipantVersionID,
		Participants:         participants,
	}
}
