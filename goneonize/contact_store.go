package main

import (
	"C"

	"github.com/krypton-byte/neonize/defproto"
	"github.com/krypton-byte/neonize/utils"
	"google.golang.org/protobuf/proto"
)
import (
	"context"

	"go.mau.fi/whatsmeow/store"
)

//export PutPushName
func PutPushName(id *C.char, user *C.uchar, userSize C.int, pushname *C.char) *C.struct_BytesReturn {
	var userJID defproto.JID
	err := proto.Unmarshal(getByteByAddr(user, userSize), &userJID)
	if err != nil {
		panic(err)
	}
	return_ := defproto.ContactsPutPushNameReturnFunction{}
	status, prev_name, err := clients[C.GoString(id)].Store.Contacts.PutPushName(context.Background(), utils.DecodeJidProto(&userJID), C.GoString(pushname))
	return_.PreviousName = proto.String(prev_name)
	return_.Status = &status
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return ProtoReturnV3(&return_)
}

//export PutBusinessName
func PutBusinessName(id *C.char, user *C.uchar, userSize C.int, businessName *C.char) *C.struct_BytesReturn {
	var userJID defproto.JID
	err := proto.Unmarshal(getByteByAddr(user, userSize), &userJID)
	if err != nil {
		panic(err)
	}
	return_ := defproto.ContactsPutPushNameReturnFunction{}
	status, prev_name, err := clients[C.GoString(id)].Store.Contacts.PutBusinessName(context.Background(), utils.DecodeJidProto(&userJID), C.GoString(businessName))
	return_.PreviousName = proto.String(prev_name)
	return_.Status = &status
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return ProtoReturnV3(&return_)
}

//export PutContactName
func PutContactName(id *C.char, user *C.uchar, userSize C.int, fullName, firstName *C.char) *C.char {
	var userJID defproto.JID
	err := proto.Unmarshal(getByteByAddr(user, userSize), &userJID)
	if err != nil {
		panic(err)
	}
	err_ := clients[C.GoString(id)].Store.Contacts.PutContactName(context.Background(), utils.DecodeJidProto(&userJID), C.GoString(fullName), C.GoString(firstName))
	if err_ != nil {
		return C.CString(err_.Error())
	}
	return C.CString("")
}

//export PutAllContactNames
func PutAllContactNames(id *C.char, contacts *C.uchar, contactsSize C.int) *C.char {
	var entry defproto.ContactEntryArray
	err := proto.Unmarshal(getByteByAddr(contacts, contactsSize), &entry)
	if err != nil {
		panic(err)
	}
	var contactEntry = make([]store.ContactEntry, len(entry.ContactEntry))
	for i, centry := range entry.ContactEntry {
		contactEntry[i] = *utils.DecodeContactEntry(centry)
	}
	err_r := clients[C.GoString(id)].Store.Contacts.PutAllContactNames(context.Background(), contactEntry)
	if err_r != nil {
		return C.CString(err_r.Error())
	}
	return C.CString("")
}

//export GetContact
func GetContact(id *C.char, user *C.uchar, userSize C.int) *C.struct_BytesReturn {
	var userJID defproto.JID
	err := proto.Unmarshal(getByteByAddr(user, userSize), &userJID)
	if err != nil {
		panic(err)
	}
	contact_info, err_ := clients[C.GoString(id)].Store.Contacts.GetContact(context.Background(), utils.DecodeJidProto(&userJID))
	return_ := defproto.ContactsGetContactReturnFunction{
		ContactInfo: utils.EncodeContactInfo(contact_info),
	}
	if err_ != nil {
		return_.Error = proto.String(err_.Error())
	}
	return ProtoReturnV3(&return_)
}

//export GetAllContacts
func GetAllContacts(id *C.char) *C.struct_BytesReturn {
	contacts, err := clients[C.GoString(id)].Store.Contacts.GetAllContacts(context.Background())
	return_ := defproto.ContactsGetAllContactsReturnFunction{
		Contact: utils.EncodeContacts(contacts),
	}
	if err != nil {
		return_.Error = proto.String(err.Error())
	}
	return ProtoReturnV3(&return_)

}
