package main

/*
   #include <stdlib.h>
   #include <stdbool.h>
   #include <stdint.h>
   #include <string.h>
   #include "header/cstruct.h"
*/
import "C"

import (
	"sync"
	"unsafe"

	"github.com/krypton-byte/neonize/defproto"
	"github.com/krypton-byte/neonize/utils"
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/types"
	"google.golang.org/protobuf/proto"
)

// bufPool reuses byte slices for protobuf marshaling to reduce GC pressure.
var bufPool = sync.Pool{
	New: func() interface{} {
		b := make([]byte, 0, 4096)
		return &b
	},
}

// getClient retrieves a whatsmeow client by its UUID string.
// Returns nil if the client does not exist.
func getClient(id *C.char) *whatsmeow.Client {
	return clients[C.GoString(id)]
}

// unmarshalJID decodes a protobuf-encoded JID from C memory into a Go types.JID.
// Returns the decoded JID and any unmarshal error.
func unmarshalJID(data *C.uchar, size C.int) (types.JID, error) {
	var jidProto defproto.JID
	err := proto.Unmarshal(getByteByAddr(data, size), &jidProto)
	if err != nil {
		return types.JID{}, err
	}
	return utils.DecodeJidProto(&jidProto), nil
}

// unmarshalProto decodes protobuf bytes from C memory into the given proto.Message.
func unmarshalProto(data *C.uchar, size C.int, msg proto.Message) error {
	return proto.Unmarshal(getByteByAddr(data, size), msg)
}

// protoReturnWithError creates a BytesReturn from a proto message, or returns
// an error-only response if err is non-nil. Suitable for functions that return
// *C.struct_BytesReturn with a protobuf response containing an Error field.
//
// Usage: For return types that have an Error field set via the setErr callback.
//
//	return_ := &defproto.SomeReturnFunction{}
//	if err != nil {
//	    return_.Error = proto.String(err.Error())
//	}
//	return ProtoReturnV3(return_)
//
// This helper is for the simpler case where you just need to marshal and return.
func marshalBytesReturn(msg proto.Message) *C.struct_BytesReturn {
	return ProtoReturnV3(msg)
}

// stringError returns a C string with the error message, or empty string on success.
// The caller (Python side) must free the returned C string.
func stringError(err error) *C.char {
	if err != nil {
		return C.CString(err.Error())
	}
	return C.CString("")
}

// allocBytesReturn creates a BytesReturn struct on the C heap from Go bytes.
// The caller must eventually call FreeBytesStruct to release the memory.
func allocBytesReturn(data []byte) *C.struct_BytesReturn {
	result := (*C.struct_BytesReturn)(C.malloc(C.size_t(unsafe.Sizeof(C.struct_BytesReturn{}))))
	result.size = C.size_t(len(data))
	if len(data) > 0 {
		result.data = (*C.char)(C.malloc(result.size))
		C.memcpy(unsafe.Pointer(result.data), unsafe.Pointer(&data[0]), result.size)
	} else {
		result.data = nil
	}
	return result
}
