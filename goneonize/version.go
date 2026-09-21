package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.5.2"
	return C.CString(version)
}
