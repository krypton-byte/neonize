package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.3.12.1"
	return C.CString(version)
}
