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
	var JID defproto.JID
	proto.Unmarshal(getByteByAddr(user, userSize), &JID)
	err := clients[C.GoString(id)].Store.ChatSettings.PutMutedUntil(context.Background(), utils.DecodeJidProto(&JID), time.Unix(int64(mutedUntil), 0))
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

//export GetChatSettings
func GetChatSettings(id *C.char, user *C.uchar, userSize C.int) C.struct_BytesReturn {
	var JID defproto.JID
	proto.Unmarshal(getByteByAddr(user, userSize), &JID)
	local_chat_settings, err := clients[C.GoString(id)].Store.ChatSettings.GetChatSettings(context.Background(), utils.DecodeJidProto(&JID))
	return_ := defproto.ReturnFunctionWithError{}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return_.Return = &defproto.ReturnFunctionWithError_LocalChatSettings{
		LocalChatSettings: &defproto.LocalChatSettings{
			Found:      proto.Bool(local_chat_settings.Found),
			MutedUntil: proto.Float64(float64(local_chat_settings.MutedUntil.Unix())),
			Pinned:     proto.Bool(local_chat_settings.Pinned),
			Archived:   proto.Bool(local_chat_settings.Pinned),
		},
	}
	return_bytes, err_proto := proto.Marshal(&return_)
	if err_proto != nil {
		panic(err_proto)
	}
	return ReturnBytes(return_bytes)
}
