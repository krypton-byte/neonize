# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: waCert/WACert.proto
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
    'waCert/WACert.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13waCert/WACert.proto\x12\x06WACert\"\x90\x01\n\x10NoiseCertificate\x12\x0f\n\x07\x64\x65tails\x18\x01 \x01(\x0c\x12\x11\n\tsignature\x18\x02 \x01(\x0c\x1aX\n\x07\x44\x65tails\x12\x0e\n\x06serial\x18\x01 \x01(\r\x12\x0e\n\x06issuer\x18\x02 \x01(\t\x12\x0f\n\x07\x65xpires\x18\x03 \x01(\x04\x12\x0f\n\x07subject\x18\x04 \x01(\t\x12\x0b\n\x03key\x18\x05 \x01(\x0c\"\x93\x02\n\tCertChain\x12\x30\n\x04leaf\x18\x01 \x01(\x0b\x32\".WACert.CertChain.NoiseCertificate\x12\x38\n\x0cintermediate\x18\x02 \x01(\x0b\x32\".WACert.CertChain.NoiseCertificate\x1a\x99\x01\n\x10NoiseCertificate\x12\x0f\n\x07\x64\x65tails\x18\x01 \x01(\x0c\x12\x11\n\tsignature\x18\x02 \x01(\x0c\x1a\x61\n\x07\x44\x65tails\x12\x0e\n\x06serial\x18\x01 \x01(\r\x12\x14\n\x0cissuerSerial\x18\x02 \x01(\r\x12\x0b\n\x03key\x18\x03 \x01(\x0c\x12\x11\n\tnotBefore\x18\x04 \x01(\x04\x12\x10\n\x08notAfter\x18\x05 \x01(\x04\x42\"Z go.mau.fi/whatsmeow/proto/waCert')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'waCert.WACert_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z go.mau.fi/whatsmeow/proto/waCert'
  _globals['_NOISECERTIFICATE']._serialized_start=32
  _globals['_NOISECERTIFICATE']._serialized_end=176
  _globals['_NOISECERTIFICATE_DETAILS']._serialized_start=88
  _globals['_NOISECERTIFICATE_DETAILS']._serialized_end=176
  _globals['_CERTCHAIN']._serialized_start=179
  _globals['_CERTCHAIN']._serialized_end=454
  _globals['_CERTCHAIN_NOISECERTIFICATE']._serialized_start=301
  _globals['_CERTCHAIN_NOISECERTIFICATE']._serialized_end=454
  _globals['_CERTCHAIN_NOISECERTIFICATE_DETAILS']._serialized_start=357
  _globals['_CERTCHAIN_NOISECERTIFICATE_DETAILS']._serialized_end=454
# @@protoc_insertion_point(module_scope)
