package main

/*

   #include <stdlib.h>
   #include <stdbool.h>
   #include <stdint.h>
   #include <string.h>
   #include "header/cstruct.h"
   #include "python/pythonptr.h"
*/
import "C"
import (
	"context"
	// "crypto/sha256"
	// "encoding/hex"
	"fmt"
	"strings"
	"time"
	"unsafe"

	"github.com/krypton-byte/neonize/defproto"
	"github.com/krypton-byte/neonize/utils"
	_ "github.com/mattn/go-sqlite3"
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/proto/waCompanionReg"
	"go.mau.fi/whatsmeow/proto/waConsumerApplication"
	waE2E "go.mau.fi/whatsmeow/proto/waE2E"
	"go.mau.fi/whatsmeow/proto/waMsgApplication"
	"go.mau.fi/whatsmeow/store"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"

	_ "github.com/lib/pq"

	waLog "go.mau.fi/whatsmeow/util/log"
	"google.golang.org/protobuf/proto"
)

var clients = make(map[string]*whatsmeow.Client)

type MessageEvent struct {
	eventType int
	message   proto.Message
}

var eventChannel map[string]chan *MessageEvent = make(map[string]chan *MessageEvent)
var StopSignal map[string]context.CancelFunc = make(map[string]context.CancelFunc)

// Defaults to sqlite otherwise use postgres database url
func getDB(db *C.char, dbLog waLog.Logger) (*sqlstore.Container, error) {
	container, err := sqlstore.New(context.TODO(), "sqlite3", fmt.Sprintf("file:%s?_foreign_keys=on", C.GoString(db)), dbLog)
	if strings.HasPrefix(C.GoString(db), "postgres") {
		container, err = sqlstore.New(context.TODO(), "postgres", C.GoString(db), dbLog)
	}
	return container, err
}

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

//export GetPNFromLID
func GetPNFromLID(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var neoJIDProto defproto.JID
	jidbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(jidbyte, &neoJIDProto)
	if err != nil {
		panic(err)
	}
	lid := utils.DecodeJidProto(&neoJIDProto)
	cli := clients[C.GoString(id)].Store
	pn, err := cli.LIDs.GetPNForLID(context.Background(), lid)

	neojid := utils.EncodeJidProto(pn)

	return_ := defproto.GetJIDFromStoreReturnFunction{
		Jid: neojid,
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}

	return ProtoReturnV3(&return_)
}
//export GetLIDFromPN
func GetLIDFromPN(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var neoJIDProto defproto.JID
	jidbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(jidbyte, &neoJIDProto)
	if err != nil {
		panic(err)
	}
	pn := utils.DecodeJidProto(&neoJIDProto)
	cli := clients[C.GoString(id)].Store
	lid, err := cli.LIDs.GetLIDForPN(context.Background(), pn)

	neojid := utils.EncodeJidProto(lid)

	return_ := defproto.GetJIDFromStoreReturnFunction{
		Jid: neojid,
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}

	return ProtoReturnV3(&return_)
}


func ReturnBytes(data []byte) C.struct_BytesReturn {
	size := C.size_t(len(data))
	ptr := (*C.char)(C.CBytes(data))
	// defer C.free(unsafe.Pointer(&ptr))
	return C.struct_BytesReturn{ptr, size}
}

func ReturnBytesV2(data []byte) *C.struct_BytesReturn {
	size := C.size_t(len(data))
	ptr := (*C.char)(C.CBytes(data))
	// defer C.free(unsafe.Pointer(&ptr))
	return &C.struct_BytesReturn{ptr, size}
}

func ProtoReturn(data proto.Message) C.struct_BytesReturn {
	data_buf, err := proto.Marshal(data)
	if err != nil {
		panic(err)
	}
	return ReturnBytes(data_buf)
}
func ProtoReturnV2(data proto.Message) *C.struct_BytesReturn {
	data_buf, err := proto.Marshal(data)
	if err != nil {
		panic(err)
	}
	return ReturnBytesV2(data_buf)
}
func ProtoReturnV3(data proto.Message) *C.struct_BytesReturn {
	data_buf, err := proto.Marshal(data)
	if err != nil {
		panic(err)
	}
	result := (*C.struct_BytesReturn)(C.malloc(C.size_t(unsafe.Sizeof(C.struct_BytesReturn{}))))
	result.size = C.size_t(len(data_buf))
	result.data = (*C.char)(C.malloc(result.size))
	C.memcpy(unsafe.Pointer(result.data), unsafe.Pointer(&data_buf[0]), result.size)
	return result
}
func getBytesAndSize(data []byte) (*C.char, C.size_t) {
	messageSourceCDATA := (*C.char)(unsafe.Pointer(&data[0]))
	messageSourceCSize := C.size_t(len(data))
	return messageSourceCDATA, messageSourceCSize
}

//export Upload
func Upload(id *C.char, mediabuff *C.uchar, mediaSize C.int, mediatype C.int) *C.struct_BytesReturn {
	client := clients[C.GoString(id)]
	data := getByteByAddr(mediabuff, mediaSize)
	response, err_upload := client.Upload(context.Background(), data, utils.MediaType[int(mediatype)])
	return_ := defproto.UploadReturnFunction{}
	if err_upload != nil {
		return_.Error = proto.String(err_upload.Error())
	}
	return_.UploadResponse = utils.EncodeUploadResponse(response)
	return ProtoReturnV3(&return_)
}

//export UploadNewsletter
func UploadNewsletter(id *C.char, data *C.uchar, dataSize C.int, appInfo C.int) *C.struct_BytesReturn {
	return_ := defproto.UploadReturnFunction{}
	upload, err := clients[C.GoString(id)].UploadNewsletter(context.Background(), getByteByAddr(data, dataSize), utils.MediaType[int(appInfo)])
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_.UploadResponse = utils.EncodeUploadResponse(upload)
	return ProtoReturnV3(&return_)
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

//export TestStruct
func TestStruct() *C.struct_BytesReturn {
	data := defproto.SendRequestExtra{
		ID: proto.String("test-id"),
		InlineBotJID: &defproto.JID{
			User:       proto.String("test-user"),
			Server:     proto.String("test-server"),
			RawAgent:   proto.Uint32(0),
			Device:     proto.Uint32(0),
			Integrator: proto.Uint32(0),
			IsEmpty:    proto.Bool(false),
		},
		Peer:        proto.Bool(true),
		Timeout:     proto.Int64(99999999),
		MediaHandle: proto.String("test-media-handle"),
	}
	return ProtoReturnV3(&data)
}

//export SendMessage
func SendMessage(id *C.char, JIDByte *C.uchar, JIDSize C.int, messageByte *C.uchar, messageSize C.int) *C.struct_BytesReturn {
	// fmt.Println("SendMessage: Getting client from ID")
	client := clients[C.GoString(id)]
	// fmt.Println("SendMessage: Getting JID byte array")
	jid := getByteByAddr(JIDByte, JIDSize)
	// fmt.Println("SendMessage: Creating neonize_jid variable")
	var neonize_jid defproto.JID
	// fmt.Println("SendMessage: Creating return object")
	return_ := defproto.SendMessageReturnFunction{}
	// fmt.Println("SendMessage: Unmarshaling JID")
	err := proto.Unmarshal(jid, &neonize_jid)
	if err != nil {
		fmt.Println("SendMessage: Error unmarshaling JID:", err.Error())
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	// fmt.Println("SendMessage: Getting message byte array")
	message_bytes := getByteByAddr(messageByte, messageSize)
	// fmt.Println("SendMessage: Creating message variable")
	var message waE2E.Message
	// fmt.Println("SendMessage: Unmarshaling message")
	err_message := proto.Unmarshal(message_bytes, &message)
	if err_message != nil {
		fmt.Println("SendMessage: Error unmarshaling message:", err_message.Error())
		return_.Error = proto.String(err_message.Error())
		return ProtoReturnV3(&return_)
	}
	// fmt.Println("SendMessage: Sending message to WhatsApp")
	sendresponse, err := client.SendMessage(context.Background(), utils.DecodeJidProto(&neonize_jid), &message)
	if err != nil {
		fmt.Println("SendMessage: Error sending message:", err.Error())
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	// fmt.Println("SendMessage: Encoding send response")
	return_.SendResponse = utils.EncodeSendResponse(sendresponse)
	// buff, err := proto.Marshal(&return_)
	// if err != nil {
	// 	panic(err)
	// }
	// hashx := sha256.Sum256(buff)
	// hashl := hex.EncodeToString(hashx[:]) // This is just to ensure the data is not empty
	// fmt.Printf("Marshaled data (%d bytes): %x\thash: %s\n", len(buff), buff, hashl)
	// fmt.Println("SendMessage: Returning proto response")
	// result := ProtoReturnV3(&return_)
	// fmt.Println("size of result:", int(result.size))
	return ProtoReturnV3(&return_)
}

//export StopAll
func StopAll() {
	for key := range clients {
		Stop(C.CString(key))
	}
}

//export Stop
func Stop(id *C.char) {
	waLog.Noop.Infof("Stopping client with ID:", C.GoString(id))
	if client, exists := clients[C.GoString(id)]; exists {
		client.Disconnect()
		delete(clients, C.GoString(id))
	}
	if cancelFunc, exists := StopSignal[C.GoString(id)]; exists {
		cancelFunc()
		delete(StopSignal, C.GoString(id))
	}
	if eventChan, exists := eventChannel[C.GoString(id)]; exists {
		close(eventChan)
		delete(eventChannel, C.GoString(id))
	}
}

//export Neonize
func Neonize(db *C.char, id *C.char, JIDByte *C.uchar, JIDSize C.int, logLevel *C.char, qrCb C.ptr_to_python_function_string, logStatus C.ptr_to_python_function_string, event C.ptr_to_python_function_bytes, subscribes *C.uchar, lenSubscriber C.int, devicePropsBuf *C.uchar, devicePropsSize C.int, pairphone *C.uchar, pairphoneSize C.int) { // ,
	subscribers := map[int]bool{}
	var deviceProps waCompanionReg.DeviceProps
	var loginStateChan = make(chan bool)
	err_proto := proto.Unmarshal(getByteByAddr(devicePropsBuf, devicePropsSize), &deviceProps)
	ctx, cancel := context.WithCancel(context.Background())
	StopSignal[C.GoString(id)] = cancel
	if err_proto != nil {
		panic(err_proto)
	}
	for _, s := range getByteByAddr(subscribes, lenSubscriber) {
		subscribers[int(s)] = true
	}
	dbLog := waLog.Stdout("Database", C.GoString(logLevel), true)
	// Make sure you add appropriate DB connector imports, e.g. github.com/mattn/go-sqlite3 for SQLite
	container, err := getDB(db, dbLog)
	uuid := C.GoString(id)
	eventChan := make(chan *MessageEvent, 100)
	eventChannel[uuid] = eventChan
	if err != nil {
		panic(err)
	}
	// If you want multiple sessions, remember their JIDs and use .GetDevice(jid) or .GetAllDevices() instead.
	var deviceStore *store.Device
	var err_device error
	var JID defproto.JID
	if int(JIDSize) > 0 {
		jidbyte_err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
		if jidbyte_err != nil {
			panic(jidbyte_err)
		}
		deviceStore, err_device = container.GetDevice(context.TODO(), utils.DecodeJidProto(&JID))
	} else {
		deviceStore, err_device = container.GetFirstDevice(context.TODO())
	}
	if err_device != nil {
		panic(err_device)
	}
	proto.Merge(store.DeviceProps, &deviceProps)
	clientLog := waLog.Stdout("Client", C.GoString(logLevel), true)
	client := whatsmeow.NewClient(deviceStore, clientLog)
	clients[uuid] = client
	eventHandler := func(evt interface{}) {
		switch v := evt.(type) {
		case *events.QR:
			if _, ok := subscribers[1]; ok {
				qr := defproto.QR{
					Codes: v.Codes,
				}
				messageEvent := MessageEvent{
					eventType: 1,
					message:   &qr,
				}
				eventChan <- &messageEvent
			}
		case *events.PairError:
			if _, ok := subscribers[2]; ok {
				pair := utils.EncodePairError(v)
				messageEvent := MessageEvent{
					eventType: 2,
					message:   pair,
				}
				eventChan <- &messageEvent
			}
		case *events.PairSuccess:
			if _, ok := subscribers[2]; ok {
				pair := utils.EncodePairSuccess(v)
				messageEvent := MessageEvent{
					eventType: 2,
					message:   pair,
				}
				eventChan <- &messageEvent
			}
		case *events.Connected:
			if int(pairphoneSize) > 0 && client.Store.ID == nil {
				loginStateChan <- true
			}
			if _, ok := subscribers[3]; ok {
				connected := defproto.Connected{Status: proto.Bool(true)}
				messageEvent := MessageEvent{
					eventType: 3,
					message:   &connected,
				}
				eventChan <- &messageEvent
			}
		case *events.KeepAliveTimeout:
			if _, ok := subscribers[4]; ok {
				timeout := defproto.KeepAliveTimeout{
					ErrorCount:  proto.Int64(int64(v.ErrorCount)),
					LastSuccess: proto.Int64(v.LastSuccess.Unix()),
				}
				messageEvent := MessageEvent{
					eventType: 4,
					message:   &timeout,
				}
				eventChan <- &messageEvent
			}
		case *events.KeepAliveRestored:
			if _, ok := subscribers[5]; ok {
				restored := defproto.KeepAliveRestored{}
				messageEvent := MessageEvent{
					eventType: 5,
					message:   &restored,
				}
				eventChan <- &messageEvent
			}
		case *events.LoggedOut:
			if _, ok := subscribers[6]; ok {
				logout := utils.EncodeLoggedOut(v)
				messageEvent := MessageEvent{
					eventType: 6,
					message:   logout,
				}
				eventChan <- &messageEvent
			}
		case *events.StreamReplaced:
			if _, ok := subscribers[7]; ok {
				stream := defproto.StreamReplaced{}
				messageEvent := MessageEvent{
					eventType: 7,
					message:   &stream,
				}
				eventChan <- &messageEvent
			}
		case *events.TemporaryBan:
			if _, ok := subscribers[8]; ok {
				ban := utils.EncodeTemporaryBan(v)
				messageEvent := MessageEvent{
					eventType: 8,
					message:   ban,
				}
				eventChan <- &messageEvent
			}
		case *events.ConnectFailure:
			if _, ok := subscribers[9]; ok {
				failure := utils.EncodeConnectFailure(v)
				messageEvent := MessageEvent{
					eventType: 9,
					message:   failure,
				}
				eventChan <- &messageEvent
			}
		case *events.ClientOutdated:
			if _, ok := subscribers[10]; ok {
				outdated := defproto.ClientOutdated{}
				messageEvent := MessageEvent{
					eventType: 10,
					message:   &outdated,
				}
				eventChan <- &messageEvent
			}
		case *events.StreamError:
			if _, ok := subscribers[11]; ok {
				stream_error := defproto.StreamError{
					Code: &v.Code,
					Raw:  utils.EncodeNode(v.Raw),
				}
				messageEvent := MessageEvent{
					eventType: 11,
					message:   &stream_error,
				}
				eventChan <- &messageEvent
			}
		case *events.Disconnected:
			if _, ok := subscribers[12]; ok {
				disconnect := defproto.Disconnected{
					Status: proto.Bool(true),
				}
				messageEvent := MessageEvent{
					eventType: 12,
					message:   &disconnect,
				}
				eventChan <- &messageEvent
			}
		case *events.HistorySync:
			if _, ok := subscribers[13]; ok {
				data := defproto.HistorySync{
					Data: v.Data,
				}
				messageEvent := MessageEvent{
					eventType: 13,
					message:   &data,
				}
				eventChan <- &messageEvent
			}
		case *events.Message:
			if _, ok := subscribers[17]; ok {
				messageSource := utils.EncodeEventTypesMessage(v)
				messageEvent := MessageEvent{
					eventType: 17,
					message:   messageSource,
				}
				eventChan <- &messageEvent
			}
		case *events.Receipt:
			if _, ok := subscribers[18]; ok {
				receipt := utils.EncodeReceipts(v)
				messageEvent := MessageEvent{
					eventType: 18,
					message:   &receipt,
				}
				eventChan <- &messageEvent
			}
		case *events.ChatPresence:
			if _, ok := subscribers[19]; ok {
				presence := utils.EncodeChatPresence(v)
				messageEvent := MessageEvent{
					eventType: 19,
					message:   &presence,
				}
				eventChan <- &messageEvent
			}
		case *events.Presence:
			if _, ok := subscribers[20]; ok {
				presence := utils.EncodePresence(v)
				messageEvent := MessageEvent{
					eventType: 20,
					message:   &presence,
				}
				eventChan <- &messageEvent
			}
		case *events.JoinedGroup:
			if _, ok := subscribers[21]; ok {
				joined := utils.EncodeJoinedGroup(v)
				messageEvent := MessageEvent{
					eventType: 21,
					message:   &joined,
				}
				eventChan <- &messageEvent
			}
		case *events.GroupInfo:
			if _, ok := subscribers[22]; ok {
				groupinfo := utils.EncodeGroupInfoEvent(v)
				messageEvent := MessageEvent{
					eventType: 22,
					message:   groupinfo,
				}
				eventChan <- &messageEvent
			}
		case *events.Picture:
			if _, ok := subscribers[23]; ok {
				picture := defproto.Picture{
					JID:       utils.EncodeJidProto(v.JID),
					Author:    utils.EncodeJidProto(v.Author),
					Timestamp: proto.Int64(v.Timestamp.Unix()),
					Remove:    &v.Remove,
				}
				messageEvent := MessageEvent{
					eventType: 23,
					message:   &picture,
				}
				eventChan <- &messageEvent
			}
		case *events.IdentityChange:
			if _, ok := subscribers[24]; ok {
				identity := defproto.IdentityChange{
					JID:       utils.EncodeJidProto(v.JID),
					Timestamp: proto.Int64(v.Timestamp.Unix()),
					Implicit:  &v.Implicit,
				}
				messageEvent := MessageEvent{
					eventType: 24,
					message:   &identity,
				}
				eventChan <- &messageEvent
			}
		case *events.PrivacySettings:
			if _, ok := subscribers[25]; ok {
				privacy_event := defproto.PrivacySettingsEvent{
					NewSettings:         utils.EncodePrivacySettings(v.NewSettings),
					GroupAddChanged:     &v.GroupAddChanged,
					LastSeenChanged:     &v.LastSeenChanged,
					StatusChanged:       &v.StatusChanged,
					ProfileChanged:      &v.ProfileChanged,
					ReadReceiptsChanged: &v.ReadReceiptsChanged,
					OnlineChanged:       &v.OnlineChanged,
					CallAddChanged:      &v.CallAddChanged,
				}
				messageEvent := MessageEvent{
					eventType: 25,
					message:   &privacy_event,
				}
				eventChan <- &messageEvent
			}
		case *events.OfflineSyncPreview:
			if _, ok := subscribers[26]; ok {
				sync := defproto.OfflineSyncPreview{
					Total:          proto.Int32(int32(v.Total)),
					AppDataChanges: proto.Int32(int32(v.AppDataChanges)),
					Message:        proto.Int32(int32(v.Messages)),
					Notifications:  proto.Int32(int32(v.Notifications)),
					Receipts:       proto.Int32(int32(v.Receipts)),
				}
				messageEvent := MessageEvent{
					eventType: 26,
					message:   &sync,
				}
				eventChan <- &messageEvent
			}
		case *events.OfflineSyncCompleted:
			if _, ok := subscribers[27]; ok {
				sync := defproto.OfflineSyncCompleted{
					Count: proto.Int32(int32(v.Count)),
				}
				messageEvent := MessageEvent{
					eventType: 27,
					message:   &sync,
				}
				eventChan <- &messageEvent
			}
		case *events.Blocklist:
			if _, ok := subscribers[30]; ok {
				blocklist := utils.EncodeBlocklistEvent(v)
				messageEvent := MessageEvent{
					eventType: 30,
					message:   &blocklist,
				}
				eventChan <- &messageEvent
			}
		case *events.BlocklistChange:
			if _, ok := subscribers[31]; ok {
				block := utils.EncodeBlocklistChange(v)
				messageEvent := MessageEvent{
					eventType: 31,
					message:   block,
				}
				eventChan <- &messageEvent
			}
		case *events.NewsletterJoin:
			if _, ok := subscribers[32]; ok {
				newsletter := defproto.NewsletterJoin{
					NewsletterMetadata: utils.EncodeNewsLetterMessageMetadata(v.NewsletterMetadata),
				}
				messageEvent := MessageEvent{
					eventType: 32,
					message:   &newsletter,
				}
				eventChan <- &messageEvent
			}
		case *events.NewsletterLeave:
			if _, ok := subscribers[33]; ok {
				leave := utils.EncodeNewsletterLeave(v)
				messageEvent := MessageEvent{
					eventType: 33,
					message:   &leave,
				}
				eventChan <- &messageEvent
			}
		case *events.NewsletterMuteChange:
			if _, ok := subscribers[34]; ok {
				mute := utils.EncodeNewsletterMuteChange(v)
				messageEvent := MessageEvent{
					eventType: 34,
					message:   &mute,
				}
				eventChan <- &messageEvent
			}
		case *events.NewsletterLiveUpdate:
			if _, ok := subscribers[35]; ok {
				update := utils.EncodeNewsletterLiveUpdate(v)
				messageEvent := MessageEvent{
					eventType: 35,
					message:   &update,
				}
				eventChan <- &messageEvent
			}
		case *events.CallOffer:
			if _, ok := subscribers[36]; ok {
				callOffer := defproto.CallOffer{
					BasicCallMeta:  utils.EncodeBasicCallMeta(v.BasicCallMeta),
					CallRemoteMeta: utils.EncodeCallRemoteMeta(v.CallRemoteMeta),
					Data:           utils.EncodeNode(v.Data),
				}
				messageEvent := MessageEvent{
					eventType: 36,
					message:   &callOffer,
				}
				eventChan <- &messageEvent
			}
		case *events.CallAccept:
			if _, ok := subscribers[37]; ok {
				callAccept := defproto.CallAccept{
					BasicCallMeta:  utils.EncodeBasicCallMeta(v.BasicCallMeta),
					CallRemoteMeta: utils.EncodeCallRemoteMeta(v.CallRemoteMeta),
					Data:           utils.EncodeNode(v.Data),
				}
				messageEvent := MessageEvent{
					eventType: 37,
					message:   &callAccept,
				}
				eventChan <- &messageEvent
			}
		case *events.CallPreAccept:
			if _, ok := subscribers[38]; ok {
				callPreAccept := defproto.CallPreAccept{
					BasicCallMeta:  utils.EncodeBasicCallMeta(v.BasicCallMeta),
					CallRemoteMeta: utils.EncodeCallRemoteMeta(v.CallRemoteMeta),
					Data:           utils.EncodeNode(v.Data),
				}
				messageEvent := MessageEvent{
					eventType: 38,
					message:   &callPreAccept,
				}
				eventChan <- &messageEvent
			}
		case *events.CallTransport:
			if _, ok := subscribers[39]; ok {
				callTransport := defproto.CallTransport{
					BasicCallMeta:  utils.EncodeBasicCallMeta(v.BasicCallMeta),
					CallRemoteMeta: utils.EncodeCallRemoteMeta(v.CallRemoteMeta),
					Data:           utils.EncodeNode(v.Data),
				}
				messageEvent := MessageEvent{
					eventType: 39,
					message:   &callTransport,
				}
				eventChan <- &messageEvent
			}
		case *events.CallOfferNotice:
			if _, ok := subscribers[40]; ok {
				callOfferNotice := defproto.CallOfferNotice{
					BasicCallMeta: utils.EncodeBasicCallMeta(v.BasicCallMeta),
					Media:         proto.String(v.Media),
					Type:          proto.String(v.Type),
					Data:          utils.EncodeNode(v.Data),
				}
				messageEvent := MessageEvent{
					eventType: 40,
					message:   &callOfferNotice,
				}
				eventChan <- &messageEvent
			}
		case *events.CallRelayLatency:
			if _, ok := subscribers[41]; ok {
				callRelayLatency := defproto.CallRelayLatency{
					BasicCallMeta: utils.EncodeBasicCallMeta(v.BasicCallMeta),
					Data:          utils.EncodeNode(v.Data),
				}
				messageEvent := MessageEvent{
					eventType: 41,
					message:   &callRelayLatency,
				}
				eventChan <- &messageEvent
			}
		case *events.CallTerminate:
			if _, ok := subscribers[42]; ok {
				callTerminate := defproto.CallTerminate{
					BasicCallMeta: utils.EncodeBasicCallMeta(v.BasicCallMeta),
					Reason:        proto.String(v.Reason),
					Data:          utils.EncodeNode(v.Data),
				}
				messageEvent := MessageEvent{
					eventType: 42,
					message:   &callTerminate,
				}
				eventChan <- &messageEvent
			}
		case *events.UnknownCallEvent:
			if _, ok := subscribers[43]; ok {
				unknownCall := defproto.UnknownCallEvent{
					Node: utils.EncodeNode(v.Node),
				}
				messageEvent := MessageEvent{
					eventType: 43,
					message:   &unknownCall,
				}
				eventChan <- &messageEvent
			}
		case *events.UndecryptableMessage:
			if _, ok := subscribers[44]; ok {
				undecryptableMessage := utils.EncodeUndecryptableMessageEvent(*v)
				messageEvent := MessageEvent{
					eventType: 44,
					message:   undecryptableMessage,
				}
				eventChan <- &messageEvent
			}
		}

		// C.free(unsafe.Pointer(CData))
	}
	client.AddEventHandler(eventHandler)
	qrFuncCb := func(data string) {
		cstr := C.CString(data)
		defer C.free(unsafe.Pointer(cstr))
		C.call_c_func_string(qrCb, C.CString(uuid), cstr)
	}
	logStatusCb := func(eventName string) {
		cstr := C.CString(eventName)
		defer C.free(unsafe.Pointer(cstr))
		C.call_c_func_string(logStatus, C.CString(uuid), cstr)
	}
	if client.Store.ID == nil {
		// No ID stored, new login
		if int(pairphoneSize) > 0 {
			phone_number := getByteByAddr(pairphone, pairphoneSize)
			var PairPhone defproto.PairPhoneParams
			err_pairparams := proto.Unmarshal(phone_number, &PairPhone)
			if err_pairparams != nil {
				panic(err_pairparams)
			}
			phone := *PairPhone.Phone
			notif := *PairPhone.ShowPushNotification
			displayname := *PairPhone.ClientDisplayName
			clientType := *PairPhone.ClientType
			client.Connect()
			code_, code_err := client.PairPhone(context.Background(), phone, notif, whatsmeow.PairClientType(int(clientType)), displayname)
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
					qrFuncCb(evt.Code)
					// C.free(unsafe.Pointer(cstr))
				} else {
					fmt.Println("Login event:", evt.Event)
					logStatusCb(evt.Event)
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
	println("Press Ctrl+C to exit")
	CallbackFunction(ctx, event, uuid)
}

//export Disconnect
func Disconnect(id *C.char) {
	clients[C.GoString(id)].Disconnect()
}

//export DownloadAny
func DownloadAny(id *C.char, messageProto *C.uchar, size C.int) *C.struct_BytesReturn {
	var message waE2E.Message
	return_ := defproto.DownloadReturnFunction{}
	err := proto.Unmarshal(getByteByAddr(messageProto, size), &message)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	data_buff, err := clients[C.GoString(id)].DownloadAny(context.Background(), &message)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	if data_buff != nil {
		return_.Binary = data_buff
	}
	return ProtoReturnV3(&return_)
}

//export DownloadMediaWithPath
func DownloadMediaWithPath(id *C.char, directPath *C.char, encFileHash *C.uchar, encFileHashSize C.int, fileHash *C.uchar, fileHashSize C.int, mediakey *C.uchar, mediaKeySize C.int, fileLength C.int, mediaType C.int, mmsType *C.char) *C.struct_BytesReturn {
	data_buff, err := clients[C.GoString(id)].DownloadMediaWithPath(context.Background(), C.GoString(directPath), getByteByAddr(encFileHash, encFileHashSize), getByteByAddr(fileHash, fileHashSize), getByteByAddr(mediakey, mediaKeySize), int(fileLength), utils.MediaType[mediaType], C.GoString(mmsType))
	return_ := defproto.DownloadReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	if data_buff != nil {
		return_.Binary = data_buff
	}
	return ProtoReturnV3(&return_)
}

//export IsOnWhatsApp
func IsOnWhatsApp(id *C.char, numbers *C.char) *C.struct_BytesReturn {
	onWhatsApp := []*defproto.IsOnWhatsAppResponse{}
	return_ := defproto.IsOnWhatsAppReturnFunction{}
	response, err := clients[C.GoString(id)].IsOnWhatsApp(strings.Split(C.GoString(numbers), " "))
	for _, participant := range response {
		onWhatsApp = append(onWhatsApp, utils.EncodeIsOnWhatsApp(participant))
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	return_.IsOnWhatsAppResponse = onWhatsApp
	return ProtoReturnV3(&return_)
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
func GetUserInfo(id *C.char, JIDSByte *C.uchar, JIDSSize C.int) *C.struct_BytesReturn {
	var NeoJIDS defproto.JIDArray
	JIDSBuf := getByteByAddr(JIDSByte, JIDSSize)
	err := proto.Unmarshal(JIDSBuf, &NeoJIDS)
	return_ := defproto.GetUserInfoReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	JIDS := []types.JID{}
	for _, jid := range NeoJIDS.JIDS {
		JIDS = append(JIDS, utils.DecodeJidProto(jid))
	}
	user_info, err := clients[C.GoString(id)].GetUserInfo(JIDS)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	usersinfo := []*defproto.GetUserInfoSingleReturnFunction{}
	for jid, info := range user_info {
		singlereturn := &defproto.GetUserInfoSingleReturnFunction{
			JID:      utils.EncodeJidProto(jid),
			UserInfo: utils.EncodeUserInfo(info),
		}

		usersinfo = append(usersinfo, singlereturn)
	}
	return_.UsersInfo = usersinfo
	return ProtoReturnV3(&return_)
}

// /GROUP
//
//export GetGroupInfo
func GetGroupInfo(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var neoJIDProto defproto.JID
	jidbyte := getByteByAddr(JIDByte, JIDSize)
	groupinfo := defproto.GetGroupInfoReturnFunction{}
	err := proto.Unmarshal(jidbyte, &neoJIDProto)
	if err != nil {
		groupinfo.Error = proto.String(err.Error())
		return ProtoReturnV3(&groupinfo)
	}
	decodeJid := utils.DecodeJidProto(&neoJIDProto)
	info, err_info := clients[C.GoString(id)].GetGroupInfo(decodeJid)
	if err_info != nil {
		groupinfo.Error = proto.String(err_info.Error())
		return ProtoReturnV3(&groupinfo)
	}
	if info != nil {
		groupinfo.GroupInfo = utils.EncodeGroupInfo(info)
		return ProtoReturnV3(&groupinfo)
	}
	return ProtoReturnV3(&groupinfo)
}

//export GetGroupInfoFromInvite
func GetGroupInfoFromInvite(id *C.char, JIDByte *C.uchar, JIDSize C.int, inviter *C.uchar, inviterSize C.int, code *C.char, expiration C.int) *C.struct_BytesReturn {
	var JIDInviter defproto.JID
	var JID defproto.JID
	err_jid := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	return_proto := defproto.GetGroupInfoReturnFunction{}
	if err_jid != nil {
		return_proto.Error = proto.String(err_jid.Error())
		return ProtoReturnV3(&return_proto)
	}
	err_inviter := proto.Unmarshal(getByteByAddr(inviter, inviterSize), &JIDInviter)
	if err_inviter != nil {
		return_proto.Error = proto.String(err_inviter.Error())
		return ProtoReturnV3(&return_proto)
	}
	group_info, err := clients[C.GoString(id)].GetGroupInfoFromInvite(utils.DecodeJidProto(&JID), utils.DecodeJidProto(&JIDInviter), C.GoString(code), int64(expiration))
	if err != nil {
		return_proto.Error = proto.String(err.Error())
	}
	if group_info != nil {
		return_proto.GroupInfo = utils.EncodeGroupInfo(group_info)
	}
	return ProtoReturnV3(&return_proto)
}

//export GetGroupInfoFromLink
func GetGroupInfoFromLink(id *C.char, code *C.char) *C.struct_BytesReturn {
	return_proto := defproto.GetGroupInfoReturnFunction{}
	info, err := clients[C.GoString(id)].GetGroupInfoFromLink(C.GoString(code))
	if err != nil {
		return_proto.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_proto)
	}
	if info != nil {
		return_proto.GroupInfo = utils.EncodeGroupInfo(info)
	}
	return ProtoReturnV3(&return_proto)
}

//export GetGroupRequestParticipants
func GetGroupRequestParticipants(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	return_ := defproto.GetGroupRequestParticipantsReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	request_participants, err_request := clients[C.GoString(id)].GetGroupRequestParticipants(utils.DecodeJidProto(&JID))
	participants := []*defproto.GroupParticipantRequest{}
	for _, participant := range request_participants {
		participants = append(participants, &defproto.GroupParticipantRequest{
			Participant: utils.EncodeJidProto(participant.JID),
			TimeAt:      proto.Uint64(uint64(participant.RequestedAt.UnixMicro())),
		})
	}
	return_.Participants = participants
	// return_ := defproto.GetGroupRequestParticipantsReturnFunction{
	// Participants: participants,
	// }
	if err_request != nil {
		return_.Error = proto.String(err_request.Error())
		return ProtoReturnV3(&return_)
	}
	return ProtoReturnV3(&return_)
}

//export GetLinkedGroupsParticipants
func GetLinkedGroupsParticipants(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	return_ := defproto.ReturnFunctionWithError{}
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	JIDS, err_get := clients[C.GoString(id)].GetLinkedGroupsParticipants(utils.DecodeJidProto(&JID))
	if err_get != nil {
		return_.Error = proto.String(err_get.Error())
		return ProtoReturnV3(&return_)
	}
	neonizeJID := []*defproto.JID{}
	for _, jid := range JIDS {
		neonizeJID = append(neonizeJID, utils.EncodeJidProto(jid))
	}
	return_.Return = &defproto.ReturnFunctionWithError_GetLinkedGroupsParticipants{
		GetLinkedGroupsParticipants: &defproto.JIDArray{
			JIDS: neonizeJID,
		},
	}
	return ProtoReturnV3(&return_)
}

//export SetGroupName
func SetGroupName(id *C.char, JIDByte *C.uchar, JIDSize C.int, name *C.char) *C.char {
	jidbyte := getByteByAddr(JIDByte, JIDSize)
	var neoJIDProto defproto.JID
	err := proto.Unmarshal(jidbyte, &neoJIDProto)
	if err != nil {
		return C.CString(err.Error())
	}
	status_err := clients[C.GoString(id)].SetGroupName(utils.DecodeJidProto(&neoJIDProto), C.GoString(name))
	if status_err != nil {
		return C.CString(status_err.Error())

	}
	return C.CString("")

}

//export SetGroupPhoto
func SetGroupPhoto(id *C.char, JIDByte *C.uchar, JIDSize C.int, Photo *C.uchar, PhotoSize C.int) *C.struct_BytesReturn {
	var neoJIDProto defproto.JID
	return_ := defproto.SetGroupPhotoReturnFunction{}
	JIDbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(JIDbyte, &neoJIDProto)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	photo_buf := getByteByAddr(Photo, PhotoSize)
	response, err_status := clients[C.GoString(id)].SetGroupPhoto(utils.DecodeJidProto(&neoJIDProto), photo_buf)
	return_.PictureID = &response
	if err_status != nil {
		return_.Error = proto.String(err_status.Error())
	}
	return ProtoReturnV3(&return_)
}

//export SetProfilePhoto
func SetProfilePhoto(id *C.char, Photo *C.uchar, PhotoSize C.int) *C.struct_BytesReturn {
	var empty types.JID
	photo_buf := getByteByAddr(Photo, PhotoSize)
	response, err_status := clients[C.GoString(id)].SetGroupPhoto(empty, photo_buf)
	return_ := defproto.SetGroupPhotoReturnFunction{
		PictureID: &response,
	}
	if err_status != nil {
		return_.Error = proto.String(err_status.Error())
	}
	return ProtoReturnV3(&return_)
}

//export LeaveGroup
func LeaveGroup(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.char {
	var neoJIDProto defproto.JID
	JIDbyte := getByteByAddr(JIDByte, JIDSize)
	err := proto.Unmarshal(JIDbyte, &neoJIDProto)
	if err != nil {
		return C.CString(err.Error())
	}
	err_status := clients[C.GoString(id)].LeaveGroup(utils.DecodeJidProto(&neoJIDProto))
	if err_status != nil {
		return C.CString(err_status.Error())
	}
	return C.CString("")
}

//export GetGroupInviteLink
func GetGroupInviteLink(id *C.char, JIDByte *C.uchar, JIDSize C.int, revoke C.bool) *C.struct_BytesReturn {
	var neoJIDProto defproto.JID
	JIDbyte := getByteByAddr(JIDByte, JIDSize)
	return_ := defproto.GetGroupInviteLinkReturnFunction{}
	err := proto.Unmarshal(JIDbyte, &neoJIDProto)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	url, err := clients[C.GoString(id)].GetGroupInviteLink(utils.DecodeJidProto(&neoJIDProto), bool(revoke))
	return_.InviteLink = &url
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return ProtoReturnV3(&return_)
}

//export JoinGroupWithLink
func JoinGroupWithLink(id *C.char, code *C.char) *C.struct_BytesReturn {
	jid, err := clients[C.GoString(id)].JoinGroupWithLink(C.GoString(code))

	neojid := utils.EncodeJidProto(jid)

	return_ := defproto.JoinGroupWithLinkReturnFunction{
		Jid: neojid,
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}

	return ProtoReturnV3(&return_)
}

//export JoinGroupWithInvite
func JoinGroupWithInvite(id *C.char, JIDByte *C.uchar, JIDSize C.int, inviterByte *C.uchar, inviterSize C.int, code *C.char, expiration C.int) *C.char {
	var JID, Inviter defproto.JID
	err := proto.Unmarshal(getByteByAddr(inviterByte, inviterSize), &Inviter)
	if err != nil {
		return C.CString(err.Error())
	}
	err_unmarshal := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err_unmarshal != nil {
		return C.CString(err_unmarshal.Error())
	}
	err_join := clients[C.GoString(id)].JoinGroupWithInvite(utils.DecodeJidProto(&JID), utils.DecodeJidProto(&Inviter), C.GoString(code), int64(expiration))
	if err_join != nil {
		return C.CString(err_join.Error())
	}
	return C.CString("")
}

//export LinkGroup
func LinkGroup(id *C.char, parent *C.uchar, parentSize C.int, child *C.uchar, childSize C.int) *C.char {
	var parentJID, childJID defproto.JID
	err_parent := proto.Unmarshal(getByteByAddr(parent, parentSize), &parentJID)
	if err_parent != nil {
		return C.CString(err_parent.Error())
	}
	err_child := proto.Unmarshal(getByteByAddr(child, childSize), &childJID)
	if err_child != nil {
		return C.CString(err_child.Error())
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
	var neonize_jid defproto.JID
	err := proto.Unmarshal(jidbyte, &neonize_jid)
	if err != nil {
		return C.CString(err.Error())
	}
	err_status := clients[C.GoString(id)].SendChatPresence(
		utils.DecodeJidProto(&neonize_jid),
		utils.ChatPresence[int(state)],
		utils.ChatPresenceMedia[int(media)],
	)
	if err_status != nil {
		return C.CString(err_status.Error())
	}
	return C.CString("")
}

//export BuildRevoke
func BuildRevoke(id *C.char, ChatByte *C.uchar, ChatSize C.int, SenderByte *C.uchar, SenderSize C.int, messageID *C.char) *C.struct_BytesReturn {
	var Chat defproto.JID
	var Sender defproto.JID
	chatByte := getByteByAddr(ChatByte, ChatSize)
	senderByte := getByteByAddr(SenderByte, SenderSize)
	err := proto.Unmarshal(chatByte, &Chat)
	return_ := defproto.BuildMessageReturnFunction{}

	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	err_ := proto.Unmarshal(senderByte, &Sender)
	if err_ != nil {
		return_.Error = proto.String(err_.Error())
		return ProtoReturnV3(&return_)
	}
	message := clients[C.GoString(id)].BuildRevoke(
		utils.DecodeJidProto(&Chat),
		utils.DecodeJidProto(&Sender),
		C.GoString(messageID),
	)
	return_.Message = message
	return ProtoReturnV3(&return_)
}

//export BuildPollVoteCreation
func BuildPollVoteCreation(id *C.char, name *C.char, options *C.uchar, optionsSize C.int, selectableOptionCount C.int) *C.struct_BytesReturn {
	var options_proto defproto.ArrayString
	option_byte := getByteByAddr(options, optionsSize)
	return_ := defproto.BuildMessageReturnFunction{}
	err := proto.Unmarshal(option_byte, &options_proto)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	msg := clients[C.GoString(id)].BuildPollCreation(C.GoString(name), options_proto.Data, int(selectableOptionCount))
	return_.Message = msg
	return ProtoReturnV3(&return_)
}

//export CreateNewsletter
func CreateNewsletter(id *C.char, createNewsletterParams *C.uchar, size C.int) *C.struct_BytesReturn {
	var neonizeParams defproto.CreateNewsletterParams
	params_byte := getByteByAddr(createNewsletterParams, size)
	err := proto.Unmarshal(params_byte, &neonizeParams)
	if err != nil {
		panic(err)
	}
	return_ := defproto.CreateNewsLetterReturnFunction{}
	metadata, err_metadata := clients[C.GoString(id)].CreateNewsletter(utils.DecodeCreateNewsletterParams(&neonizeParams))
	if err_metadata != nil {
		return_.Error = proto.String(err_metadata.Error())
	}
	if metadata != nil {
		return_.NewsletterMetadata = utils.EncodeNewsLetterMessageMetadata(*metadata)
	}
	return ProtoReturnV3(&return_)
}

//export FollowNewsletter
func FollowNewsletter(id *C.char, jid *C.uchar, size C.int) *C.char {
	var JID defproto.JID
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
func GetNewsletterInfo(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	metadata_proto := defproto.CreateNewsLetterReturnFunction{}
	metadata, err_metadata := clients[C.GoString(id)].GetNewsletterInfo(utils.DecodeJidProto(&JID))
	if metadata != nil {
		metadata_proto.NewsletterMetadata = utils.EncodeNewsLetterMessageMetadata(*metadata)
	}
	if err_metadata != nil {
		metadata_proto.Error = proto.String(err_metadata.Error())
	}
	return ProtoReturnV3(&metadata_proto)
}

//export GetNewsletterInfoWithInvite
func GetNewsletterInfoWithInvite(id *C.char, key *C.char) *C.struct_BytesReturn {
	return_ := defproto.CreateNewsLetterReturnFunction{}
	metadata, err := clients[C.GoString(id)].GetNewsletterInfoWithInvite(C.GoString(key))
	if metadata != nil {
		return_.NewsletterMetadata = utils.EncodeNewsLetterMessageMetadata(*metadata)
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return ProtoReturnV3(&return_)
}

//export GetNewsletterMessageUpdate
func GetNewsletterMessageUpdate(id *C.char, JIDByte *C.uchar, JIDSize C.int, Count C.int, Since C.int, After C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	newsletterMessage, errnewsletter := clients[C.GoString(id)].GetNewsletterMessageUpdates(utils.DecodeJidProto(&JID), &whatsmeow.GetNewsletterUpdatesParams{
		Count: int(Count),
		Since: time.Unix(int64(Since), 0),
		After: int(After),
	})
	return_ := defproto.GetNewsletterMessageUpdateReturnFunction{}
	if errnewsletter != nil {
		return_.Error = proto.String(errnewsletter.Error())
	}
	NewsletterMessages := []*defproto.NewsletterMessage{}
	for _, msg := range newsletterMessage {
		NewsletterMessages = append(NewsletterMessages, utils.EncodeNewsletterMessage(msg))
	}
	if newsletterMessage != nil {
		return_.NewsletterMessage = NewsletterMessages
	}
	return ProtoReturnV3(&return_)
}

//export GetNewsletterMessages
func GetNewsletterMessages(id *C.char, JIDByte *C.uchar, JIDSize C.int, Count C.int, Before C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	newsletterMessage, errnewsletter := clients[C.GoString(id)].GetNewsletterMessages(utils.DecodeJidProto(&JID), &whatsmeow.GetNewsletterMessagesParams{
		Count:  int(Count),
		Before: int(Before),
	})
	return_ := defproto.GetNewsletterMessageUpdateReturnFunction{}
	if errnewsletter != nil {
		return_.Error = proto.String(errnewsletter.Error())
	}
	NewsletterMessages := []*defproto.NewsletterMessage{}
	for _, msg := range newsletterMessage {
		NewsletterMessages = append(NewsletterMessages, utils.EncodeNewsletterMessage(msg))
	}
	if newsletterMessage != nil {
		return_.NewsletterMessage = NewsletterMessages
	}
	return ProtoReturnV3(&return_)
}

//export Logout
func Logout(id *C.char) *C.char {
	err := clients[C.GoString(id)].Logout(context.TODO())
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export MarkRead
func MarkRead(id *C.char, ids *C.char, timestamp C.int, chatByte *C.uchar, chatSize C.int, senderByte *C.uchar, senderSize C.int, receiptType *C.char) *C.char {
	var chatJID, senderJID defproto.JID
	chat_err := proto.Unmarshal(getByteByAddr(chatByte, chatSize), &chatJID)
	if chat_err != nil {
		return C.CString(chat_err.Error())
	}
	sender_err := proto.Unmarshal(getByteByAddr(senderByte, senderSize), &senderJID)
	if sender_err != nil {
		return C.CString(sender_err.Error())
	}
	err := clients[C.GoString(id)].MarkRead(strings.Split(C.GoString(ids), " "), time.Unix(int64(timestamp), 0), utils.DecodeJidProto(&chatJID), utils.DecodeJidProto(&senderJID), types.ReceiptType(C.GoString(receiptType)))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export NewsletterMarkViewed
func NewsletterMarkViewed(id *C.char, JIDByte *C.uchar, JIDSize C.int, MessageServerID *C.uchar, MessageServerIDSize C.int) *C.char {
	var JID defproto.JID
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
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return C.CString(err.Error())
	}
	err_react := clients[C.GoString(id)].NewsletterSendReaction(utils.DecodeJidProto(&JID), int(messageServerID), C.GoString(reaction), C.GoString(messageID))
	if err_react != nil {
		return C.CString(err_react.Error())
	}
	return C.CString("")
}

//export NewsletterSubscribeLiveUpdates
func NewsletterSubscribeLiveUpdates(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		panic(err)
	}
	duration, err_subs := clients[C.GoString(id)].NewsletterSubscribeLiveUpdates(context.Background(), utils.DecodeJidProto(&JID))
	return_ := defproto.NewsletterSubscribeLiveUpdatesReturnFunction{
		Duration: proto.Int64(int64(duration)),
	}
	if err_subs != nil {
		return_.Error = proto.String(err_subs.Error())
	}
	return ProtoReturnV3(&return_)
}

//export NewsletterToggleMute
func NewsletterToggleMute(id *C.char, JIDByte *C.uchar, JIDSize C.int, mute C.bool) *C.char {
	var JID defproto.JID
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
func ResolveBusinessMessageLink(id *C.char, code *C.char) *C.struct_BytesReturn {
	return_ := defproto.ResolveBusinessMessageLinkReturnFunction{}
	message_link, err := clients[C.GoString(id)].ResolveBusinessMessageLink(C.GoString(code))
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	if message_link != nil {
		return_.MessageLinkTarget = utils.EncodeBusinessMessageLinkTarget(*message_link)
	}
	return ProtoReturnV3(&return_)
}

//export ResolveContactQRLink
func ResolveContactQRLink(id *C.char, code *C.char) *C.struct_BytesReturn {
	return_ := defproto.ResolveContactQRLinkReturnFunction{}
	contact, err := clients[C.GoString(id)].ResolveContactQRLink(C.GoString(code))
	if contact != nil {
		return_.ContactQrLink = utils.EncodeContactQRLinkTarget(*contact)
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return ProtoReturnV3(&return_)
}

//export SendAppState
func SendAppState(id *C.char, patchByte *C.uchar, patchSize C.int) *C.char {
	var patchInfo defproto.PatchInfo
	err_unmarshal := proto.Unmarshal(getByteByAddr(patchByte, patchSize), &patchInfo)
	if err_unmarshal != nil {
		return C.CString(err_unmarshal.Error())
	}
	err := clients[C.GoString(id)].SendAppState(context.Background(), *utils.DecodePatchInfo(&patchInfo))
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

//export SetDisappearingTimer
func SetDisappearingTimer(id *C.char, JIDByte *C.uchar, JIDSize C.int, timer C.int64_t) *C.char {
	var JID defproto.JID
	err_ := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err_ != nil {
		panic(err_)
	}
	err := clients[C.GoString(id)].SetDisappearingTimer(utils.DecodeJidProto(&JID), time.Duration(timer))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export SetForceActiveDeliveryReceipts
func SetForceActiveDeliveryReceipts(id *C.char, active C.bool) {
	clients[C.GoString(id)].SetForceActiveDeliveryReceipts(bool(active))
}

//export SetGroupAnnounce
func SetGroupAnnounce(id *C.char, JIDByte *C.uchar, JIDSize C.int, announce C.bool) *C.char {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return C.CString(err.Error())
	}
	err_announce := clients[C.GoString(id)].SetGroupAnnounce(utils.DecodeJidProto(&JID), bool(announce))
	if err_announce != nil {
		return C.CString(err_announce.Error())
	}
	return C.CString("")
}

//export SetGroupLocked
func SetGroupLocked(id *C.char, JIDByte *C.uchar, JIDSize C.int, locked C.bool) *C.char {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return C.CString(err.Error())
	}
	err_locked := clients[C.GoString(id)].SetGroupLocked(utils.DecodeJidProto(&JID), bool(locked))
	if err_locked != nil {
		return C.CString(err_locked.Error())
	}
	return C.CString("")
}

//export SetGroupTopic
func SetGroupTopic(id *C.char, JIDByte *C.uchar, JIDSize C.int, previousID, newID, topic *C.char) *C.char {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return C.CString(err.Error())
	}
	err_topic := clients[C.GoString(id)].SetGroupTopic(utils.DecodeJidProto(&JID), C.GoString(previousID), C.GoString(newID), C.GoString(topic))
	if err_topic != nil {
		return C.CString(err_topic.Error())
	}
	return C.CString("")
}

//export SetPrivacySetting
func SetPrivacySetting(id *C.char, name *C.char, value *C.char) *C.struct_BytesReturn {
	return_ := defproto.SetPrivacySettingReturnFunction{}
	privacy_settings, err := clients[C.GoString(id)].SetPrivacySetting(context.Background(), types.PrivacySettingType(C.GoString(name)), types.PrivacySetting(C.GoString(value)))
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_.Settings = utils.EncodePrivacySettings(privacy_settings)
	return ProtoReturnV3(&return_)
}

//export SetPassive
func SetPassive(id *C.char, passive C.bool) *C.char {
	err := clients[C.GoString(id)].SetPassive(context.Background(), bool(passive))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export SetStatusMessage
func SetStatusMessage(id *C.char, msg *C.char) *C.char {
	err := clients[C.GoString(id)].SetStatusMessage(C.GoString(msg))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export SubscribePresence
func SubscribePresence(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.char {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return C.CString(err.Error())
	}
	err_ := clients[C.GoString(id)].SubscribePresence(utils.DecodeJidProto(&JID))
	if err_ != nil {
		return C.CString(err_.Error())
	}
	return C.CString("")
}

//export UnfollowNewsletter
func UnfollowNewsletter(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.char {
	var JID defproto.JID
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return C.CString(err.Error())
	}
	err_ := clients[C.GoString(id)].UnfollowNewsletter(utils.DecodeJidProto(&JID))
	if err_ != nil {
		return C.CString(err_.Error())
	}
	return C.CString("")
}

//export UnlinkGroup
func UnlinkGroup(id *C.char, parentByte *C.uchar, parentSize C.int, childByte *C.uchar, childSize C.int) *C.char {
	var parent, child defproto.JID
	err_p := proto.Unmarshal(getByteByAddr(parentByte, parentSize), &parent)
	if err_p != nil {
		return C.CString(err_p.Error())
	}
	err_c := proto.Unmarshal(getByteByAddr(childByte, childSize), &child)
	if err_c != nil {
		return C.CString(err_c.Error())
	}
	err := clients[C.GoString(id)].UnlinkGroup(utils.DecodeJidProto(&parent), utils.DecodeJidProto(&child))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export UpdateBlocklist
func UpdateBlocklist(id *C.char, jidByte *C.uchar, JIDSize C.int, action *C.char) *C.struct_BytesReturn {
	var JID defproto.JID
	return_ := defproto.GetBlocklistReturnFunction{}
	err_j := proto.Unmarshal(getByteByAddr(jidByte, JIDSize), &JID)
	if err_j != nil {
		return_.Error = proto.String(err_j.Error())
		return ProtoReturnV3(&return_)
	}
	blocklist, err := clients[C.GoString(id)].UpdateBlocklist(utils.DecodeJidProto(&JID), events.BlocklistChangeAction(C.GoString(action)))
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	if blocklist != nil {
		return_.Blocklist = utils.EncodeBlocklist(blocklist)
	}
	return ProtoReturnV3(&return_)
}

//export UpdateGroupParticipants
func UpdateGroupParticipants(id *C.char, JIDByte *C.uchar, JIDSize C.int, participantsChanges *C.uchar, participantSize C.int, action *C.char) *C.struct_BytesReturn {
	var JID defproto.JID
	var jidArray defproto.JIDArray
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	return_ := defproto.UpdateGroupParticipantsReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	err_ := proto.Unmarshal(getByteByAddr(participantsChanges, participantSize), &jidArray)
	if err_ != nil {
		return_.Error = proto.String(err_.Error())
		return ProtoReturnV3(&return_)
	}
	ParticipantChanges := make([]types.JID, len(jidArray.JIDS))
	for i, participant := range jidArray.JIDS {
		ParticipantChanges[i] = utils.DecodeJidProto(participant)
	}
	participants, err_changes := clients[C.GoString(id)].UpdateGroupParticipants(utils.DecodeJidProto(&JID), ParticipantChanges, whatsmeow.ParticipantChange(C.GoString(action)))
	if err_changes != nil {
		return_.Error = proto.String(err_changes.Error())
	}
	neonizeParticipants := make([]*defproto.GroupParticipant, len(participants))
	for i, participant := range participants {
		neonizeParticipants[i] = utils.EncodeGroupParticipant(participant)
	}
	return_.Participants = neonizeParticipants
	return ProtoReturnV3(&return_)
}

//export GetPrivacySettings
func GetPrivacySettings(id *C.char) *C.struct_BytesReturn {
	settings := utils.EncodePrivacySettings(clients[C.GoString(id)].GetPrivacySettings(context.Background()))
	return ProtoReturnV3(settings)
}

//export GetProfilePicture
func GetProfilePicture(id *C.char, JIDByte *C.uchar, JIDSize C.int, paramsByte *C.uchar, paramsSize C.int) *C.struct_BytesReturn {
	var neonizeJID defproto.JID
	var neonizeParams defproto.GetProfilePictureParams
	return_ := defproto.GetProfilePictureReturnFunction{}
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &neonizeJID)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	err_params := proto.Unmarshal(getByteByAddr(paramsByte, paramsSize), &neonizeParams)
	if err_params != nil {
		return_.Error = proto.String(err_params.Error())
		return ProtoReturnV3(&return_)
	}
	picture, err_pict := clients[C.GoString(id)].GetProfilePictureInfo(utils.DecodeJidProto(&neonizeJID), utils.DecodeGetProfilePictureParams(&neonizeParams))
	if err_pict != nil {
		return_.Error = proto.String(err_pict.Error())
		return ProtoReturnV3(&return_)
	}
	if picture != nil {
		return_.Picture = utils.EncodeProfilePictureInfo(*picture)
	}
	return ProtoReturnV3(&return_)
}

//export GetStatusPrivacy
func GetStatusPrivacy(id *C.char) *C.struct_BytesReturn {
	return_ := defproto.GetStatusPrivacyReturnFunction{}
	status_privacy_encoded := []*defproto.StatusPrivacy{}
	status_privacy, err := clients[C.GoString(id)].GetStatusPrivacy()
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	for _, privacy := range status_privacy {
		status_privacy_encoded = append(status_privacy_encoded, utils.EncodeStatusPrivacy(privacy))
	}
	return_.StatusPrivacy = status_privacy_encoded
	return ProtoReturnV3(&return_)
}

//export GetSubGroups
func GetSubGroups(id *C.char, JIDByte *C.uchar, JIDSize C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	return_ := defproto.GetSubGroupsReturnFunction{}
	err := proto.Unmarshal(getByteByAddr(JIDByte, JIDSize), &JID)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	groups := []*defproto.GroupLinkTarget{}
	linked_groups, group_err := clients[C.GoString(id)].GetSubGroups(utils.DecodeJidProto(&JID))
	if group_err != nil {
		return_.Error = proto.String(group_err.Error())
		return ProtoReturnV3(&return_)
	}
	for _, group := range linked_groups {
		groups = append(groups, utils.EncodeGroupLinkTarget(*group))
	}
	return_.GroupLinkTarget = groups
	return ProtoReturnV3(&return_)
}

//export GetSubscribedNewsletters
func GetSubscribedNewsletters(id *C.char) *C.struct_BytesReturn {
	return_ := defproto.GetSubscribedNewslettersReturnFunction{}
	newsletters_ := []*defproto.NewsletterMetadata{}
	newsletters, err_newsletter := clients[C.GoString(id)].GetSubscribedNewsletters()
	for _, newsletter := range newsletters {
		newsletters_ = append(newsletters_, utils.EncodeNewsLetterMessageMetadata(*newsletter))
	}
	return_.Newsletter = newsletters_
	if err_newsletter != nil {
		return_.Error = proto.String(err_newsletter.Error())
	}
	return ProtoReturnV3(&return_)
}

//export GetUserDevices
func GetUserDevices(id *C.char, JIDSByte *C.uchar, JIDSSize C.int) *C.struct_BytesReturn {
	var JIDS defproto.JIDArray
	jids := []types.JID{}
	return_ := defproto.GetUserDevicesreturnFunction{}
	err := proto.Unmarshal(getByteByAddr(JIDSByte, JIDSSize), &JIDS)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	for _, jid := range JIDS.JIDS {
		jids = append(jids, utils.DecodeJidProto(jid))
	}
	jidstypes, err_jids := clients[C.GoString(id)].GetUserDevicesContext(context.Background(), jids)
	neonizeJID := []*defproto.JID{}
	for _, jid := range jidstypes {
		neonizeJID = append(neonizeJID, utils.EncodeJidProto(jid))
	}
	return_.JID = neonizeJID
	if err_jids != nil {
		return_.Error = proto.String(err_jids.Error())
	}
	return ProtoReturnV3(&return_)
}

//export GetBlocklist
func GetBlocklist(id *C.char) *C.struct_BytesReturn {
	blocklist, err := clients[C.GoString(id)].GetBlocklist()
	return_ := defproto.GetBlocklistReturnFunction{}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	if blocklist != nil {
		return_.Blocklist = utils.EncodeBlocklist(blocklist)
	}
	return ProtoReturnV3(&return_)
}

//export BuildPollVote
func BuildPollVote(id *C.char, pollInfo *C.uchar, pollInfoSize C.int, optionName *C.uchar, optionNameSize C.int) *C.struct_BytesReturn {
	var msgInfo defproto.MessageInfo
	var optionNames defproto.ArrayString
	return_ := defproto.BuildPollVoteReturnFunction{}
	err := proto.Unmarshal(getByteByAddr(pollInfo, pollInfoSize), &msgInfo)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	err_2 := proto.Unmarshal(getByteByAddr(optionName, optionNameSize), &optionNames)
	if err_2 != nil {
		return_.Error = proto.String(err_2.Error())
		return ProtoReturnV3(&return_)
	}
	pollInfo_, err_poll := clients[C.GoString(id)].BuildPollVote(context.Background(), utils.DecodeMessageInfo(&msgInfo), optionNames.Data)
	if err_poll != nil {
		return_.Error = proto.String(err_poll.Error())
	}
	if pollInfo_ != nil {
		return_.PollVote = pollInfo_
	}
	return ProtoReturnV3(&return_)
}

//export BuildReaction
func BuildReaction(id *C.char, chat *C.uchar, chatSize C.int, sender *C.uchar, senderSize C.int, messageID *C.char, reaction *C.char) *C.struct_BytesReturn {
	var Chat defproto.JID
	var Sender defproto.JID
	return_ := defproto.BuildMessageReturnFunction{}
	chat_err := proto.Unmarshal(getByteByAddr(chat, chatSize), &Chat)
	if chat_err != nil {
		return_.Error = proto.String(chat_err.Error())
	}
	sender_err := proto.Unmarshal(getByteByAddr(sender, senderSize), &Sender)
	if sender_err != nil {
		return_.Error = proto.String(sender_err.Error())
	}
	msg := clients[C.GoString(id)].BuildReaction(
		utils.DecodeJidProto(&Chat),
		utils.DecodeJidProto(&Sender),
		C.GoString(messageID),
		C.GoString(reaction),
	)
	return_.Message = msg
	return ProtoReturnV3(&return_)
}

//export CreateGroup
func CreateGroup(id *C.char, createGroupByte *C.uchar, createGroupSize C.int) *C.struct_BytesReturn {
	return_ := defproto.GetGroupInfoReturnFunction{}
	creategrupbyte := getByteByAddr(createGroupByte, createGroupSize)
	var reqCreateGroup defproto.ReqCreateGroup
	err := proto.Unmarshal(creategrupbyte, &reqCreateGroup)
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	group_info, err_ := clients[C.GoString(id)].CreateGroup(utils.DecodeReqCreateGroup(&reqCreateGroup))
	if group_info != nil {
		return_.GroupInfo = utils.EncodeGroupInfo(group_info)
	}
	if err_ != nil {
		return_.Error = proto.String(err_.Error())
	}
	return ProtoReturnV3(&return_)
}

//export GetJoinedGroups
func GetJoinedGroups(id *C.char) *C.struct_BytesReturn {
	return_ := defproto.GetJoinedGroupsReturnFunction{}
	neonize_groups_info := []*defproto.GroupInfo{}
	joined_groups, err := clients[C.GoString(id)].GetJoinedGroups()
	if err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	for _, group_info := range joined_groups {
		neonize_groups_info = append(neonize_groups_info, utils.EncodeGroupInfo(group_info))
	}

	return_.Group = neonize_groups_info
	return ProtoReturnV3(&return_)

}

//export GetMe
func GetMe(id *C.char) *C.struct_BytesReturn {
	cli := clients[C.GoString(id)].Store
	device := defproto.Device{
		PushName:      &cli.PushName,
		Platform:      &cli.Platform,
		BussinessName: &cli.BusinessName,
		Initialized:   &cli.Initialized,
	}
	if cli.ID != nil {
		device.JID = utils.EncodeJidProto(*cli.ID)
	}
	device.LID = utils.EncodeJidProto(cli.LID)
	return ProtoReturnV3(&device)
}

//export GetContactQRLink
func GetContactQRLink(id *C.char, revoke C.bool) *C.struct_BytesReturn {
	link, err := clients[C.GoString(id)].GetContactQRLink(bool(revoke))
	QRLinkReturn := defproto.GetContactQRLinkReturnFunction{
		Link: &link,
	}
	if err != nil {
		QRLinkReturn.Error = proto.String(err.Error())
	}
	return ProtoReturnV3(&QRLinkReturn)
}

//export GetMessageForRetry
func GetMessageForRetry(id *C.char, requester *C.uchar, requesterSize C.int, to *C.uchar, toSize C.int, messageID *C.char) *C.struct_BytesReturn {
	var RequesterJID, toJID defproto.JID
	return_ := defproto.GetMessageForRetryReturnFunction{}
	err_req := proto.Unmarshal(getByteByAddr(requester, requesterSize), &RequesterJID)
	if err_req != nil {
		return_.Error = proto.String(err_req.Error())
		return ProtoReturnV3(&return_)
	}
	err_to := proto.Unmarshal(getByteByAddr(to, toSize), &toJID)
	if err_to != nil {
		return_.Error = proto.String(err_to.Error())
		return ProtoReturnV3(&return_)
	}
	msg := clients[C.GoString(id)].GetMessageForRetry(utils.DecodeJidProto(&RequesterJID), utils.DecodeJidProto(&toJID), C.GoString(messageID))
	if msg == nil {
		return_.IsEmpty = proto.Bool(true)
	} else {
		return_.Message = msg
	}
	return ProtoReturnV3(&return_)
}

// chat_settings_store.go
//
//export PutPinned
func PutPinned(id *C.char, user *C.uchar, userSize C.int, pinned C.bool) *C.char {
	var JID defproto.JID
	proto.Unmarshal(getByteByAddr(user, userSize), &JID)
	err := clients[C.GoString(id)].Store.ChatSettings.PutPinned(context.Background(), utils.DecodeJidProto(&JID), bool(pinned))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export PutArchived
func PutArchived(id *C.char, user *C.uchar, userSize C.int, archived C.bool) *C.char {
	var JID defproto.JID
	proto.Unmarshal(getByteByAddr(user, userSize), &JID)
	err := clients[C.GoString(id)].Store.ChatSettings.PutArchived(context.Background(), utils.DecodeJidProto(&JID), bool(archived))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export GetAllDevices
func GetAllDevices(db *C.char) *C.char {
	dbLog := waLog.Stdout("Database", "ERROR", true)
	container, err := getDB(db, dbLog)
	if err != nil {
		panic(err)
	}

	deviceStore, err := container.GetAllDevices(context.TODO())
	if err != nil {
		panic(err)
	}

	var result strings.Builder
	for i, device := range deviceStore {
		if i > 0 {
			// an arbitrary delimiter (a unicode to make sure pushname doesn't collide with it)
			result.WriteString("|\u0001|")
		}
		result.WriteString(fmt.Sprintf("%s,%s,%s,%t",
			device.ID.String(),
			device.PushName,
			device.BusinessName,
			device.Initialized))
	}

	return C.CString(result.String())
}

//export SendPresence
func SendPresence(id *C.char, presence *C.char) *C.char {
	err := clients[C.GoString(id)].SendPresence(types.Presence(C.GoString(presence)))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export DecryptPollVote
func DecryptPollVote(id *C.char, message *C.uchar, messageSize C.int) *C.struct_BytesReturn {
	var pvmessage defproto.Message
	return_proto := defproto.ReturnFunctionWithError{}
	err := proto.Unmarshal(getByteByAddr(message, messageSize), &pvmessage)
	if err != nil {
		return_proto.Error = proto.String(err.Error())
	}
	result, err := clients[C.GoString(id)].DecryptPollVote(context.Background(), utils.DecodeEventTypesMessage(&pvmessage))
	if err != nil {
		return_proto.Error = proto.String(err.Error())
	} else {
		return_proto.Return = &defproto.ReturnFunctionWithError_PollVoteMessage{
			PollVoteMessage: result,
		}
	}
	return ProtoReturnV3(&return_proto)
}

//export SendFBMessage
func SendFBMessage(id *C.char, to *C.uchar, toSize C.int, message *C.uchar, messageSize C.int, metadata *C.uchar, metadataSize C.int, extra *C.uchar, extraSize C.int) *C.struct_BytesReturn {
	var _return = defproto.SendMessageReturnFunction{}
	var toJID defproto.JID
	var waConsumerApp waConsumerApplication.ConsumerApplication
	var waConsumerAppMetadata waMsgApplication.MessageApplication_Metadata
	var SendRequestExtra defproto.SendRequestExtra
	err := proto.Unmarshal(
		getByteByAddr(
			to,
			toSize,
		),
		&toJID,
	)
	if err != nil {
		_return.Error = proto.String(err.Error())
		return ProtoReturnV3(&_return)
	}
	err_1 := proto.Unmarshal(
		getByteByAddr(
			message,
			messageSize,
		),
		&waConsumerApp,
	)
	if err_1 != nil {
		_return.Error = proto.String(err_1.Error())
		return ProtoReturnV3(&_return)
	}
	err_2 := proto.Unmarshal(
		getByteByAddr(metadata, metadataSize),
		&waConsumerAppMetadata,
	)
	if err_2 != nil {
		_return.Error = proto.String(err_2.Error())
		return ProtoReturnV3(&_return)
	}
	err_3 := proto.Unmarshal(
		getByteByAddr(extra, extraSize),
		&SendRequestExtra,
	)
	if err_3 != nil {
		_return.Error = proto.String(err_3.Error())
		return ProtoReturnV3(&_return)
	}
	resp, err_fbmessage := clients[C.GoString(id)].SendFBMessage(
		context.Background(),
		utils.DecodeJidProto(&toJID),
		&waConsumerApp,
		&waConsumerAppMetadata,
		utils.DecodeSendRequestExtra(
			&SendRequestExtra,
		),
	)
	if err_fbmessage != nil {
		_return.Error = proto.String(err_fbmessage.Error())
	}
	response := defproto.SendResponse{
		Timestamp:    proto.Int64(resp.Timestamp.UnixNano()),
		ID:           proto.String(resp.ID),
		ServerID:     proto.Int64(int64(resp.ServerID)),
		DebugTimings: utils.EncodeMessageDebugTimings(resp.DebugTimings),
	}
	_return.SendResponse = &response
	return ProtoReturnV3(&_return)
}
func main() {

}

// comment
func CallbackFunction(ctx context.Context, callback C.ptr_to_python_function_bytes, id string) {
	uuid := C.CString(id)
	channel := eventChannel[id]
	for {
		select {
		case <-ctx.Done():
			return
		case message := <-channel:
			buff, err := proto.Marshal(message.message)
			if err != nil {
				panic(err)
			}
			uchars, size := getBytesAndSize(buff)
			C.call_c_func_callback_bytes(callback, uuid, uchars, size, C.int(message.eventType))

		}

	}
}

//export FreeBytesStruct
func FreeBytesStruct(bytesReturn *C.struct_BytesReturn) {
	C.free(unsafe.Pointer(bytesReturn.data))
	C.free(unsafe.Pointer(bytesReturn))
}
