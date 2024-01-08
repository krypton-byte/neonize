package main

/*

   #include <stdlib.h>
   #include <stdbool.h>
   #include <stdint.h>
   #include "header/cstruct.h"
   #include "python/pythonptr.h"
*/
import "C"
import (
	"context"
	"fmt"
	"strings"
	"time"
	"unsafe"

	"github.com/krypton-byte/neonize/neonize"
	"github.com/krypton-byte/neonize/utils"
	_ "github.com/mattn/go-sqlite3"
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/store"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"

	waProto "go.mau.fi/whatsmeow/binary/proto"
	waLog "go.mau.fi/whatsmeow/util/log"
	"google.golang.org/protobuf/proto"
)

var clients = make(map[string]*whatsmeow.Client)

func getByteByAddr(addr *C.uchar, size C.int) []byte {
	return C.GoBytes(unsafe.Pointer(addr), size)
	// var result []byte
	// for i := 0; i < int(size); i++ {
	// 	value := *(*C.uchar)(unsafe.Pointer(uintptr(unsafe.Pointer(addr)) + uintptr(i)))
	// 	// 	fmt.Println(value)
	// 	result = append(result, byte(value))
	// }
	// return result
}

func ReturnBytes(data []byte) C.struct_BytesReturn {
	size := C.size_t(len(data))
	ptr := (*C.char)(C.CBytes(data))
	// defer C.free(unsafe.Pointer(&ptr))
	return C.struct_BytesReturn{ptr, size}
}

//export Upload
func Upload(id *C.char, mediabuff *C.uchar, mediaSize C.int, mediatype C.int) C.struct_BytesReturn {
	client := clients[C.GoString(id)]
	data := getByteByAddr(mediabuff, mediaSize)
	response, err_upload := client.Upload(context.Background(), data, utils.MediaType[int(mediatype)])
	return_ := neonize.UploadReturnFunction{}
	if err_upload != nil {
		return_.Error = proto.String(err_upload.Error())
	}
	return_.UploadResponse = utils.EncodeUploadResponse(response)
	return_buf, err := proto.Marshal(&return_)
	if err != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export GenerateMessageID
func GenerateMessageID(id *C.char) *C.char {
	return C.CString(clients[C.GoString(id)].GenerateMessageID())
}

//export AcceptTOSNotice
func AcceptTOSNotice(id *C.char, noticeID *C.char, stage *C.char) *C.char {
	err := clients[C.GoString(id)].AcceptTOSNotice(C.GoString(noticeID), C.GoString(stage))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export SendMessage
func SendMessage(id *C.char, JIDByte *C.uchar, JIDSize C.int, messageByte *C.uchar, messageSize C.int) C.struct_BytesReturn {
	client := clients[C.GoString(id)]
	jid := getByteByAddr(JIDByte, JIDSize)
	var neonize_jid neonize.JID
	err := proto.Unmarshal(jid, &neonize_jid)
	if err != nil {
		panic(err)
	}
	message_bytes := getByteByAddr(messageByte, messageSize)
	var message waProto.Message
	err_message := proto.Unmarshal(message_bytes, &message)
	if err_message != nil {
		panic(err)
	}
	sendresponse, err := client.SendMessage(context.Background(), utils.DecodeJidProto(&neonize_jid), &message)
	return_ := neonize.SendMessageReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_.SendResponse = utils.EncodeSendResponse(sendresponse)
	return_buf, err := proto.Marshal(&return_)
	if err != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export Neonize
func Neonize(db *C.char, id *C.char, logLevel *C.char, qrCb C.ptr_to_python_function_string, logStatus C.ptr_to_python_function_string, event C.ptr_to_python_function_bytes, subscribes *C.uchar, lenSubscriber C.int, blocking C.ptr_to_python_function, devicePropsBuf *C.uchar, devicePropsSize C.int, pairphone *C.uchar, pairphoneSize C.int) { // ,
	subscribers := map[int]bool{}
	var deviceProps waProto.DeviceProps
	var loginStateChan = make(chan bool)
	err_proto := proto.Unmarshal(getByteByAddr(devicePropsBuf, devicePropsSize), &deviceProps)
	if err_proto != nil {
		panic(err_proto)
	}
	for _, s := range getByteByAddr(subscribes, lenSubscriber) {
		subscribers[int(s)] = true
	}
	dbLog := waLog.Stdout("Database", C.GoString(logLevel), true)
	// Make sure you add appropriate DB connector imports, e.g. github.com/mattn/go-sqlite3 for SQLite
	container, err := sqlstore.New("sqlite3", fmt.Sprintf("file:%s?_foreign_keys=on", C.GoString(db)), dbLog)
	if err != nil {
		panic(err)
	}
	// If you want multiple sessions, remember their JIDs and use .GetDevice(jid) or .GetAllDevices() instead.
	deviceStore, err := container.GetFirstDevice()
	if err != nil {
		panic(err)
	}
	proto.Merge(store.DeviceProps, &deviceProps)
	clientLog := waLog.Stdout("Client", C.GoString(logLevel), true)
	client := whatsmeow.NewClient(deviceStore, clientLog)
	uuid := C.GoString(id)
	clients[uuid] = client
	eventHandler := func(evt interface{}) {
		switch v := evt.(type) {
		case *events.Message:
			if err != nil {
				panic(err)
			}
			if _, ok := subscribers[14]; ok {
				messageSource := utils.EncodeEventTypesMessage(v)
				messageSourceBytes, err := proto.Marshal(messageSource)
				if err != nil {
					panic(err)
				}
				messageSourceCDATA := (*C.char)(unsafe.Pointer(&messageSourceBytes[0]))
				messageSourceCSize := C.size_t(len(messageSourceBytes))
				C.call_c_func_callback_bytes(event, messageSourceCDATA, messageSourceCSize, C.int(14))
			}
			// C.free(unsafe.Pointer(CData))
		case *events.Connected:
			loginStateChan <- true
		}
	}
	client.AddEventHandler(eventHandler)
	qrFuncCb := func(data string) {
		cstr := C.CString(data)
		defer C.free(unsafe.Pointer(cstr))
		C.call_c_func_string(qrCb, cstr)
	}
	logStatusCb := func(eventName string) {
		cstr := C.CString(eventName)
		defer C.free(unsafe.Pointer(cstr))
		C.call_c_func_string(logStatus, cstr)
	}
	if client.Store.ID == nil {
		// No ID stored, new login
		if int(pairphoneSize) > 0 {
			phone_number := getByteByAddr(pairphone, pairphoneSize)
			var PairPhone neonize.PairPhoneParams
			err_pairparams := proto.Unmarshal(phone_number, &PairPhone)
			if err_pairparams != nil {
				panic(err_pairparams)
			}
			phone := *PairPhone.Phone
			notif := *PairPhone.ShowPushNotification
			displayname := *PairPhone.ClientDisplayName
			clientType := *PairPhone.ClientType
			client.Connect()
			code_, code_err := client.PairPhone(phone, notif, whatsmeow.PairClientType(int(clientType)), displayname)
			if code_err != nil {
				panic(code_err)
			}
			fmt.Println("Pair Code: ", code_)
			for stat := range loginStateChan {
				if stat {
					break
				}
			}

		} else {
			qrChan, _ := client.GetQRChannel(context.Background())
			err = client.Connect()
			if err != nil {
				panic(err)
			}
			for evt := range qrChan {
				if evt.Event == "code" {
					// Render the QR code here
					// e.g. qrterminal.GenerateHalfBlock(evt.Code, qrterminal.L, os.Stdout)
					// or just manually `echo 2@... | qrencode -t ansiutf8` in a terminal
					go qrFuncCb(evt.Code)
					// C.free(unsafe.Pointer(cstr))
				} else {
					fmt.Println("Login event:", evt.Event)
					go logStatusCb(evt.Event)
				}
			}
		}

	} else {
		// Already logged in, just connect
		err = client.Connect()
		if err != nil {
			panic(err)
		}
	}

	// Listen to Ctrl+C (you can also do something else that prevents the program from exiting)
	C.call_c_func(blocking, false)
}

//export Disconnect
func Disconnect(id *C.char) {
	clients[C.GoString(id)].Disconnect()
}

//export Download
func Download(id *C.char, messageProto *C.uchar, size C.int) C.struct_BytesReturn {
	var message waProto.Message
	err := proto.Unmarshal(getByteByAddr(messageProto, size), &message)
	if err != nil {
		panic(err)
	}
	data_buff, err := clients[C.GoString(id)].DownloadAny(&message)
	return_ := neonize.DownloadReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	if data_buff != nil {
		return_.Binary = data_buff
	}
	return ReturnBytes(data_buff)

}

//export IsOnWhatsApp
func IsOnWhatsApp(id *C.char, numbers *C.char) C.struct_BytesReturn {
	onWhatsApp := []*neonize.IsOnWhatsAppResponse{}
	return_ := neonize.IsOnWhatsAppReturnFunction{}
	response, err := clients[C.GoString(id)].IsOnWhatsApp(strings.Split(C.GoString(numbers), " "))
	for _, participant := range response {
		onWhatsApp = append(onWhatsApp, utils.EncodeIsOnWhatsApp(participant))
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_.IsOnWhatsAppResponse = onWhatsApp
	return_buf, err := proto.Marshal(&return_)
	if err != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export IsConnected
func IsConnected(id *C.char) C.bool {
	check := clients[C.GoString(id)].IsConnected()
	return C.bool(check)
}

//export IsLoggedIn
func IsLoggedIn(id *C.char) C.bool {
	check := clients[C.GoString(id)].IsConnected()
	return C.bool(check)
}

//export GetUserInfo
func GetUserInfo(id *C.char, JIDSByte *C.uchar, JIDSSize C.int) C.struct_BytesReturn {
	var NeoJIDS neonize.JIDArray
	JIDSBuf := getByteByAddr(JIDSByte, JIDSSize)
	err := proto.Unmarshal(JIDSBuf, &NeoJIDS)
	if err != nil {
		panic(err)
	}
	JIDS := []types.JID{}
	for _, jid := range NeoJIDS.JIDS {
		JIDS = append(JIDS, utils.DecodeJidProto(jid))
	}
	user_info, err := clients[C.GoString(id)].GetUserInfo(JIDS)
	return_ := neonize.GetUserInfoReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	usersinfo := []*neonize.GetUserInfoSingleReturnFunction{}
	for jid, info := range user_info {
		singlereturn := &neonize.GetUserInfoSingleReturnFunction{
			JID:      utils.EncodeJidProto(jid),
			UserInfo: utils.EncodeUserInfo(info),
		}

		usersinfo = append(usersinfo, singlereturn)
	}
	return_.UsersInfo = usersinfo
	return_buf, marshal_err := proto.Marshal(&return_)
	if marshal_err != nil {
		panic(marshal_err)
	}
	return ReturnBytes(return_buf)
}

// /GROUP
//
//export GetGroupInfo
func GetGroupInfo(id *C.char, JIDByte *C.uchar, JIDSize C.int) C.struct_BytesReturn {
	var neoJIDProto neonize.JID
	jidbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(jidbyte, &neoJIDProto)
	if err != nil {
		panic(err)
	}
	decodeJid := utils.DecodeJidProto(&neoJIDProto)
	info, err_info := clients[C.GoString(id)].GetGroupInfo(decodeJid)
	groupinfo := neonize.GetGroupInfoReturnFunction{}
	if err_info != nil {
		groupinfo.Error = proto.String(err_info.Error())
	}
	if info != nil {
		groupinfo.GroupInfo = utils.EncodeGroupInfo(info)
	}
	databuf, err_ := proto.Marshal(&groupinfo)
	if err_ != nil {
		panic(err_)
	}
	return ReturnBytes(databuf)
}

//export GetGroupInfoFromInvite
func GetGroupInfoFromInvite(id *C.char, JIDByte *C.uchar, JIDSize C.int, inviter *C.uchar, inviterSize C.int, code *C.char, expiration C.int) C.struct_BytesReturn {
	var JIDInviter neonize.JID
	var JID neonize.JID
	err_jid := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err_jid != nil {
		panic(err_jid)
	}
	err_inviter := proto.Unmarshal(getByteByAddr(inviter, inviterSize), &JIDInviter)
	if err_inviter != nil {
		panic(err_inviter)
	}
	group_info, err := clients[C.GoString(id)].GetGroupInfoFromInvite(utils.DecodeJidProto(&JID), utils.DecodeJidProto(&JIDInviter), C.GoString(code), int64(expiration))
	return_proto := neonize.GetGroupInfoReturnFunction{}
	if err != nil {
		return_proto.Error = proto.String(err.Error())
	}
	if group_info != nil {
		return_proto.GroupInfo = utils.EncodeGroupInfo(group_info)
	}
	return_, err_marshal := proto.Marshal(&return_proto)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_)
}

//export GetGroupInfoFromLink
func GetGroupInfoFromLink(id *C.char, code *C.char) C.struct_BytesReturn {
	return_proto := neonize.GetGroupInfoReturnFunction{}
	info, err := clients[C.GoString(id)].GetGroupInfoFromLink(C.GoString(code))
	if err != nil {
		return_proto.Error = proto.String(err.Error())
	}
	if info != nil {
		return_proto.GroupInfo = utils.EncodeGroupInfo(info)
	}
	return_, err_marshal := proto.Marshal(&return_proto)
	if err_marshal != nil {
		panic(err)
	}
	return ReturnBytes(return_)
}

//export GetGroupRequestParticipants
func GetGroupRequestParticipants(id *C.char, JIDByte *C.uchar, JIDSize C.int) C.struct_BytesReturn {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	request_participants, err_request := clients[C.GoString(id)].GetGroupRequestParticipants(utils.DecodeJidProto(&JID))
	participants := []*neonize.JID{}
	for _, participant := range request_participants {
		participants = append(participants, utils.EncodeJidProto(participant))
	}
	return_ := neonize.GetGroupRequestParticipantsReturnFunction{
		Participants: participants,
	}
	if err_request != nil {
		return_.Error = proto.String(err_request.Error())
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export GetLinkedGroupsParticipants
func GetLinkedGroupsParticipants(id *C.char, JIDByte *C.uchar, JIDSize C.int) C.struct_BytesReturn {
	var JID neonize.JID
	return_ := neonize.GetGroupRequestParticipantsReturnFunction{}
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	JIDS, err_get := clients[C.GoString(id)].GetLinkedGroupsParticipants(utils.DecodeJidProto(&JID))
	if err_get != nil {
		return_.Error = proto.String(err_get.Error())
	}
	neonizeJID := []*neonize.JID{}
	for _, jid := range JIDS {
		neonizeJID = append(neonizeJID, utils.EncodeJidProto(jid))
	}
	return_.Participants = neonizeJID
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export SetGroupName
func SetGroupName(id *C.char, JIDByte *C.uchar, JIDSize C.int, name *C.char) *C.char {
	jidbyte := getByteByAddr(JIDByte, JIDSize)
	var neoJIDProto neonize.JID
	err := proto.Unmarshal(jidbyte, &neoJIDProto)
	if err != nil {
		panic(err)
	}
	status_err := clients[C.GoString(id)].SetGroupName(utils.DecodeJidProto(&neoJIDProto), C.GoString(name))
	if status_err != nil {
		return C.CString(status_err.Error())

	}
	return C.CString("")

}

//export SetGroupPhoto
func SetGroupPhoto(id *C.char, JIDByte *C.uchar, JIDSize C.int, Photo *C.uchar, PhotoSize C.int) C.struct_BytesReturn {
	var neoJIDProto neonize.JID
	JIDbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(JIDbyte, &neoJIDProto)
	if err != nil {
		panic(err)
	}
	photo_buf := getByteByAddr(Photo, PhotoSize)
	response, err_status := clients[C.GoString(id)].SetGroupPhoto(utils.DecodeJidProto(&neoJIDProto), photo_buf)
	return_ := neonize.SetGroupPhotoReturnFunction{
		PictureID: &response,
	}
	if err_status != nil {
		return_.Error = proto.String(err_status.Error())
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)
}

//export LeaveGroup
func LeaveGroup(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.char {
	var neoJIDProto neonize.JID
	JIDbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(JIDbyte, &neoJIDProto)
	if err != nil {
		panic(err)
	}
	err_status := clients[C.GoString(id)].LeaveGroup(utils.DecodeJidProto(&neoJIDProto))
	if err_status != nil {
		return C.CString(err_status.Error())
	}
	return C.CString("")
}

//export GetGroupInviteLink
func GetGroupInviteLink(id *C.char, JIDByte *C.uchar, JIDSize C.int, revoke C.bool) C.struct_BytesReturn {
	var neoJIDProto neonize.JID
	JIDbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(JIDbyte, &neoJIDProto)
	if err != nil {
		panic(err)
	}
	url, err := clients[C.GoString(id)].GetGroupInviteLink(utils.DecodeJidProto(&neoJIDProto), bool(revoke))
	return_ := neonize.GetGroupInviteLinkReturnFunction{
		InviteLink: &url,
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)
}

//export JoinGroupWithLink
func JoinGroupWithLink(id *C.char, code *C.char) C.struct_BytesReturn {
	jid, err := clients[C.GoString(id)].JoinGroupWithLink(C.GoString(code))

	neojid := utils.EncodeJidProto(jid)

	return_ := neonize.JoinGroupWithLinkReturnFunction{
		Jid: neojid,
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}

	jidBuf, err_ := proto.Marshal(&return_)

	if err_ != nil {
		panic(err_)
	}
	return ReturnBytes(jidBuf)
}

//export JoinGroupWithInvite
func JoinGroupWithInvite(id *C.char, JIDByte *C.uchar, JIDSize C.int, inviterByte *C.uchar, inviterSize C.int, code *C.char, expiration C.int) *C.char {
	var JID, Inviter neonize.JID
	err := proto.Unmarshal(getByteByAddr(inviterByte, inviterSize), &Inviter)
	if err != nil {
		panic(err)
	}
	err_unmarshal := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err_unmarshal != nil {
		panic(err)
	}
	err_join := clients[C.GoString(id)].JoinGroupWithInvite(utils.DecodeJidProto(&JID), utils.DecodeJidProto(&Inviter), C.GoString(code), int64(expiration))
	if err != nil {
		return C.CString(err_join.Error())
	}
	return C.CString("")
}

//export LinkGroup
func LinkGroup(id *C.char, parent *C.uchar, parentSize C.int, child *C.uchar, childSize C.int) *C.char {
	var parentJID, childJID neonize.JID
	err_parent := proto.Unmarshal(getByteByAddr(parent, parentSize), &parentJID)
	if err_parent != nil {
		panic(err_parent)
	}
	err_child := proto.Unmarshal(getByteByAddr(child, childSize), &childJID)
	if err_child != nil {
		panic(err_child)
	}
	err := clients[C.GoString(id)].LinkGroup(utils.DecodeJidProto(&parentJID), utils.DecodeJidProto(&childJID))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")

}

//export SendChatPresence
func SendChatPresence(id *C.char, JIDByte *C.uchar, JIDSize C.int, state C.int, media C.int) *C.char {
	jidbyte := getByteByAddr(JIDByte, JIDSize)
	var neonize_jid neonize.JID
	err := proto.Unmarshal(jidbyte, &neonize_jid)
	if err != nil {
		panic(err)
	}
	err_status := clients[C.GoString(id)].SendChatPresence(
		utils.DecodeJidProto(&neonize_jid),
		utils.ChatPresence[int(state)],
		utils.ChatPresenceMedia[int(media)],
	)
	if err != nil {
		return C.CString(err_status.Error())
	}
	return C.CString("")
}

//export BuildRevoke
func BuildRevoke(id *C.char, ChatByte *C.uchar, ChatSize C.int, SenderByte *C.uchar, SenderSize C.int, messageID *C.char) C.struct_BytesReturn {
	chatByte := getByteByAddr(ChatByte, ChatSize)
	senderByte := getByteByAddr(SenderByte, SenderSize)
	var Chat neonize.JID
	var Sender neonize.JID
	err := proto.Unmarshal(chatByte, &Chat)

	if err != nil {
		panic(err)
	}
	err_ := proto.Unmarshal(senderByte, &Sender)
	if err_ != nil {
		panic(err_)
	}
	message := clients[C.GoString(id)].BuildRevoke(
		utils.DecodeJidProto(&Chat),
		utils.DecodeJidProto(&Sender),
		C.GoString(messageID),
	)
	messageByte, err_marshal := proto.Marshal(message)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(messageByte)
}

//export BuildPollVoteCreation
func BuildPollVoteCreation(id *C.char, name *C.char, options *C.uchar, optionsSize C.int, selectableOptionCount C.int) C.struct_BytesReturn {
	var options_proto neonize.ArrayString
	options_array := []string{}
	option_byte := getByteByAddr(options, optionsSize)
	err := proto.Unmarshal(option_byte, &options_proto)
	if err != nil {
		panic(err)
	}
	for _, option := range options_proto.Data {
		options_array = append(options_array, option)
	}
	msg := clients[C.GoString(id)].BuildPollCreation(C.GoString(name), options_array, int(selectableOptionCount))
	return_, err_marshal := proto.Marshal(msg)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_)
}

//export CreateNewsletter
func CreateNewsletter(id *C.char, createNewsletterParams *C.uchar, size C.int) C.struct_BytesReturn {
	var neonizeParams neonize.CreateNewsletterParams
	params_byte := getByteByAddr(createNewsletterParams, size)
	err := proto.Unmarshal(params_byte, &neonizeParams)
	if err != nil {
		panic(err)
	}
	return_ := neonize.CreateNewsLetterReturnFunction{}
	metadata, err_metadata := clients[C.GoString(id)].CreateNewsletter(utils.DecodeCreateNewsletterParams(&neonizeParams))
	if err_metadata != nil {
		return_.Error = proto.String(err_metadata.Error())
	}
	if metadata != nil {
		return_.NewsletterMetadata = utils.EncodeNewsLetterMessageMetadata(*metadata)
	}
	retrun_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(retrun_buf)
}

//export FollowNewsletter
func FollowNewsletter(id *C.char, jid *C.uchar, size C.int) *C.char {
	var JID neonize.JID
	jid_byte := getByteByAddr(jid, size)
	unmarshal_err := proto.Unmarshal(jid_byte, &JID)
	if unmarshal_err != nil {
		panic(unmarshal_err)
	}
	err := clients[C.GoString(id)].FollowNewsletter(utils.DecodeJidProto(&JID))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export GetNewsletterInfo
func GetNewsletterInfo(id *C.char, JIDByte *C.uchar, JIDSize C.int) C.struct_BytesReturn {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	metadata_proto := neonize.CreateNewsLetterReturnFunction{}
	metadata, err_metadata := clients[C.GoString(id)].GetNewsletterInfo(utils.DecodeJidProto(&JID))
	if metadata != nil {
		metadata_proto.NewsletterMetadata = utils.EncodeNewsLetterMessageMetadata(*metadata)
	}
	if err_metadata != nil {
		metadata_proto.Error = proto.String(err_metadata.Error())
	}
	return_, err_marshal := proto.Marshal(&metadata_proto)
	if err_marshal != nil {
		panic(err)
	}
	return ReturnBytes(return_)
}

//export GetNewsletterInfoWithInvite
func GetNewsletterInfoWithInvite(id *C.char, key *C.char) C.struct_BytesReturn {
	return_ := neonize.CreateNewsLetterReturnFunction{}
	metadata, err := clients[C.GoString(id)].GetNewsletterInfoWithInvite(C.GoString(key))
	if metadata != nil {
		return_.NewsletterMetadata = utils.EncodeNewsLetterMessageMetadata(*metadata)
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_buf, err := proto.Marshal(&return_)
	return ReturnBytes(return_buf)
}

//export GetNewsletterMessageUpdate
func GetNewsletterMessageUpdate(id *C.char, JIDByte *C.uchar, JIDSize C.int, Count C.int, Since C.int, After C.int) C.struct_BytesReturn {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	newsletterMessage, errnewsletter := clients[C.GoString(id)].GetNewsletterMessageUpdates(utils.DecodeJidProto(&JID), &whatsmeow.GetNewsletterUpdatesParams{
		Count: int(Count),
		Since: time.Unix(int64(Since), 0),
		After: int(After),
	})
	return_ := neonize.GetNewsletterMessageUpdateReturnFunction{}
	if errnewsletter != nil {
		return_.Error = proto.String(errnewsletter.Error())
	}
	NewsletterMessages := []*neonize.NewsletterMessage{}
	for _, msg := range newsletterMessage {
		NewsletterMessages = append(NewsletterMessages, utils.EncodeNewsletterMessage(msg))
	}
	if newsletterMessage != nil {
		return_.NewsletterMessage = NewsletterMessages
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)

}

//export GetNewsletterMessages
func GetNewsletterMessages(id *C.char, JIDByte *C.uchar, JIDSize C.int, Count C.int, Before C.int) C.struct_BytesReturn {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	newsletterMessage, errnewsletter := clients[C.GoString(id)].GetNewsletterMessages(utils.DecodeJidProto(&JID), &whatsmeow.GetNewsletterMessagesParams{
		Count:  int(Count),
		Before: int(Before),
	})
	return_ := neonize.GetNewsletterMessageUpdateReturnFunction{}
	if errnewsletter != nil {
		return_.Error = proto.String(errnewsletter.Error())
	}
	NewsletterMessages := []*neonize.NewsletterMessage{}
	for _, msg := range newsletterMessage {
		NewsletterMessages = append(NewsletterMessages, utils.EncodeNewsletterMessage(msg))
	}
	if newsletterMessage != nil {
		return_.NewsletterMessage = NewsletterMessages
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)

}

//export Logout
func Logout(id *C.char) *C.char {
	err := clients[C.GoString(id)].Logout()
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export MarkRead
func MarkRead(id *C.char, ids *C.char, timestamp C.int, chatByte *C.uchar, chatSize C.int, senderByte *C.uchar, senderSize C.int, receiptType *C.char) *C.char {
	var chatJID, senderJID neonize.JID
	chat_err := proto.Unmarshal(getByteByAddr(chatByte, chatSize), &chatJID)
	if chat_err != nil {
		panic(chat_err)
	}
	sender_err := proto.Unmarshal(getByteByAddr(senderByte, senderSize), &senderJID)
	if sender_err != nil {
		panic(sender_err)
	}
	err := clients[C.GoString(id)].MarkRead(strings.Split(C.GoString(ids), " "), time.Unix(int64(timestamp), 0), utils.DecodeJidProto(&chatJID), utils.DecodeJidProto(&senderJID), types.ReceiptType(C.GoString(receiptType)))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export NewsletterMarkViewed
func NewsletterMarkViewed(id *C.char, JIDByte *C.uchar, JIDSize C.int, MessageServerID *C.uchar, MessageServerIDSize C.int) *C.char {
	var JID neonize.JID
	var serverIDs = make([]int, int(MessageServerIDSize))
	for _, msid := range getByteByAddr(MessageServerID, MessageServerIDSize) {
		serverIDs = append(serverIDs, int(msid))
	}
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	err_return := clients[C.GoString(id)].NewsletterMarkViewed(utils.DecodeJidProto(&JID), serverIDs)
	if err_return != nil {
		return C.CString(err_return.Error())
	}
	return C.CString("")
}

//export  NewsletterSendReaction
func NewsletterSendReaction(id *C.char, JIDByte *C.uchar, JIDSize, messageServerID C.int, reaction *C.char, messageID *C.char) *C.char {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	err_react := clients[C.GoString(id)].NewsletterSendReaction(utils.DecodeJidProto(&JID), int(messageServerID), C.GoString(reaction), C.GoString(messageID))
	if err_react != nil {
		return C.CString(err_react.Error())
	}
	return C.CString(err_react.Error())
}

//export NewsletterSubscribeLiveUpdates
func NewsletterSubscribeLiveUpdates(id *C.char, JIDByte *C.uchar, JIDSize C.int) C.struct_BytesReturn {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	duration, err_subs := clients[C.GoString(id)].NewsletterSubscribeLiveUpdates(context.Background(), utils.DecodeJidProto(&JID))
	return_ := neonize.NewsletterSubscribeLiveUpdatesReturnFunction{
		Duration: proto.Int64(int64(duration)),
	}
	if err_subs != nil {
		return_.Error = proto.String(err_subs.Error())
	}
	return_buf, return_err := proto.Marshal(&return_)
	if return_err != nil {
		panic(return_err)
	}
	return ReturnBytes(return_buf)
}

//export NewsletterToggleMute
func NewsletterToggleMute(id *C.char, JIDByte *C.uchar, JIDSize C.int, mute C.bool) *C.char {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	err_togglemute := clients[C.GoString(id)].NewsletterToggleMute(utils.DecodeJidProto(&JID), bool(mute))
	if err_togglemute != nil {
		return C.CString(err_togglemute.Error())
	}
	return C.CString("")
}

//export ResolveBusinessMessageLink
func ResolveBusinessMessageLink(id *C.char, code *C.char) C.struct_BytesReturn {
	return_ := neonize.ResolveBusinessMessageLinkReturnFunction{}
	message_link, err := clients[C.GoString(id)].ResolveBusinessMessageLink(C.GoString(code))
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	if message_link != nil {
		return_.MessageLinkTarget = utils.EncodeBusinessMessageLinkTarget(*message_link)
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)
}

//export ResolveContactQRLink
func ResolveContactQRLink(id *C.char, code *C.char) C.struct_BytesReturn {
	return_ := neonize.ResolveContactQRLinkReturnFunction{}
	contact, err := clients[C.GoString(id)].ResolveContactQRLink(C.GoString(code))
	if contact != nil {
		return_.ContactQrLink = utils.EncodeContactQRLinkTarget(*contact)
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)
}

//export SendAppState
func SendAppState(id *C.char, patchByte *C.uchar, patchSize C.int) *C.char {
	var patchInfo neonize.PatchInfo
	err_unmarshal := proto.Unmarshal(getByteByAddr(patchByte, patchSize), &patchInfo)
	if err_unmarshal != nil {
		panic(err_unmarshal)
	}
	err := clients[C.GoString(id)].SendAppState(*utils.DecodePatchInfo(&patchInfo))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export SetDefaultDisappearingTimer
func SetDefaultDisappearingTimer(id *C.char, timer C.int64_t) *C.char {
	err := clients[C.GoString(id)].SetDefaultDisappearingTimer(time.Duration(int64(timer)))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export GetPrivacySettings
func GetPrivacySettings(id *C.char) C.struct_BytesReturn {
	settings := clients[C.GoString(id)].GetPrivacySettings()
	return_buf, err := proto.Marshal(utils.EncodePrivacySettings(settings))
	if err != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export GetProfilePicture
func GetProfilePicture(id *C.char, JIDByte *C.uchar, JIDSize C.int, paramsByte *C.uchar, paramsSize C.int) C.struct_BytesReturn {
	var neonizeJID neonize.JID
	var neonizeParams neonize.GetProfilePictureParams
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &neonizeJID)
	if err != nil {
		panic(err)
	}
	err_params := proto.Unmarshal(getByteByAddr(paramsByte, paramsSize), &neonizeParams)
	if err_params != nil {
		panic(err_params)
	}
	return_ := neonize.GetProfilePictureReturnFunction{}
	picture, err_pict := clients[C.GoString(id)].GetProfilePictureInfo(utils.DecodeJidProto(&neonizeJID), utils.DecodeGetProfilePictureParams(&neonizeParams))
	if err_params != nil {
		return_.Error = proto.String(err_pict.Error())
	}
	if picture != nil {
		return_.Picture = utils.EncodeProfilePictureInfo(*picture)
	}
	return_buf, err_buf := proto.Marshal(&return_)
	if err_buf != nil {
		panic(err_buf)
	}
	return ReturnBytes(return_buf)
}

//export GetStatusPrivacy
func GetStatusPrivacy(id *C.char) C.struct_BytesReturn {
	return_ := neonize.GetStatusPrivacyReturnFunction{}
	status_privacy_encoded := []*neonize.StatusPrivacy{}
	status_privacy, err := clients[C.GoString(id)].GetStatusPrivacy()
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	for _, privacy := range status_privacy {
		status_privacy_encoded = append(status_privacy_encoded, utils.EncodeStatusPrivacy(privacy))
	}
	return_.StatusPrivacy = status_privacy_encoded
	return_buf, err_buf := proto.Marshal(&return_)
	if err_buf != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export GetSubGroups
func GetSubGroups(id *C.char, JIDByte *C.uchar, JIDSize C.int) C.struct_BytesReturn {
	var JID neonize.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	groups := []*neonize.GroupLinkTarget{}
	return_ := neonize.GetSubGroupsReturnFunction{}
	linked_groups, group_err := clients[C.GoString(id)].GetSubGroups(utils.DecodeJidProto(&JID))
	if group_err != nil {
		return_.Error = proto.String(group_err.Error())
	}
	for _, group := range linked_groups {
		groups = append(groups, utils.EncodeGroupLinkTarget(*group))
	}
	return_.GroupLinkTarget = groups
	return_buf, err := proto.Marshal(&return_)
	return ReturnBytes(return_buf)
}

//export GetSubscribedNewsletters
func GetSubscribedNewsletters(id *C.char) C.struct_BytesReturn {
	return_ := neonize.GetSubscribedNewslettersReturnFunction{}
	newsletters_ := []*neonize.NewsletterMetadata{}
	newsletters, err_newsletter := clients[C.GoString(id)].GetSubscribedNewsletters()
	for _, newsletter := range newsletters {
		newsletters_ = append(newsletters_, utils.EncodeNewsLetterMessageMetadata(*newsletter))
	}
	return_.Newsletter = newsletters_
	if err_newsletter != nil {
		return_.Error = proto.String(err_newsletter.Error())
	}
	return_buf, err := proto.Marshal(&return_)
	if err != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export GetUserDevices
func GetUserDevices(id *C.char, JIDSByte *C.uchar, JIDSSize C.int) C.struct_BytesReturn {
	var JIDS neonize.JIDArray
	jids := []types.JID{}
	err := proto.Unmarshal(getByteByAddr(JIDSByte, JIDSSize), &JIDS)
	if err != nil {
		panic(err)
	}
	for _, jid := range JIDS.JIDS {
		jids = append(jids, utils.DecodeJidProto(jid))
	}
	return_ := neonize.GetUserDevicesreturnFunction{}
	jidstypes, err_jids := clients[C.GoString(id)].GetUserDevices(jids)
	neonizeJID := []*neonize.JID{}
	for _, jid := range jidstypes {
		neonizeJID = append(neonizeJID, utils.EncodeJidProto(jid))
	}
	return_.JID = neonizeJID
	if err_jids != nil {
		return_.Error = proto.String(err_jids.Error())
	}
	return_buf, err := proto.Marshal(&return_)
	if err != nil {
		panic(err)
	}
	return ReturnBytes(return_buf)
}

//export GetBlocklist
func GetBlocklist(id *C.char) C.struct_BytesReturn {
	blocklist, err := clients[C.GoString(id)].GetBlocklist()
	return_ := neonize.GetBlocklistReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	if blocklist != nil {
		return_.Blocklist = utils.EncodeBlocklist(blocklist)
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)
}

//export BuildPollVote
func BuildPollVote(id *C.char, pollInfo *C.uchar, pollInfoSize C.int, optionName *C.uchar, optionNameSize C.int) C.struct_BytesReturn {
	var msgInfo neonize.MessageInfo
	var optionNames neonize.ArrayString
	err := proto.Unmarshal(getByteByAddr(pollInfo, pollInfoSize), &msgInfo)
	if err != nil {
		panic(err)
	}
	err_2 := proto.Unmarshal(getByteByAddr(optionName, optionNameSize), &optionNames)
	if err_2 != nil {
		panic(err_2)
	}
	optionsname := []string{}
	for _, option := range optionNames.Data {
		optionsname = append(optionsname, option)
	}
	pollInfo_, err_poll := clients[C.GoString(id)].BuildPollVote(utils.DecodeMessageInfo(&msgInfo), optionsname)
	return_ := neonize.BuildPollVoteReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err_poll.Error())
	}
	if pollInfo_ != nil {
		return_.PollVote = utils.EncodeMessage(pollInfo_)
	}
	return_buf, err_decode := proto.Marshal(&return_)
	if err_decode != nil {
		panic(err_decode)
	}
	return ReturnBytes(return_buf)
}

//export BuildReaction
func BuildReaction(id *C.char, chat *C.uchar, chatSize C.int, sender *C.uchar, senderSize C.int, messageID *C.char, reaction *C.char) C.struct_BytesReturn {
	var Chat neonize.JID
	var Sender neonize.JID
	chat_err := proto.Unmarshal(getByteByAddr(chat, chatSize), &Chat)
	if chat_err != nil {
		panic(chat_err)
	}
	sender_err := proto.Unmarshal(getByteByAddr(sender, senderSize), &Sender)
	if sender_err != nil {
		panic(sender_err)
	}
	msg := clients[C.GoString(id)].BuildReaction(
		utils.DecodeJidProto(&Chat),
		utils.DecodeJidProto(&Sender),
		C.GoString(messageID),
		C.GoString(reaction),
	)
	return_, err := proto.Marshal(msg)
	if err != nil {
		panic(err)
	}
	return ReturnBytes(return_)
}

//export CreateGroup
func CreateGroup(id *C.char, createGroupByte *C.uchar, createGroupSize C.int) C.struct_BytesReturn {
	creategrupbyte := getByteByAddr(createGroupByte, createGroupSize)
	var reqCreateGroup neonize.ReqCreateGroup
	err := proto.Unmarshal(creategrupbyte, &reqCreateGroup)
	if err != nil {
		panic(err)
	}
	group_info, err_ := clients[C.GoString(id)].CreateGroup(utils.DecodeReqCreateGroup(&reqCreateGroup))
	return_ := neonize.GetGroupInfoReturnFunction{}
	if group_info != nil {
		return_.GroupInfo = utils.EncodeGroupInfo(group_info)
	}
	if err_ != nil {
		return_.Error = proto.String(err.Error())
	}
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)
}

//export GetJoinedGroups
func GetJoinedGroups(id *C.char) C.struct_BytesReturn {
	neonize_groups_info := []*neonize.GroupInfo{}
	joined_groups, err := clients[C.GoString(id)].GetJoinedGroups()
	return_ := neonize.GetJoinedGroupsReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	for _, group_info := range joined_groups {
		neonize_groups_info = append(neonize_groups_info, utils.EncodeGroupInfo(group_info))
	}
	return_.Group = neonize_groups_info
	return_buf, err_marshal := proto.Marshal(&return_)
	if err_marshal != nil {
		panic(err_marshal)
	}
	return ReturnBytes(return_buf)

}

//export GetMe
func GetMe(id *C.char) C.struct_BytesReturn {
	cli := clients[C.GoString(id)].Store
	device := neonize.Device{
		PushName:      &cli.PushName,
		Platform:      &cli.Platform,
		BussinessName: &cli.BusinessName,
		Initialized:   &cli.Initialized,
	}
	if cli.ID != nil {
		device.JID = utils.EncodeJidProto(*cli.ID)
	}
	DeviceBuf, err := proto.Marshal(&device)
	if err != nil {
		panic(DeviceBuf)
	}
	return ReturnBytes(DeviceBuf)
}

//export GetContactQRLink
func GetContactQRLink(id *C.char, revoke C.bool) C.struct_BytesReturn {
	link, err := clients[C.GoString(id)].GetContactQRLink(bool(revoke))
	QRLinkReturn := neonize.GetContactQRLinkReturnFunction{
		Link: &link,
	}
	if err != nil {
		QRLinkReturn.Error = proto.String(err.Error())
	}
	return_, err_masrhal := proto.Marshal(&QRLinkReturn)
	if err_masrhal != nil {
		panic(err_masrhal)
	}
	return ReturnBytes(return_)
}

///

func main() {

}
