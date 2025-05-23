# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: waMultiDevice/WAMultiDevice.proto
# Protobuf Python Version: 6.30.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    30,
    2,
    '',
    'waMultiDevice/WAMultiDevice.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!waMultiDevice/WAMultiDevice.proto\x12\rWAMultiDevice\"\xf5\t\n\x0bMultiDevice\x12\x33\n\x07payload\x18\x01 \x01(\x0b\x32\".WAMultiDevice.MultiDevice.Payload\x12\x35\n\x08metadata\x18\x02 \x01(\x0b\x32#.WAMultiDevice.MultiDevice.Metadata\x1a\n\n\x08Metadata\x1a\x90\x01\n\x07Payload\x12\x45\n\x0f\x61pplicationData\x18\x01 \x01(\x0b\x32*.WAMultiDevice.MultiDevice.ApplicationDataH\x00\x12\x33\n\x06signal\x18\x02 \x01(\x0b\x32!.WAMultiDevice.MultiDevice.SignalH\x00\x42\t\n\x07payload\x1a\xd0\x07\n\x0f\x41pplicationData\x12\x66\n\x14\x61ppStateSyncKeyShare\x18\x01 \x01(\x0b\x32\x46.WAMultiDevice.MultiDevice.ApplicationData.AppStateSyncKeyShareMessageH\x00\x12j\n\x16\x61ppStateSyncKeyRequest\x18\x02 \x01(\x0b\x32H.WAMultiDevice.MultiDevice.ApplicationData.AppStateSyncKeyRequestMessageH\x00\x1am\n\x1d\x41ppStateSyncKeyRequestMessage\x12L\n\x06keyIDs\x18\x01 \x03(\x0b\x32<.WAMultiDevice.MultiDevice.ApplicationData.AppStateSyncKeyId\x1ag\n\x1b\x41ppStateSyncKeyShareMessage\x12H\n\x04keys\x18\x01 \x03(\x0b\x32:.WAMultiDevice.MultiDevice.ApplicationData.AppStateSyncKey\x1a\xd9\x03\n\x0f\x41ppStateSyncKey\x12K\n\x05keyID\x18\x01 \x01(\x0b\x32<.WAMultiDevice.MultiDevice.ApplicationData.AppStateSyncKeyId\x12_\n\x07keyData\x18\x02 \x01(\x0b\x32N.WAMultiDevice.MultiDevice.ApplicationData.AppStateSyncKey.AppStateSyncKeyData\x1a\x97\x02\n\x13\x41ppStateSyncKeyData\x12\x0f\n\x07keyData\x18\x01 \x01(\x0c\x12~\n\x0b\x66ingerprint\x18\x02 \x01(\x0b\x32i.WAMultiDevice.MultiDevice.ApplicationData.AppStateSyncKey.AppStateSyncKeyData.AppStateSyncKeyFingerprint\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x1a\\\n\x1a\x41ppStateSyncKeyFingerprint\x12\r\n\x05rawID\x18\x01 \x01(\r\x12\x14\n\x0c\x63urrentIndex\x18\x02 \x01(\r\x12\x19\n\rdeviceIndexes\x18\x03 \x03(\rB\x02\x10\x01\x1a\"\n\x11\x41ppStateSyncKeyId\x12\r\n\x05keyID\x18\x01 \x01(\x0c\x42\x11\n\x0f\x61pplicationData\x1a\x08\n\x06SignalB)Z\'go.mau.fi/whatsmeow/proto/waMultiDevice')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'waMultiDevice.WAMultiDevice_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\'go.mau.fi/whatsmeow/proto/waMultiDevice'
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY_APPSTATESYNCKEYDATA_APPSTATESYNCKEYFINGERPRINT'].fields_by_name['deviceIndexes']._loaded_options = None
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY_APPSTATESYNCKEYDATA_APPSTATESYNCKEYFINGERPRINT'].fields_by_name['deviceIndexes']._serialized_options = b'\020\001'
  _globals['_MULTIDEVICE']._serialized_start=53
  _globals['_MULTIDEVICE']._serialized_end=1322
  _globals['_MULTIDEVICE_METADATA']._serialized_start=176
  _globals['_MULTIDEVICE_METADATA']._serialized_end=186
  _globals['_MULTIDEVICE_PAYLOAD']._serialized_start=189
  _globals['_MULTIDEVICE_PAYLOAD']._serialized_end=333
  _globals['_MULTIDEVICE_APPLICATIONDATA']._serialized_start=336
  _globals['_MULTIDEVICE_APPLICATIONDATA']._serialized_end=1312
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEYREQUESTMESSAGE']._serialized_start=567
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEYREQUESTMESSAGE']._serialized_end=676
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEYSHAREMESSAGE']._serialized_start=678
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEYSHAREMESSAGE']._serialized_end=781
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY']._serialized_start=784
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY']._serialized_end=1257
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY_APPSTATESYNCKEYDATA']._serialized_start=978
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY_APPSTATESYNCKEYDATA']._serialized_end=1257
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY_APPSTATESYNCKEYDATA_APPSTATESYNCKEYFINGERPRINT']._serialized_start=1165
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEY_APPSTATESYNCKEYDATA_APPSTATESYNCKEYFINGERPRINT']._serialized_end=1257
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEYID']._serialized_start=1259
  _globals['_MULTIDEVICE_APPLICATIONDATA_APPSTATESYNCKEYID']._serialized_end=1293
  _globals['_MULTIDEVICE_SIGNAL']._serialized_start=1314
  _globals['_MULTIDEVICE_SIGNAL']._serialized_end=1322
# @@protoc_insertion_point(module_scope)
