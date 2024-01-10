package utils

import (
	"C"

	defproto "github.com/krypton-byte/neonize/defproto"
	"github.com/krypton-byte/neonize/neonize"
	"go.mau.fi/whatsmeow"
	waBinary "go.mau.fi/whatsmeow/binary"
	waProto "go.mau.fi/whatsmeow/binary/proto"
	"go.mau.fi/whatsmeow/types"
	"google.golang.org/protobuf/proto"
)
import (
	"go.mau.fi/whatsmeow/types/events"
)

// Function
func EncodeUploadResponse(response whatsmeow.UploadResponse) *neonize.UploadResponse {
	return &neonize.UploadResponse{
		Url:           &response.URL,
		DirectPath:    &response.DirectPath,
		Handle:        &response.Handle,
		MediaKey:      response.MediaKey,
		FileEncSHA256: response.FileEncSHA256,
		FileSHA256:    response.FileSHA256,
		FileLength:    proto.Uint32(uint32(response.FileLength)),
	}
}

// types.go
func EncodeJidProto(data types.JID) *neonize.JID {
	isempty := data.IsEmpty()
	return &neonize.JID{
		User:       &data.User,
		RawAgent:   proto.Uint32(uint32(data.RawAgent)),
		Device:     proto.Uint32(uint32(data.Device)),
		Integrator: proto.Uint32(uint32(data.Integrator)),
		Server:     &data.Server,
		IsEmpty:    &isempty,
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
	participant_group := neonize.GroupParticipant{
		LID:          EncodeJidProto(participant.LID),
		JID:          EncodeJidProto(participant.JID),
		IsAdmin:      &participant.IsAdmin,
		IsSuperAdmin: &participant.IsSuperAdmin,
		DisplayName:  &participant.DisplayName,
		Error:        proto.Int32(int32(participant.Error)),
	}
	if participant.AddRequest != nil {
		participant_group.AddRequest = EncodeGroupParticipantAddRequest(*participant.AddRequest)
	}
	return &participant_group
}

// send.go
func EncodeGroupInfo(info *types.GroupInfo) *neonize.GroupInfo {
	participants := []*neonize.GroupParticipant{}
	for _, participant := range info.Participants {
		participants = append(participants, EncodeGroupParticipant(participant))
	}
	return &neonize.GroupInfo{
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

func EncodeMessageDebugTimings(debugTimings whatsmeow.MessageDebugTimings) *neonize.MessageDebugTimings {
	return &neonize.MessageDebugTimings{
		Queue:           proto.Int64(debugTimings.Queue.Nanoseconds()),
		Marshal_:        proto.Int64(debugTimings.Marshal.Nanoseconds()),
		GetParticipants: proto.Int64(debugTimings.GetParticipants.Nanoseconds()),
		GetDevices:      proto.Int64(debugTimings.GetParticipants.Nanoseconds()),
		GroupEncrypt:    proto.Int64(debugTimings.Queue.Nanoseconds()),
		PeerEncrypt:     proto.Int64(debugTimings.PeerEncrypt.Nanoseconds()),
		Send:            proto.Int64(debugTimings.Send.Nanoseconds()),
		Resp:            proto.Int64(debugTimings.Queue.Nanoseconds()),
		Retry:           proto.Int64(debugTimings.Retry.Nanoseconds()),
	}
}
func EncodeSendResponse(sendResponse whatsmeow.SendResponse) *neonize.SendResponse {
	return &neonize.SendResponse{
		Timestamp:    proto.Int64(sendResponse.Timestamp.Unix()),
		ID:           proto.String(sendResponse.ID),
		ServerID:     proto.Int64(int64(sendResponse.ServerID)),
		DebugTimings: EncodeMessageDebugTimings(sendResponse.DebugTimings),
	}
}
func EncodeVerifiedNameCertificate(verifiedNameCertificate *waProto.VerifiedNameCertificate) *defproto.VerifiedNameCertificate {
	return &defproto.VerifiedNameCertificate{
		Details:         verifiedNameCertificate.Details,
		Signature:       verifiedNameCertificate.Signature,
		ServerSignature: verifiedNameCertificate.ServerSignature,
	}
}
func EncodeLocalizedName(localizedname *waProto.LocalizedName) *defproto.LocalizedName {
	return &defproto.LocalizedName{
		Lg:           localizedname.Lg,
		Lc:           localizedname.Lc,
		VerifiedName: localizedname.VerifiedName,
	}
}
func EncodeVerifiedNameCertificate_Details(details *waProto.VerifiedNameCertificate_Details) *defproto.VerifiedNameCertificate_Details {
	localizedName := []*defproto.LocalizedName{}
	for _, localized := range details.LocalizedNames {
		localizedName = append(localizedName, EncodeLocalizedName(localized))
	}
	return &defproto.VerifiedNameCertificate_Details{
		Serial:         details.Serial,
		Issuer:         details.Issuer,
		VerifiedName:   details.VerifiedName,
		LocalizedNames: localizedName,
		IssueTime:      details.IssueTime,
	}
}
func EncodeVerifiedName(verifiedName *types.VerifiedName) *neonize.VerifiedName {
	models := &neonize.VerifiedName{}
	if verifiedName.Details != nil {
		models.Details = EncodeVerifiedNameCertificate_Details(verifiedName.Details)
	}
	if verifiedName.Certificate != nil {
		models.Certificate = EncodeVerifiedNameCertificate(verifiedName.Certificate)
	}
	return models
}
func EncodeIsOnWhatsApp(isOnWhatsApp types.IsOnWhatsAppResponse) *neonize.IsOnWhatsAppResponse {
	model := &neonize.IsOnWhatsAppResponse{
		Query: &isOnWhatsApp.Query,
		JID:   EncodeJidProto(isOnWhatsApp.JID),
		IsIn:  &isOnWhatsApp.IsIn,
	}
	if isOnWhatsApp.VerifiedName != nil {
		model.VerifiedName = EncodeVerifiedName(isOnWhatsApp.VerifiedName)
	}
	return model
}

func EncodeUserInfo(userInfo types.UserInfo) *neonize.UserInfo {
	devices := []*neonize.JID{}
	for _, jid := range userInfo.Devices {
		devices = append(devices, EncodeJidProto(jid))
	}
	models := &neonize.UserInfo{
		Status:    &userInfo.Status,
		PictureID: &userInfo.PictureID,
		Devices:   devices,
	}
	if userInfo.VerifiedName != nil {
		models.VerifiedName = EncodeVerifiedName(userInfo.VerifiedName)
	}
	return models
}
func EncodeMessageSource(messageSource types.MessageSource) *neonize.MessageSource {
	return &neonize.MessageSource{
		Chat:               EncodeJidProto(messageSource.Chat),
		Sender:             EncodeJidProto(messageSource.Sender),
		IsFromMe:           &messageSource.IsFromMe,
		IsGroup:            &messageSource.IsGroup,
		BroadcastListOwner: EncodeJidProto(messageSource.BroadcastListOwner),
	}
}
func EncodeDeviceSentMeta(deviceSentMeta *types.DeviceSentMeta) *neonize.DeviceSentMeta {
	return &neonize.DeviceSentMeta{
		DestinationJID: &deviceSentMeta.DestinationJID,
		Phash:          &deviceSentMeta.Phash,
	}
}
func EncodeMessageInfo(messageInfo types.MessageInfo) *neonize.MessageInfo {
	model := &neonize.MessageInfo{
		MessageSource: EncodeMessageSource(messageInfo.MessageSource),
		ID:            &messageInfo.ID,
		ServerID:      proto.Int64(messageInfo.Timestamp.Unix()),
		Type:          &messageInfo.Type,
		Pushname:      &messageInfo.PushName,
		Timestamp:     proto.Int64(messageInfo.Timestamp.Unix()),
		Category:      &messageInfo.Category,
		Multicast:     &messageInfo.Multicast,
		MediaType:     &messageInfo.MediaType,
		Edit:          (*string)(&messageInfo.Edit),
	}
	if messageInfo.VerifiedName != nil {
		model.VerifiedName = EncodeVerifiedName(messageInfo.VerifiedName)
	}
	if messageInfo.DeviceSentMeta != nil {
		model.DeviceSentMeta = EncodeDeviceSentMeta(messageInfo.DeviceSentMeta)
	}
	return model
}

func EncodeMessage(message *waProto.Message) *defproto.Message {
	var neonizeMessage defproto.Message
	encoded, err := proto.Marshal(message)
	if err != nil {
		panic(err)
	}
	err_decode := proto.Unmarshal(encoded, &neonizeMessage)
	if err_decode != nil {
		panic(err_decode)
	}
	return &neonizeMessage
}
func EncodeNewsLetterMessageMeta(newsLetter *events.NewsletterMessageMeta) *neonize.NewsLetterMessageMeta {
	return &neonize.NewsLetterMessageMeta{
		EditTS:     proto.Int64(int64(newsLetter.EditTS.Unix())),
		OriginalTS: proto.Int64(int64(newsLetter.OriginalTS.Unix())),
	}
}
func EncodeWebMessageInfo(sourceWebMsg *waProto.WebMessageInfo) *defproto.WebMessageInfo {
	var sourcewebmsg defproto.WebMessageInfo
	sourceWebBuf, err := proto.Marshal(sourceWebMsg)
	if err != nil {
		panic(err)
	}
	err_decoded := proto.Unmarshal(sourceWebBuf, &sourcewebmsg)
	if err_decoded != nil {
		panic(err)
	}
	return &sourcewebmsg

}

func EncodeEventTypesMessage(message *events.Message) *neonize.Message {
	model := &neonize.Message{
		Info:                 EncodeMessageInfo(message.Info),
		IsEphemeral:          &message.IsEphemeral,
		IsViewOnce:           &message.IsViewOnce,
		IsViewOnceV2:         &message.IsViewOnceV2,
		IsEdit:               &message.IsEdit,
		UnavailableRequestID: &message.UnavailableRequestID,
		RetryCount:           proto.Int64(int64(message.RetryCount)),
	}
	if message.NewsletterMeta != nil {
		model.NewsLetterMeta = EncodeNewsLetterMessageMeta(message.NewsletterMeta)
	}
	if message.SourceWebMsg != nil {
		model.SourceWebMsg = EncodeWebMessageInfo(message.SourceWebMsg)
	}
	if message.Message != nil {
		model.Message = EncodeMessage(message.Message)
	}
	return model
}
func EncodeNewsletterText(newsletterText types.NewsletterText) *neonize.NewsletterText {
	return &neonize.NewsletterText{
		Text:       &newsletterText.Text,
		ID:         &newsletterText.ID,
		UpdateTime: proto.Int64(newsletterText.UpdateTime.Unix()),
	}
}
func EncodeWrappedNewsletterState(state types.WrappedNewsletterState) *neonize.WrappedNewsletterState {
	var enum neonize.WrappedNewsletterState_NewsletterState
	switch state.Type {
	case types.NewsletterStateActive:
		enum = neonize.WrappedNewsletterState_ACTIVE
	case types.NewsletterStateSuspended:
		enum = neonize.WrappedNewsletterState_SUSPENDED
	case types.NewsletterStateGeoSuspended:
		enum = neonize.WrappedNewsletterState_GEOSUSPENDED
	}
	return &neonize.WrappedNewsletterState{
		Type: &enum,
	}
}
func EncodeProfilePictureInfo(profilePictureInfo types.ProfilePictureInfo) *neonize.ProfilePictureInfo {
	return &neonize.ProfilePictureInfo{
		URL:        &profilePictureInfo.URL,
		ID:         &profilePictureInfo.ID,
		Type:       &profilePictureInfo.Type,
		DirectPath: &profilePictureInfo.DirectPath,
	}
}
func EncodeNewsletterReactionSettings(reactionSettings types.NewsletterReactionSettings) *neonize.NewsletterReactionSettings {
	var reactionMode neonize.NewsletterReactionSettings_NewsletterReactionsMode
	switch reactionSettings.Value {
	case types.NewsletterReactionsModeAll:
		reactionMode = neonize.NewsletterReactionSettings_ALL
	case types.NewsletterReactionsModeBasic:
		reactionMode = neonize.NewsletterReactionSettings_BASIC
	case types.NewsletterReactionsModeNone:
		reactionMode = neonize.NewsletterReactionSettings_NONE
	case types.NewsletterReactionsModeBlocklist:
		reactionMode = neonize.NewsletterReactionSettings_BLOCKLIST
	}
	return &neonize.NewsletterReactionSettings{
		Value: &reactionMode,
	}
}
func EncodeNewsletterSetting(settings types.NewsletterSettings) *neonize.NewsletterSetting {
	return &neonize.NewsletterSetting{
		ReactionCodes: EncodeNewsletterReactionSettings(settings.ReactionCodes),
	}
}
func EncodeNewsletterThreadMetadata(threadMetadata types.NewsletterThreadMetadata) *neonize.NewsletterThreadMetadata {
	var state neonize.NewsletterThreadMetadata_NewsletterVerificationState
	switch threadMetadata.VerificationState {
	case types.NewsletterVerificationStateVerified:
		state = neonize.NewsletterThreadMetadata_VERIFIED
	case types.NewsletterVerificationStateUnverified:
		state = neonize.NewsletterThreadMetadata_UNVERIFIED
	}
	metadata := neonize.NewsletterThreadMetadata{
		CreationTime:      proto.Int64(threadMetadata.CreationTime.Unix()),
		InviteCode:        &threadMetadata.InviteCode,
		Name:              EncodeNewsletterText(threadMetadata.Name),
		Description:       EncodeNewsletterText(threadMetadata.Description),
		SubscriberCount:   proto.Int64(int64(threadMetadata.SubscriberCount)),
		VerificationState: &state,
		Preview:           EncodeProfilePictureInfo(threadMetadata.Preview),
		Settings:          EncodeNewsletterSetting(threadMetadata.Settings),
	}
	if threadMetadata.Picture != nil {
		metadata.Picture = EncodeProfilePictureInfo(*threadMetadata.Picture)
	}
	return &metadata
}
func EncodeNewsletterViewerMetadata(viewerMetadata *types.NewsletterViewerMetadata) *neonize.NewsletterViewerMetadata {
	var mute neonize.NewsletterMuteState
	var role neonize.NewsletterRole
	switch viewerMetadata.Mute {
	case types.NewsletterMuteOff:
		mute = neonize.NewsletterMuteState_OFF
	case types.NewsletterMuteOn:
		mute = neonize.NewsletterMuteState_ON
	}
	switch viewerMetadata.Role {
	case types.NewsletterRoleSubscriber:
		role = neonize.NewsletterRole_SUBSCRIBER
	case types.NewsletterRoleGuest:
		role = neonize.NewsletterRole_GUEST
	case types.NewsletterRoleAdmin:
		role = neonize.NewsletterRole_ADMIN
	case types.NewsletterRoleOwner:
		role = neonize.NewsletterRole_OWNER

	}
	return &neonize.NewsletterViewerMetadata{
		Mute: &mute,
		Role: &role,
	}
}
func EncodeNewsLetterMessageMetadata(metadata types.NewsletterMetadata) *neonize.NewsletterMetadata {
	model := &neonize.NewsletterMetadata{
		ID:         EncodeJidProto(metadata.ID),
		State:      EncodeWrappedNewsletterState(metadata.State),
		ThreadMeta: EncodeNewsletterThreadMetadata(metadata.ThreadMeta),
	}
	if metadata.ViewerMeta != nil {
		model.ViewerMeta = EncodeNewsletterViewerMetadata(metadata.ViewerMeta)
	}
	return model
}
func EncodeBlocklist(blocklist *types.Blocklist) *neonize.Blocklist {
	JIDs := []*neonize.JID{}
	for _, jid := range blocklist.JIDs {
		JIDs = append(JIDs, EncodeJidProto(jid))
	}
	return &neonize.Blocklist{
		DHash: &blocklist.DHash,
		JIDs:  JIDs,
	}
}
func EncodeNewsletterMessage(message *types.NewsletterMessage) *neonize.NewsletterMessage {
	var defmessage defproto.Message
	message_buf, err := proto.Marshal(message.Message)
	if err != nil {
		panic(err)
	}
	err_unmarshal := proto.Unmarshal(message_buf, &defmessage)
	if err_unmarshal != nil {
		panic(err)
	}
	reacts := []*neonize.Reaction{}
	for react, count := range message.ReactionCounts {
		reacts = append(reacts, &neonize.Reaction{
			Type:  proto.String(react),
			Count: proto.Int64(int64(count)),
		})
	}
	return &neonize.NewsletterMessage{
		MessageServerID: proto.Int64(int64(message.MessageServerID)),
		ViewsCount:      proto.Int64(int64(message.ViewsCount)),
		Message:         &defmessage,
		ReactionCounts:  reacts,
	}
}

func EncodePrivacySetting(privacy types.PrivacySetting) *neonize.PrivacySettings_PrivacySetting {
	var privacySetting neonize.PrivacySettings_PrivacySetting
	switch privacy {
	case types.PrivacySettingUndefined:
		privacySetting = neonize.PrivacySettings_UNDEFINED
	case types.PrivacySettingAll:
		privacySetting = neonize.PrivacySettings_ALL
	case types.PrivacySettingContacts:
		privacySetting = neonize.PrivacySettings_CONTACTS
	case types.PrivacySettingContactBlacklist:
		privacySetting = neonize.PrivacySettings_CONTACT_BLACKLIST
	case types.PrivacySettingMatchLastSeen:
		privacySetting = neonize.PrivacySettings_MATCH_LAST_SEEN
	case types.PrivacySettingKnown:
		privacySetting = neonize.PrivacySettings_KNOWN
	case types.PrivacySettingNone:
		privacySetting = neonize.PrivacySettings_NONE
	}
	return &privacySetting
}

func EncodePrivacySettings(privacySetting types.PrivacySettings) *neonize.PrivacySettings {
	return &neonize.PrivacySettings{
		GroupAdd:     EncodePrivacySetting(privacySetting.GroupAdd),
		LastSeen:     EncodePrivacySetting(privacySetting.LastSeen),
		Status:       EncodePrivacySetting(privacySetting.Status),
		Profile:      EncodePrivacySetting(privacySetting.Profile),
		ReadReceipts: EncodePrivacySetting(privacySetting.ReadReceipts),
		CallAdd:      EncodePrivacySetting(privacySetting.CallAdd),
		Online:       EncodePrivacySetting(privacySetting.Online),
	}
}

func EncodeStatusPrivacy(statusPrivacy types.StatusPrivacy) *neonize.StatusPrivacy {
	var ptype neonize.StatusPrivacy_StatusPrivacyType
	JIDS := []*neonize.JID{}
	switch statusPrivacy.Type {
	case types.StatusPrivacyTypeBlacklist:
		ptype = neonize.StatusPrivacy_BLACKLIST
	case types.StatusPrivacyTypeContacts:
		ptype = neonize.StatusPrivacy_CONTACTS
	case types.StatusPrivacyTypeWhitelist:
		ptype = neonize.StatusPrivacy_WHITELIST
	}
	for _, jid := range statusPrivacy.List {
		JIDS = append(JIDS, EncodeJidProto(jid))
	}
	return &neonize.StatusPrivacy{
		Type:      &ptype,
		List:      JIDS,
		IsDefault: &statusPrivacy.IsDefault,
	}
}

func EncodeGroupLinkTarget(group types.GroupLinkTarget) *neonize.GroupLinkTarget {
	return &neonize.GroupLinkTarget{
		JID:               EncodeJidProto(group.JID),
		GroupName:         EncodeGroupName(group.GroupName),
		GroupIsDefaultSub: EncodeGroupIsDefaultSub(group.GroupIsDefaultSub),
	}
}

func EncodeContactQRLinkTarget(contact types.ContactQRLinkTarget) *neonize.ContactQRLinkTarget {
	return &neonize.ContactQRLinkTarget{
		JID:      EncodeJidProto(contact.JID),
		Type:     &contact.Type,
		PushName: &contact.PushName,
	}
}

func EncodeBusinessMessageLinkTarget(message types.BusinessMessageLinkTarget) *neonize.BusinessMessageLinkTarget {
	return &neonize.BusinessMessageLinkTarget{
		JID:           EncodeJidProto(message.JID),
		PushName:      proto.String(message.PushName),
		VerifiedName:  proto.String(message.VerifiedName),
		IsSigned:      &message.IsSigned,
		VerifiedLevel: &message.VerifiedLevel,
		Message:       &message.Message,
	}
}

func EncodePairSuccess(pair *events.PairSuccess) *neonize.PairStatus {
	return &neonize.PairStatus{
		ID:           EncodeJidProto(pair.ID),
		BusinessName: &pair.BusinessName,
		Platform:     &pair.Platform,
		Status:       neonize.PairStatus_SUCCESS.Enum(),
	}
}

func EncodePairError(pair *events.PairError) *neonize.PairStatus {
	return &neonize.PairStatus{
		ID:           EncodeJidProto(pair.ID),
		BusinessName: &pair.BusinessName,
		Platform:     &pair.Platform,
		Status:       neonize.PairStatus_ERROR.Enum(),
		Error:        proto.String(pair.Error.Error()),
	}
}
func EncodeConnectFailureReason(reason_types events.ConnectFailureReason) *neonize.ConnectFailureReason {
	var reason *neonize.ConnectFailureReason
	switch reason_types {
	case events.ConnectFailureGeneric:
		reason = neonize.ConnectFailureReason_GENERIC.Enum()
	case events.ConnectFailureLoggedOut:
		reason = neonize.ConnectFailureReason_LOGGED_OUT.Enum()
	case events.ConnectFailureTempBanned:
		reason = neonize.ConnectFailureReason_TEMP_BANNED.Enum()
	case events.ConnectFailureMainDeviceGone:
		reason = neonize.ConnectFailureReason_MAIN_DEVICE_GONE.Enum()
	case events.ConnectFailureUnknownLogout:
		reason = neonize.ConnectFailureReason_UNKNOWN_LOGOUT.Enum()
	case events.ConnectFailureClientOutdated:
		reason = neonize.ConnectFailureReason_CLIENT_OUTDATED.Enum()
	case events.ConnectFailureBadUserAgent:
		reason = neonize.ConnectFailureReason_BAD_USER_AGENT.Enum()
	case events.ConnectFailureInternalServerError:
		reason = neonize.ConnectFailureReason_INTERNAL_SERVER_ERROR.Enum()
	case events.ConnectFailureExperimental:
		reason = neonize.ConnectFailureReason_EXPERIMENTAL.Enum()
	case events.ConnectFailureServiceUnavailable:
		reason = neonize.ConnectFailureReason_SERVICE_UNAVAILABLE.Enum()
	}
	return reason
}
func EncodeLoggedOut(logout *events.LoggedOut) *neonize.LoggedOut {
	return &neonize.LoggedOut{
		OnConnect: &logout.OnConnect,
		Reason:    EncodeConnectFailureReason(logout.Reason),
	}
}

func EncodeTemporaryBan(ban *events.TemporaryBan) *neonize.TemporaryBan {
	var reason *neonize.TemporaryBan_TempBanReason
	switch ban.Code {
	case events.TempBanSentToTooManyPeople:
		reason = neonize.TemporaryBan_SEND_TO_TOO_MANY_PEOPLE.Enum()
	case events.TempBanBlockedByUsers:
		reason = neonize.TemporaryBan_BLOCKED_BY_USERS.Enum()
	case events.TempBanCreatedTooManyGroups:
		reason = neonize.TemporaryBan_CREATED_TOO_MANY_GROUPS.Enum()
	case events.TempBanSentTooManySameMessage:
		reason = neonize.TemporaryBan_SENT_TOO_MANY_SAME_MESSAGE.Enum()
	case events.TempBanBroadcastList:
		reason = neonize.TemporaryBan_BROADCAST_LIST.Enum()
	}
	return &neonize.TemporaryBan{
		Code:   reason,
		Expire: proto.Int64(int64(ban.Expire.Seconds())),
	}
}
func EncodeNodeAttrs(attrs waBinary.Attrs) []*neonize.NodeAttrs {
	n_attr := []*neonize.NodeAttrs{}
	for k, v := range attrs {
		attr := neonize.NodeAttrs{Name: proto.String(k)}
		switch value := v.(type) {
		case *int:
			attr.Value = &neonize.NodeAttrs_Integer{Integer: *proto.Int64(int64(*value))}
		case *int32:
			attr.Value = &neonize.NodeAttrs_Integer{Integer: *proto.Int64(int64(*value))}
		case *int64:
			attr.Value = &neonize.NodeAttrs_Integer{Integer: *proto.Int64(int64(*value))}
		case *bool:
			attr.Value = &neonize.NodeAttrs_Boolean{Boolean: *value}
		case *string:
			attr.Value = &neonize.NodeAttrs_Text{Text: *value}
		}
		n_attr = append(n_attr, &attr)
	}
	return n_attr
}
func EncodeNode(node *waBinary.Node) *neonize.Node {
	nodes := neonize.Node{
		Tag:   &node.Tag,
		Attrs: EncodeNodeAttrs(node.Attrs),
	}
	switch v := node.Content.(type) {
	case nil:
		nodes.Nil = proto.Bool(true)
	case []waBinary.Node:
		var content = make([]*neonize.Node, len(v))
		for i, c_node := range v {
			content[i] = EncodeNode(&c_node)
		}
		nodes.Nodes = content
	case []byte:
		nodes.Bytes = v
	}
	return &nodes

}
func EncodeConnectFailure(connect *events.ConnectFailure) *neonize.ConnectFailure {
	return &neonize.ConnectFailure{
		Reason:  EncodeConnectFailureReason(connect.Reason),
		Message: &connect.Message,
		Raw:     EncodeNode(connect.Raw),
	}
}
