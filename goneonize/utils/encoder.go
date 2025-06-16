package utils

import (
	"C"

	// defproto "github.com/krypton-byte/neonize/defproto"
	defproto "github.com/krypton-byte/neonize/defproto"
	"go.mau.fi/whatsmeow"
	waBinary "go.mau.fi/whatsmeow/binary"
	"go.mau.fi/whatsmeow/types"
	"google.golang.org/protobuf/proto"
)
import (
	"go.mau.fi/whatsmeow/types/events"
)

// Function
func EncodeUploadResponse(response whatsmeow.UploadResponse) *defproto.UploadResponse {
	return &defproto.UploadResponse{
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
func EncodeJidProto(data types.JID) *defproto.JID {
	isempty := data.IsEmpty()
	return &defproto.JID{
		User:       &data.User,
		RawAgent:   proto.Uint32(uint32(data.RawAgent)),
		Device:     proto.Uint32(uint32(data.Device)),
		Integrator: proto.Uint32(uint32(data.Integrator)),
		Server:     &data.Server,
		IsEmpty:    &isempty,
	}
}
func EncodeGroupName(groupName types.GroupName) *defproto.GroupName {
	return &defproto.GroupName{
		Name:      &groupName.Name,
		NameSetAt: proto.Int64(groupName.NameSetAt.Unix()),
		NameSetBy: EncodeJidProto(groupName.NameSetBy),
	}
}
func EncodeGroupTopic(topic types.GroupTopic) *defproto.GroupTopic {
	return &defproto.GroupTopic{
		Topic:        &topic.Topic,
		TopicID:      &topic.TopicID,
		TopicSetAt:   proto.Int64(topic.TopicSetAt.Unix()),
		TopicSetBy:   EncodeJidProto(topic.TopicSetBy),
		TopicDeleted: &topic.TopicDeleted,
	}
}
func EncodeGroupLocked(locked types.GroupLocked) *defproto.GroupLocked {
	return &defproto.GroupLocked{
		IsLocked: &locked.IsLocked,
	}
}
func EncodeGroupAnnounce(announce types.GroupAnnounce) *defproto.GroupAnnounce {
	return &defproto.GroupAnnounce{
		IsAnnounce:        &announce.IsAnnounce,
		AnnounceVersionID: &announce.AnnounceVersionID,
	}
}
func EncodeGroupEphemeral(ephemeral types.GroupEphemeral) *defproto.GroupEphemeral {
	return &defproto.GroupEphemeral{
		IsEphemeral:       &ephemeral.IsEphemeral,
		DisappearingTimer: &ephemeral.DisappearingTimer,
	}
}
func EncodeGroupIncognito(incognito types.GroupIncognito) *defproto.GroupIncognito {
	return &defproto.GroupIncognito{
		IsIncognito: &incognito.IsIncognito,
	}
}
func EncodeGroupParent(parent types.GroupParent) *defproto.GroupParent {
	return &defproto.GroupParent{
		IsParent:                      &parent.IsParent,
		DefaultMembershipApprovalMode: &parent.DefaultMembershipApprovalMode,
	}
}
func EncodeGroupLinkedParent(linkedParent types.GroupLinkedParent) *defproto.GroupLinkedParent {
	return &defproto.GroupLinkedParent{
		LinkedParentJID: EncodeJidProto(linkedParent.LinkedParentJID),
	}
}
func EncodeGroupIsDefaultSub(isDefaultSub types.GroupIsDefaultSub) *defproto.GroupIsDefaultSub {
	return &defproto.GroupIsDefaultSub{
		IsDefaultSubGroup: &isDefaultSub.IsDefaultSubGroup,
	}
}
func EncodeGroupParticipantAddRequest(addRequest types.GroupParticipantAddRequest) *defproto.GroupParticipantAddRequest {
	return &defproto.GroupParticipantAddRequest{
		Code:       &addRequest.Code,
		Expiration: proto.Float32(float32(addRequest.Expiration.Unix())),
	}
}
func EncodeGroupParticipant(participant types.GroupParticipant) *defproto.GroupParticipant {
	participant_group := defproto.GroupParticipant{
		LID:          EncodeJidProto(participant.LID),
		JID:          EncodeJidProto(participant.JID),
		PhoneNumber:  EncodeJidProto(participant.PhoneNumber),
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
func EncodeGroupInfo(info *types.GroupInfo) *defproto.GroupInfo {
	participants := []*defproto.GroupParticipant{}
	for _, participant := range info.Participants {
		participants = append(participants, EncodeGroupParticipant(participant))
	}
	return &defproto.GroupInfo{
		JID:                  EncodeJidProto(info.JID),
		OwnerJID:             EncodeJidProto(info.OwnerJID),
		OwnerPN:              EncodeJidProto(info.OwnerPN),
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

func EncodeMessageDebugTimings(debugTimings whatsmeow.MessageDebugTimings) *defproto.MessageDebugTimings {
	return &defproto.MessageDebugTimings{
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
func EncodeSendResponse(sendResponse whatsmeow.SendResponse) *defproto.SendResponse {
	return &defproto.SendResponse{
		Timestamp:    proto.Int64(sendResponse.Timestamp.Unix()),
		ID:           proto.String(sendResponse.ID),
		ServerID:     proto.Int64(int64(sendResponse.ServerID)),
		DebugTimings: EncodeMessageDebugTimings(sendResponse.DebugTimings),
	}
}

func EncodeVerifiedName(verifiedName *types.VerifiedName) *defproto.VerifiedName {
	models := &defproto.VerifiedName{}
	if verifiedName.Details != nil {
		models.Details = verifiedName.Details
	}
	if verifiedName.Certificate != nil {
		models.Certificate = verifiedName.Certificate
	}
	return models
}
func EncodeIsOnWhatsApp(isOnWhatsApp types.IsOnWhatsAppResponse) *defproto.IsOnWhatsAppResponse {
	model := &defproto.IsOnWhatsAppResponse{
		Query: &isOnWhatsApp.Query,
		JID:   EncodeJidProto(isOnWhatsApp.JID),
		IsIn:  &isOnWhatsApp.IsIn,
	}
	if isOnWhatsApp.VerifiedName != nil {
		model.VerifiedName = EncodeVerifiedName(isOnWhatsApp.VerifiedName)
	}
	return model
}

func EncodeUserInfo(userInfo types.UserInfo) *defproto.UserInfo {
	devices := []*defproto.JID{}
	for _, jid := range userInfo.Devices {
		devices = append(devices, EncodeJidProto(jid))
	}
	models := &defproto.UserInfo{
		Status:    &userInfo.Status,
		PictureID: &userInfo.PictureID,
		Devices:   devices,
	}
	if userInfo.VerifiedName != nil {
		models.VerifiedName = EncodeVerifiedName(userInfo.VerifiedName)
	}
	return models
}

func EncodeAddressingMode(mode_types types.AddressingMode) *defproto.AddressingMode {
	var AddressingMode *defproto.AddressingMode
	switch mode_types {
	case types.AddressingModePN:
		AddressingMode = defproto.AddressingMode_PN.Enum()
	case types.AddressingModeLID:
		AddressingMode = defproto.AddressingMode_LID.Enum()
	}
	return AddressingMode
}
func EncodeMessageSource(messageSource types.MessageSource) *defproto.MessageSource {
	return &defproto.MessageSource{
		Chat:               EncodeJidProto(messageSource.Chat),
		Sender:             EncodeJidProto(messageSource.Sender),
		IsFromMe:           &messageSource.IsFromMe,
		IsGroup:            &messageSource.IsGroup,

		AddressingMode:     EncodeAddressingMode(messageSource.AddressingMode),
		SenderAlt:          EncodeJidProto(messageSource.SenderAlt),
		RecipientAlt:       EncodeJidProto(messageSource.RecipientAlt),

		BroadcastListOwner: EncodeJidProto(messageSource.BroadcastListOwner),
	}
}
func EncodeDeviceSentMeta(deviceSentMeta *types.DeviceSentMeta) *defproto.DeviceSentMeta {
	return &defproto.DeviceSentMeta{
		DestinationJID: &deviceSentMeta.DestinationJID,
		Phash:          &deviceSentMeta.Phash,
	}
}
func EncodeMessageInfo(messageInfo types.MessageInfo) *defproto.MessageInfo {
	model := &defproto.MessageInfo{
		MessageSource: EncodeMessageSource(messageInfo.MessageSource),
		ID:            &messageInfo.ID,
		ServerID:      proto.Int64(int64(messageInfo.ServerID)),
		Type:          &messageInfo.Type,
		Pushname:      &messageInfo.PushName,
		Timestamp:     proto.Int64(messageInfo.Timestamp.UnixMilli()),
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

//	func EncodeMessage(message *waProto.Message) *defproto.Message {
//		var neonizeMessage defproto.Message
//		encoded, err := proto.Marshal(message)
//		if err != nil {
//			panic(err)
//		}
//		err_decode := proto.Unmarshal(encoded, &neonizeMessage)
//		if err_decode != nil {
//			panic(err_decode)
//		}
//		return &neonizeMessage
//	}
func EncodeNewsLetterMessageMeta(newsLetter *events.NewsletterMessageMeta) *defproto.NewsLetterMessageMeta {
	return &defproto.NewsLetterMessageMeta{
		EditTS:     proto.Int64(int64(newsLetter.EditTS.Unix())),
		OriginalTS: proto.Int64(int64(newsLetter.OriginalTS.Unix())),
	}
}

func EncodeEventTypesMessage(message *events.Message) *defproto.Message {
	model := &defproto.Message{
		Info:                  EncodeMessageInfo(message.Info),
		IsEphemeral:           &message.IsEphemeral,
		IsViewOnce:            &message.IsViewOnce,
		IsViewOnceV2:          &message.IsViewOnceV2,
		IsEdit:                &message.IsEdit,
		IsViewOnceV2Extension: proto.Bool(message.IsViewOnceV2Extension),
		IsDocumentWithCaption: proto.Bool(message.IsDocumentWithCaption),
		IsLottieSticker:       proto.Bool(message.IsLottieSticker),
		UnavailableRequestID:  &message.UnavailableRequestID,
		RetryCount:            proto.Int64(int64(message.RetryCount)),
		Raw:                   message.Message,
	}
	if message.NewsletterMeta != nil {
		model.NewsLetterMeta = EncodeNewsLetterMessageMeta(message.NewsletterMeta)
	}
	if message.SourceWebMsg != nil {
		model.SourceWebMsg = message.SourceWebMsg
	}
	if message.Message != nil {
		model.Message = message.Message
	}
	return model
}
func EncodeNewsletterText(newsletterText types.NewsletterText) *defproto.NewsletterText {
	return &defproto.NewsletterText{
		Text:       &newsletterText.Text,
		ID:         &newsletterText.ID,
		UpdateTime: proto.Int64(newsletterText.UpdateTime.Unix()),
	}
}
func EncodeWrappedNewsletterState(state types.WrappedNewsletterState) *defproto.WrappedNewsletterState {
	var enum defproto.WrappedNewsletterState_NewsletterState
	switch state.Type {
	case types.NewsletterStateActive:
		enum = defproto.WrappedNewsletterState_ACTIVE
	case types.NewsletterStateSuspended:
		enum = defproto.WrappedNewsletterState_SUSPENDED
	case types.NewsletterStateGeoSuspended:
		enum = defproto.WrappedNewsletterState_GEOSUSPENDED
	}
	return &defproto.WrappedNewsletterState{
		Type: &enum,
	}
}
func EncodeProfilePictureInfo(profilePictureInfo types.ProfilePictureInfo) *defproto.ProfilePictureInfo {
	return &defproto.ProfilePictureInfo{
		URL:        &profilePictureInfo.URL,
		ID:         &profilePictureInfo.ID,
		Type:       &profilePictureInfo.Type,
		DirectPath: &profilePictureInfo.DirectPath,
	}
}
func EncodeNewsletterReactionSettings(reactionSettings types.NewsletterReactionSettings) *defproto.NewsletterReactionSettings {
	var reactionMode defproto.NewsletterReactionSettings_NewsletterReactionsMode
	switch reactionSettings.Value {
	case types.NewsletterReactionsModeAll:
		reactionMode = defproto.NewsletterReactionSettings_ALL
	case types.NewsletterReactionsModeBasic:
		reactionMode = defproto.NewsletterReactionSettings_BASIC
	case types.NewsletterReactionsModeNone:
		reactionMode = defproto.NewsletterReactionSettings_NONE
	case types.NewsletterReactionsModeBlocklist:
		reactionMode = defproto.NewsletterReactionSettings_BLOCKLIST
	}
	return &defproto.NewsletterReactionSettings{
		Value: &reactionMode,
	}
}
func EncodeNewsletterSetting(settings types.NewsletterSettings) *defproto.NewsletterSetting {
	return &defproto.NewsletterSetting{
		ReactionCodes: EncodeNewsletterReactionSettings(settings.ReactionCodes),
	}
}
func EncodeNewsletterThreadMetadata(threadMetadata types.NewsletterThreadMetadata) *defproto.NewsletterThreadMetadata {
	var state defproto.NewsletterThreadMetadata_NewsletterVerificationState
	switch threadMetadata.VerificationState {
	case types.NewsletterVerificationStateVerified:
		state = defproto.NewsletterThreadMetadata_VERIFIED
	case types.NewsletterVerificationStateUnverified:
		state = defproto.NewsletterThreadMetadata_UNVERIFIED
	}
	metadata := defproto.NewsletterThreadMetadata{
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
func EncodeNewsletterViewerMetadata(viewerMetadata *types.NewsletterViewerMetadata) *defproto.NewsletterViewerMetadata {
	var mute defproto.NewsletterMuteState
	var role defproto.NewsletterRole
	switch viewerMetadata.Mute {
	case types.NewsletterMuteOff:
		mute = defproto.NewsletterMuteState_OFF
	case types.NewsletterMuteOn:
		mute = defproto.NewsletterMuteState_ON
	}
	switch viewerMetadata.Role {
	case types.NewsletterRoleSubscriber:
		role = defproto.NewsletterRole_SUBSCRIBER
	case types.NewsletterRoleGuest:
		role = defproto.NewsletterRole_GUEST
	case types.NewsletterRoleAdmin:
		role = defproto.NewsletterRole_ADMIN
	case types.NewsletterRoleOwner:
		role = defproto.NewsletterRole_OWNER

	}
	return &defproto.NewsletterViewerMetadata{
		Mute: &mute,
		Role: &role,
	}
}
func EncodeNewsLetterMessageMetadata(metadata types.NewsletterMetadata) *defproto.NewsletterMetadata {
	model := &defproto.NewsletterMetadata{
		ID:         EncodeJidProto(metadata.ID),
		State:      EncodeWrappedNewsletterState(metadata.State),
		ThreadMeta: EncodeNewsletterThreadMetadata(metadata.ThreadMeta),
	}
	if metadata.ViewerMeta != nil {
		model.ViewerMeta = EncodeNewsletterViewerMetadata(metadata.ViewerMeta)
	}
	return model
}
func EncodeBlocklist(blocklist *types.Blocklist) *defproto.Blocklist {
	JIDs := []*defproto.JID{}
	for _, jid := range blocklist.JIDs {
		JIDs = append(JIDs, EncodeJidProto(jid))
	}
	return &defproto.Blocklist{
		DHash: &blocklist.DHash,
		JIDs:  JIDs,
	}
}
func EncodeNewsletterMessage(message *types.NewsletterMessage) *defproto.NewsletterMessage {
	reacts := []*defproto.Reaction{}
	for react, count := range message.ReactionCounts {
		reacts = append(reacts, &defproto.Reaction{
			Type:  proto.String(react),
			Count: proto.Int64(int64(count)),
		})
	}
	return &defproto.NewsletterMessage{
		MessageServerID: proto.Int64(int64(message.MessageServerID)),
		ViewsCount:      proto.Int64(int64(message.ViewsCount)),
		Message:         message.Message,
		ReactionCounts:  reacts,
	}
}

func EncodePrivacySetting(privacy types.PrivacySetting) *defproto.PrivacySettings_PrivacySetting {
	var privacySetting defproto.PrivacySettings_PrivacySetting
	switch privacy {
	case types.PrivacySettingUndefined:
		privacySetting = defproto.PrivacySettings_UNDEFINED
	case types.PrivacySettingAll:
		privacySetting = defproto.PrivacySettings_ALL
	case types.PrivacySettingContacts:
		privacySetting = defproto.PrivacySettings_CONTACTS
	case types.PrivacySettingContactBlacklist:
		privacySetting = defproto.PrivacySettings_CONTACT_BLACKLIST
	case types.PrivacySettingMatchLastSeen:
		privacySetting = defproto.PrivacySettings_MATCH_LAST_SEEN
	case types.PrivacySettingKnown:
		privacySetting = defproto.PrivacySettings_KNOWN
	case types.PrivacySettingNone:
		privacySetting = defproto.PrivacySettings_NONE
	}
	return &privacySetting
}

func EncodePrivacySettings(privacySetting types.PrivacySettings) *defproto.PrivacySettings {
	return &defproto.PrivacySettings{
		GroupAdd:     EncodePrivacySetting(privacySetting.GroupAdd),
		LastSeen:     EncodePrivacySetting(privacySetting.LastSeen),
		Status:       EncodePrivacySetting(privacySetting.Status),
		Profile:      EncodePrivacySetting(privacySetting.Profile),
		ReadReceipts: EncodePrivacySetting(privacySetting.ReadReceipts),
		CallAdd:      EncodePrivacySetting(privacySetting.CallAdd),
		Online:       EncodePrivacySetting(privacySetting.Online),
	}
}

func EncodeStatusPrivacy(statusPrivacy types.StatusPrivacy) *defproto.StatusPrivacy {
	var ptype defproto.StatusPrivacy_StatusPrivacyType
	JIDS := []*defproto.JID{}
	switch statusPrivacy.Type {
	case types.StatusPrivacyTypeBlacklist:
		ptype = defproto.StatusPrivacy_BLACKLIST
	case types.StatusPrivacyTypeContacts:
		ptype = defproto.StatusPrivacy_CONTACTS
	case types.StatusPrivacyTypeWhitelist:
		ptype = defproto.StatusPrivacy_WHITELIST
	}
	for _, jid := range statusPrivacy.List {
		JIDS = append(JIDS, EncodeJidProto(jid))
	}
	return &defproto.StatusPrivacy{
		Type:      &ptype,
		List:      JIDS,
		IsDefault: &statusPrivacy.IsDefault,
	}
}

func EncodeGroupLinkTarget(group types.GroupLinkTarget) *defproto.GroupLinkTarget {
	return &defproto.GroupLinkTarget{
		JID:               EncodeJidProto(group.JID),
		GroupName:         EncodeGroupName(group.GroupName),
		GroupIsDefaultSub: EncodeGroupIsDefaultSub(group.GroupIsDefaultSub),
	}
}

func EncodeContactQRLinkTarget(contact types.ContactQRLinkTarget) *defproto.ContactQRLinkTarget {
	return &defproto.ContactQRLinkTarget{
		JID:      EncodeJidProto(contact.JID),
		Type:     &contact.Type,
		PushName: &contact.PushName,
	}
}

func EncodeBusinessMessageLinkTarget(message types.BusinessMessageLinkTarget) *defproto.BusinessMessageLinkTarget {
	return &defproto.BusinessMessageLinkTarget{
		JID:           EncodeJidProto(message.JID),
		PushName:      proto.String(message.PushName),
		VerifiedName:  proto.String(message.VerifiedName),
		IsSigned:      &message.IsSigned,
		VerifiedLevel: &message.VerifiedLevel,
		Message:       &message.Message,
	}
}

func EncodePairSuccess(pair *events.PairSuccess) *defproto.PairStatus {
	return &defproto.PairStatus{
		ID:           EncodeJidProto(pair.ID),
		BusinessName: &pair.BusinessName,
		Platform:     &pair.Platform,
		Status:       defproto.PairStatus_SUCCESS.Enum(),
	}
}

func EncodePairError(pair *events.PairError) *defproto.PairStatus {
	return &defproto.PairStatus{
		ID:           EncodeJidProto(pair.ID),
		BusinessName: &pair.BusinessName,
		Platform:     &pair.Platform,
		Status:       defproto.PairStatus_ERROR.Enum(),
		Error:        proto.String(pair.Error.Error()),
	}
}
func EncodeConnectFailureReason(reason_types events.ConnectFailureReason) *defproto.ConnectFailureReason {
	var reason *defproto.ConnectFailureReason
	switch reason_types {
	case events.ConnectFailureGeneric:
		reason = defproto.ConnectFailureReason_GENERIC.Enum()
	case events.ConnectFailureLoggedOut:
		reason = defproto.ConnectFailureReason_LOGGED_OUT.Enum()
	case events.ConnectFailureTempBanned:
		reason = defproto.ConnectFailureReason_TEMP_BANNED.Enum()
	case events.ConnectFailureMainDeviceGone:
		reason = defproto.ConnectFailureReason_MAIN_DEVICE_GONE.Enum()
	case events.ConnectFailureUnknownLogout:
		reason = defproto.ConnectFailureReason_UNKNOWN_LOGOUT.Enum()
	case events.ConnectFailureClientOutdated:
		reason = defproto.ConnectFailureReason_CLIENT_OUTDATED.Enum()
	case events.ConnectFailureBadUserAgent:
		reason = defproto.ConnectFailureReason_BAD_USER_AGENT.Enum()
	case events.ConnectFailureInternalServerError:
		reason = defproto.ConnectFailureReason_INTERNAL_SERVER_ERROR.Enum()
	case events.ConnectFailureExperimental:
		reason = defproto.ConnectFailureReason_EXPERIMENTAL.Enum()
	case events.ConnectFailureServiceUnavailable:
		reason = defproto.ConnectFailureReason_SERVICE_UNAVAILABLE.Enum()
	}
	return reason
}
func EncodeLoggedOut(logout *events.LoggedOut) *defproto.LoggedOut {
	return &defproto.LoggedOut{
		OnConnect: &logout.OnConnect,
		Reason:    EncodeConnectFailureReason(logout.Reason),
	}
}

func EncodeTemporaryBan(ban *events.TemporaryBan) *defproto.TemporaryBan {
	var reason *defproto.TemporaryBan_TempBanReason
	switch ban.Code {
	case events.TempBanSentToTooManyPeople:
		reason = defproto.TemporaryBan_SEND_TO_TOO_MANY_PEOPLE.Enum()
	case events.TempBanBlockedByUsers:
		reason = defproto.TemporaryBan_BLOCKED_BY_USERS.Enum()
	case events.TempBanCreatedTooManyGroups:
		reason = defproto.TemporaryBan_CREATED_TOO_MANY_GROUPS.Enum()
	case events.TempBanSentTooManySameMessage:
		reason = defproto.TemporaryBan_SENT_TOO_MANY_SAME_MESSAGE.Enum()
	case events.TempBanBroadcastList:
		reason = defproto.TemporaryBan_BROADCAST_LIST.Enum()
	}
	return &defproto.TemporaryBan{
		Code:   reason,
		Expire: proto.Int64(int64(ban.Expire.Seconds())),
	}
}
func EncodeNodeAttrs(attrs waBinary.Attrs) []*defproto.NodeAttrs {
	n_attr := []*defproto.NodeAttrs{}
	for k, v := range attrs {
		attr := defproto.NodeAttrs{Name: proto.String(k)}
		switch value := v.(type) {
		case int:
			attr.Value = &defproto.NodeAttrs_Integer{Integer: *proto.Int64(int64(value))}
		case int32:
			attr.Value = &defproto.NodeAttrs_Integer{Integer: *proto.Int64(int64(value))}
		case int64:
			attr.Value = &defproto.NodeAttrs_Integer{Integer: *proto.Int64(int64(value))}
		case bool:
			attr.Value = &defproto.NodeAttrs_Boolean{Boolean: value}
		case string:
			attr.Value = &defproto.NodeAttrs_Text{Text: value}
		case types.JID:
			attr.Value = &defproto.NodeAttrs_Jid{Jid: EncodeJidProto(value)}
		}
		n_attr = append(n_attr, &attr)
	}
	return n_attr
}
func EncodeNode(node *waBinary.Node) *defproto.Node {
	nodes := defproto.Node{
		Tag:   &node.Tag,
		Attrs: EncodeNodeAttrs(node.Attrs),
	}
	switch v := node.Content.(type) {
	case nil:
		nodes.Nil = proto.Bool(true)
	case []waBinary.Node:
		var content = make([]*defproto.Node, len(v))
		for i, c_node := range v {
			content[i] = EncodeNode(&c_node)
		}
		nodes.Nodes = content
	case []byte:
		nodes.Bytes = v
	}

	return &nodes

}
func EncodeConnectFailure(connect *events.ConnectFailure) *defproto.ConnectFailure {
	return &defproto.ConnectFailure{
		Reason:  EncodeConnectFailureReason(connect.Reason),
		Message: &connect.Message,
		Raw:     EncodeNode(connect.Raw),
	}
}

func EncodeReceipts(receipt *events.Receipt) defproto.Receipt {
	var Type *defproto.Receipt_ReceiptType
	switch receipt.Type {
	case types.ReceiptTypeDelivered:
		Type = defproto.Receipt_DELIVERED.Enum()
	case types.ReceiptTypeSender:
		Type = defproto.Receipt_SENDER.Enum()
	case types.ReceiptTypeRetry:
		Type = defproto.Receipt_RETRY.Enum()
	case types.ReceiptTypeRead:
		Type = defproto.Receipt_READ.Enum()
	case types.ReceiptTypeReadSelf:
		Type = defproto.Receipt_READ_SELF.Enum()
	case types.ReceiptTypePlayed:
		Type = defproto.Receipt_PLAYED.Enum()
	case types.ReceiptTypePlayedSelf:
		Type = defproto.Receipt_SERVER_ERROR.Enum()
	case types.ReceiptTypeInactive:
		Type = defproto.Receipt_INACTIVE.Enum()
	case types.ReceiptTypePeerMsg:
		Type = defproto.Receipt_PEER_MSG.Enum()
	case types.ReceiptTypeHistorySync:
		Type = defproto.Receipt_HISTORY_SYNC.Enum()
	}
	return defproto.Receipt{
		MessageSource: EncodeMessageSource(receipt.MessageSource),
		MessageIDs:    receipt.MessageIDs,
		Timestamp:     proto.Int64(receipt.Timestamp.Unix()),
		Type:          Type,
	}
}

func EncodeChatPresence(presence *events.ChatPresence) defproto.ChatPresence {
	var chat_presence *defproto.ChatPresence_ChatPresence
	var chat_presence_media *defproto.ChatPresence_ChatPresenceMedia
	switch presence.State {
	case types.ChatPresenceComposing:
		chat_presence = defproto.ChatPresence_COMPOSING.Enum()
	case types.ChatPresencePaused:
		chat_presence = defproto.ChatPresence_PAUSED.Enum()
	}
	switch presence.Media {
	case types.ChatPresenceMediaAudio:
		chat_presence_media = defproto.ChatPresence_AUDIO.Enum()
	case types.ChatPresenceMediaText:
		chat_presence_media = defproto.ChatPresence_TEXT.Enum()
	}
	return defproto.ChatPresence{
		MessageSource: EncodeMessageSource(presence.MessageSource),
		State:         chat_presence,
		Media:         chat_presence_media,
	}
}
func EncodePresence(presence *events.Presence) defproto.Presence {
	return defproto.Presence{
		From:        EncodeJidProto(presence.From),
		Unavailable: &presence.Unavailable,
		LastSeen:    proto.Int64(presence.LastSeen.Unix()),
	}
}

func EncodeJoinedGroup(joined *events.JoinedGroup) defproto.JoinedGroup {
	return defproto.JoinedGroup{
		Reason:    &joined.Reason,
		Type:      &joined.Reason,
		CreateKey: &joined.CreateKey,
		GroupInfo: EncodeGroupInfo(&joined.GroupInfo),
	}
}
func EncodeGroupDelete(delete types.GroupDelete) *defproto.GroupDelete {
	return &defproto.GroupDelete{
		Deleted:       &delete.Deleted,
		DeletedReason: &delete.DeleteReason,
	}
}
func EncodeGroupLinkChange(group *types.GroupLinkChange) *defproto.GroupLinkChange {
	var Type *defproto.GroupLinkChange_ChangeType
	switch group.Type {
	case types.GroupLinkChangeTypeParent:
		Type = defproto.GroupLinkChange_PARENT.Enum()
	case types.GroupLinkChangeTypeSub:
		Type = defproto.GroupLinkChange_SUB.Enum()
	case types.GroupLinkChangeTypeSibling:
		Type = defproto.GroupLinkChange_SIBLING.Enum()
	}
	return &defproto.GroupLinkChange{
		Type:         Type,
		UnlinkReason: (*string)(&group.UnlinkReason),
		Group:        EncodeGroupLinkTarget(group.Group),
	}
}
func EncodeGroupInfoEvent(groupInfo *events.GroupInfo) *defproto.GroupInfoEvent {
	var Join = make([]*defproto.JID, len(groupInfo.Join))
	var Leave = make([]*defproto.JID, len(groupInfo.Leave))
	var Promote = make([]*defproto.JID, len(groupInfo.Promote))
	var Demote = make([]*defproto.JID, len(groupInfo.Demote))
	var UnknownChanges = make([]*defproto.Node, len(groupInfo.UnknownChanges))
	for i, jidJoin := range groupInfo.Join {
		Join[i] = EncodeJidProto(jidJoin)
	}
	for i, jidLeave := range groupInfo.Leave {
		Leave[i] = EncodeJidProto(jidLeave)
	}
	for i, jidPromote := range groupInfo.Promote {
		Promote[i] = EncodeJidProto(jidPromote)
	}
	for i, jidDemote := range groupInfo.Demote {
		Demote[i] = EncodeJidProto(jidDemote)
	}
	for i, changes := range groupInfo.UnknownChanges {
		UnknownChanges[i] = EncodeNode(changes)
	}
	group_info := defproto.GroupInfoEvent{
		JID:                       EncodeJidProto(groupInfo.JID),
		Notify:                    &groupInfo.Notify,
		Timestamp:                 proto.Int64(groupInfo.Timestamp.Unix()),
		PrevParticipantsVersionID: &groupInfo.PrevParticipantVersionID,
		ParticipantVersionID:      &groupInfo.ParticipantVersionID,
		JoinReason:                &groupInfo.JoinReason,
		Join:                      Join,
		Leave:                     Leave,
		Promote:                   Promote,
		Demote:                    Demote,
		UnknownChanges:            UnknownChanges,
	}
	if groupInfo.Sender != nil {
		group_info.Sender = EncodeJidProto(*groupInfo.Sender)
	}
	if groupInfo.Name != nil {
		group_info.Name = EncodeGroupName(*groupInfo.Name)
	}
	if groupInfo.Topic != nil {
		group_info.Topic = EncodeGroupTopic(*groupInfo.Topic)
	}
	if groupInfo.Locked != nil {
		group_info.Locked = EncodeGroupLocked(*groupInfo.Locked)
	}
	if groupInfo.Announce != nil {
		group_info.Announce = EncodeGroupAnnounce(*groupInfo.Announce)
	}
	if groupInfo.Ephemeral != nil {
		group_info.Ephemeral = EncodeGroupEphemeral(*groupInfo.Ephemeral)
	}
	if groupInfo.Delete != nil {
		group_info.Delete = EncodeGroupDelete(*groupInfo.Delete)
	}
	if groupInfo.Link != nil {
		group_info.Link = EncodeGroupLinkChange(groupInfo.Link)
	}
	if groupInfo.Unlink != nil {
		group_info.Unlink = EncodeGroupLinkChange(groupInfo.Unlink)
	}
	if groupInfo.NewInviteLink != nil {
		group_info.NewInviteLink = groupInfo.NewInviteLink
	}
	return &group_info
}

func EncodeBlocklistChange(blocklist *events.BlocklistChange) *defproto.BlocklistChange {
	var action *defproto.BlocklistChange_Action
	switch blocklist.Action {
	case events.BlocklistChangeActionBlock:
		action = defproto.BlocklistChange_BLOCK.Enum()
	case events.BlocklistChangeActionUnblock:
		action = defproto.BlocklistChange_UNBLOCK.Enum()
	}
	return &defproto.BlocklistChange{
		JID:         EncodeJidProto(blocklist.JID),
		BlockAction: action,
	}
}

func EncodeBlocklistEvent(blocklist *events.Blocklist) defproto.BlocklistEvent {
	var action *defproto.BlocklistEvent_Actions
	var blocklistchanges = make([]*defproto.BlocklistChange, len(blocklist.Changes))
	for i, changes := range blocklist.Changes {
		blocklistchanges[i] = EncodeBlocklistChange(&changes)
	}
	switch blocklist.Action {
	case events.BlocklistActionDefault:
		action = defproto.BlocklistEvent_DEFAULT.Enum()
	case events.BlocklistActionModify:
		action = defproto.BlocklistEvent_MODIFY.Enum()
	}
	return defproto.BlocklistEvent{
		Action:    action,
		DHASH:     &blocklist.DHash,
		PrevDHash: &blocklist.PrevDHash,
		Changes:   blocklistchanges,
	}
}

func EncodeNewsletterLeave(leave *events.NewsletterLeave) defproto.NewsletterLeave {
	var role *defproto.NewsletterRole
	switch leave.Role {
	case types.NewsletterRoleAdmin:
		role = defproto.NewsletterRole_ADMIN.Enum()
	case types.NewsletterRoleGuest:
		role = defproto.NewsletterRole_GUEST.Enum()
	case types.NewsletterRoleOwner:
		role = defproto.NewsletterRole_OWNER.Enum()
	case types.NewsletterRoleSubscriber:
		role = defproto.NewsletterRole_SUBSCRIBER.Enum()
	}
	return defproto.NewsletterLeave{
		ID:   EncodeJidProto(leave.ID),
		Role: role,
	}
}
func EncodeNewsletterMuteChange(mute *events.NewsletterMuteChange) defproto.NewsletterMuteChange {
	var state *defproto.NewsletterMuteState
	switch mute.Mute {
	case types.NewsletterMuteOff:
		state = defproto.NewsletterMuteState_OFF.Enum()
	case types.NewsletterMuteOn:
		state = defproto.NewsletterMuteState_ON.Enum()
	}
	return defproto.NewsletterMuteChange{
		ID:   EncodeJidProto(mute.ID),
		Mute: state,
	}
}
func EncodeNewsletterLiveUpdate(update *events.NewsletterLiveUpdate) defproto.NewsletterLiveUpdate {
	var messages = make([]*defproto.NewsletterMessage, len(update.Messages))
	for i, message := range update.Messages {
		messages[i] = EncodeNewsletterMessage(message)
	}
	return defproto.NewsletterLiveUpdate{
		JID:      EncodeJidProto(update.JID),
		TIME:     proto.Int64(int64(update.Time.Unix())),
		Messages: messages,
	}
}

func EncodeContactInfo(info types.ContactInfo) *defproto.ContactInfo {
	return &defproto.ContactInfo{
		Found:        proto.Bool(info.Found),
		FirstName:    proto.String(info.FirstName),
		FullName:     proto.String(info.FullName),
		PushName:     proto.String(info.PushName),
		BusinessName: proto.String(info.BusinessName),
	}
}

func EncodeContacts(info map[types.JID]types.ContactInfo) []*defproto.Contact {
	var contacts = make([]*defproto.Contact, len(info))
	i := 0
	for k, v := range info {
		contacts[i] = &defproto.Contact{
			JID:  EncodeJidProto(k),
			Info: EncodeContactInfo(v),
		}
		i++
	}
	return contacts
}

func EncodeBasicCallMeta(basicCallMeta types.BasicCallMeta) *defproto.BasicCallMeta {
	return &defproto.BasicCallMeta{
		From:        EncodeJidProto(basicCallMeta.From),
		Timestamp:   proto.Int64(int64(basicCallMeta.Timestamp.Unix())),
		CallCreator: EncodeJidProto(basicCallMeta.CallCreator),
		CallID:      proto.String(basicCallMeta.CallID),
	}
}

func EncodeCallRemoteMeta(callRemoteMeta types.CallRemoteMeta) *defproto.CallRemoteMeta {
	return &defproto.CallRemoteMeta{
		RemotePlatform: proto.String(callRemoteMeta.RemotePlatform),
		RemoteVersion:  proto.String(callRemoteMeta.RemoteVersion),
	}
}

func EncodeUndecryptableMessageEvent(undecryptableMessage events.UndecryptableMessage) *defproto.UndecryptableMessage {
	var failMode defproto.UndecryptableMessage_DecryptFailModeT
	switch undecryptableMessage.DecryptFailMode {
	case "":
		failMode = defproto.UndecryptableMessage_DECRYPT_FAIL_SHOW
	case "hide":
		failMode = defproto.UndecryptableMessage_DECRYPT_FAIL_HIDE
	}
	return &defproto.UndecryptableMessage{
		Info:            EncodeMessageInfo(undecryptableMessage.Info),
		IsUnavailable:   &undecryptableMessage.IsUnavailable,
		DecryptFailMode: &failMode,
	}
}
