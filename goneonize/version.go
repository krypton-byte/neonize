package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.4.5"
	return C.CString(version)
}
