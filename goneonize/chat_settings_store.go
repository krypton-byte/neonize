package main

/*

   #include <stdlib.h>
   #include <stdbool.h>
   #include <stdint.h>
*/

import (
	"C"

	"github.com/krypton-byte/neonize/defproto"
	"github.com/krypton-byte/neonize/utils"
)

import (
	"context"
	"time"

	"google.golang.org/protobuf/proto"
)

//export PutMutedUntil
func PutMutedUntil(id *C.char, user *C.uchar, userSize C.int, mutedUntil C.float) *C.char {
	client, ok := lookupClientC(id)
	if !ok || client == nil {
		return C.CString("client not found for the given uuid")
	}
	var JID defproto.JID
	if err := proto.Unmarshal(getByteByAddr(user, userSize), &JID); err != nil {
		return C.CString(err.Error())
	}
	err := client.Store.ChatSettings.PutMutedUntil(context.Background(), utils.DecodeJidProto(&JID), time.Unix(int64(mutedUntil), 0))
	if err != nil {
		return C.CString(err.Error())
	}
	return nil
}

//export GetChatSettings
func GetChatSettings(id *C.char, user *C.uchar, userSize C.int) *C.struct_BytesReturn {
	var JID defproto.JID
	return_ := defproto.ReturnFunctionWithError{}
	client, ok := lookupClientC(id)
	if !ok || client == nil {
		return_.Error = proto.String("client not found for the given uuid")
		return ProtoReturnV3(&return_)
	}
	if err := proto.Unmarshal(getByteByAddr(user, userSize), &JID); err != nil {
		return_.Error = proto.String(err.Error())
		return ProtoReturnV3(&return_)
	}
	local_chat_settings, err := client.Store.ChatSettings.GetChatSettings(context.Background(), utils.DecodeJidProto(&JID))
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_.Return = &defproto.ReturnFunctionWithError_LocalChatSettings{
		LocalChatSettings: &defproto.LocalChatSettings{
			Found:      proto.Bool(local_chat_settings.Found),
			MutedUntil: proto.Float64(float64(local_chat_settings.MutedUntil.Unix())),
			Pinned:     proto.Bool(local_chat_settings.Pinned),
			Archived:   proto.Bool(local_chat_settings.Archived),
		},
	}
	return ProtoReturnV3(&return_)
}
