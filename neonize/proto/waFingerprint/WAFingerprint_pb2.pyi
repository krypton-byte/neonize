"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _HostedState:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _HostedStateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_HostedState.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    E2EE: _HostedState.ValueType  # 0
    HOSTED: _HostedState.ValueType  # 1

class HostedState(_HostedState, metaclass=_HostedStateEnumTypeWrapper): ...

E2EE: HostedState.ValueType  # 0
HOSTED: HostedState.ValueType  # 1
global___HostedState = HostedState

@typing.final
class FingerprintData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PUBLICKEY_FIELD_NUMBER: builtins.int
    PNIDENTIFIER_FIELD_NUMBER: builtins.int
    LIDIDENTIFIER_FIELD_NUMBER: builtins.int
    USERNAMEIDENTIFIER_FIELD_NUMBER: builtins.int
    HOSTEDSTATE_FIELD_NUMBER: builtins.int
    HASHEDPUBLICKEY_FIELD_NUMBER: builtins.int
    publicKey: builtins.bytes
    pnIdentifier: builtins.bytes
    lidIdentifier: builtins.bytes
    usernameIdentifier: builtins.bytes
    hostedState: global___HostedState.ValueType
    hashedPublicKey: builtins.bytes
    def __init__(
        self,
        *,
        publicKey: builtins.bytes | None = ...,
        pnIdentifier: builtins.bytes | None = ...,
        lidIdentifier: builtins.bytes | None = ...,
        usernameIdentifier: builtins.bytes | None = ...,
        hostedState: global___HostedState.ValueType | None = ...,
        hashedPublicKey: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["hashedPublicKey", b"hashedPublicKey", "hostedState", b"hostedState", "lidIdentifier", b"lidIdentifier", "pnIdentifier", b"pnIdentifier", "publicKey", b"publicKey", "usernameIdentifier", b"usernameIdentifier"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["hashedPublicKey", b"hashedPublicKey", "hostedState", b"hostedState", "lidIdentifier", b"lidIdentifier", "pnIdentifier", b"pnIdentifier", "publicKey", b"publicKey", "usernameIdentifier", b"usernameIdentifier"]) -> None: ...

global___FingerprintData = FingerprintData

@typing.final
class CombinedFingerprint(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VERSION_FIELD_NUMBER: builtins.int
    LOCALFINGERPRINT_FIELD_NUMBER: builtins.int
    REMOTEFINGERPRINT_FIELD_NUMBER: builtins.int
    version: builtins.int
    @property
    def localFingerprint(self) -> global___FingerprintData: ...
    @property
    def remoteFingerprint(self) -> global___FingerprintData: ...
    def __init__(
        self,
        *,
        version: builtins.int | None = ...,
        localFingerprint: global___FingerprintData | None = ...,
        remoteFingerprint: global___FingerprintData | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["localFingerprint", b"localFingerprint", "remoteFingerprint", b"remoteFingerprint", "version", b"version"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["localFingerprint", b"localFingerprint", "remoteFingerprint", b"remoteFingerprint", "version", b"version"]) -> None: ...

global___CombinedFingerprint = CombinedFingerprint
