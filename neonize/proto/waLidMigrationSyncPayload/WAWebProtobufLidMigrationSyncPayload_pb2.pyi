"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class LIDMigrationMapping(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PN_FIELD_NUMBER: builtins.int
    ASSIGNEDLID_FIELD_NUMBER: builtins.int
    LATESTLID_FIELD_NUMBER: builtins.int
    pn: builtins.int
    assignedLid: builtins.int
    latestLid: builtins.int
    def __init__(
        self,
        *,
        pn: builtins.int | None = ...,
        assignedLid: builtins.int | None = ...,
        latestLid: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["assignedLid", b"assignedLid", "latestLid", b"latestLid", "pn", b"pn"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["assignedLid", b"assignedLid", "latestLid", b"latestLid", "pn", b"pn"]) -> None: ...

global___LIDMigrationMapping = LIDMigrationMapping

@typing.final
class LIDMigrationMappingSyncPayload(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PNTOLIDMAPPINGS_FIELD_NUMBER: builtins.int
    CHATDBMIGRATIONTIMESTAMP_FIELD_NUMBER: builtins.int
    chatDbMigrationTimestamp: builtins.int
    @property
    def pnToLidMappings(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___LIDMigrationMapping]: ...
    def __init__(
        self,
        *,
        pnToLidMappings: collections.abc.Iterable[global___LIDMigrationMapping] | None = ...,
        chatDbMigrationTimestamp: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["chatDbMigrationTimestamp", b"chatDbMigrationTimestamp"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["chatDbMigrationTimestamp", b"chatDbMigrationTimestamp", "pnToLidMappings", b"pnToLidMappings"]) -> None: ...

global___LIDMigrationMappingSyncPayload = LIDMigrationMappingSyncPayload
