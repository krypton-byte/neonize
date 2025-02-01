"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class ClientPayload(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _TrafficAnonymization:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TrafficAnonymizationEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload._TrafficAnonymization.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        OFF: ClientPayload._TrafficAnonymization.ValueType  # 0
        STANDARD: ClientPayload._TrafficAnonymization.ValueType  # 1

    class TrafficAnonymization(_TrafficAnonymization, metaclass=_TrafficAnonymizationEnumTypeWrapper): ...
    OFF: ClientPayload.TrafficAnonymization.ValueType  # 0
    STANDARD: ClientPayload.TrafficAnonymization.ValueType  # 1

    class _Product:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ProductEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload._Product.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        WHATSAPP: ClientPayload._Product.ValueType  # 0
        MESSENGER: ClientPayload._Product.ValueType  # 1
        INTEROP: ClientPayload._Product.ValueType  # 2
        INTEROP_MSGR: ClientPayload._Product.ValueType  # 3

    class Product(_Product, metaclass=_ProductEnumTypeWrapper): ...
    WHATSAPP: ClientPayload.Product.ValueType  # 0
    MESSENGER: ClientPayload.Product.ValueType  # 1
    INTEROP: ClientPayload.Product.ValueType  # 2
    INTEROP_MSGR: ClientPayload.Product.ValueType  # 3

    class _ConnectType:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ConnectTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload._ConnectType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        CELLULAR_UNKNOWN: ClientPayload._ConnectType.ValueType  # 0
        WIFI_UNKNOWN: ClientPayload._ConnectType.ValueType  # 1
        CELLULAR_EDGE: ClientPayload._ConnectType.ValueType  # 100
        CELLULAR_IDEN: ClientPayload._ConnectType.ValueType  # 101
        CELLULAR_UMTS: ClientPayload._ConnectType.ValueType  # 102
        CELLULAR_EVDO: ClientPayload._ConnectType.ValueType  # 103
        CELLULAR_GPRS: ClientPayload._ConnectType.ValueType  # 104
        CELLULAR_HSDPA: ClientPayload._ConnectType.ValueType  # 105
        CELLULAR_HSUPA: ClientPayload._ConnectType.ValueType  # 106
        CELLULAR_HSPA: ClientPayload._ConnectType.ValueType  # 107
        CELLULAR_CDMA: ClientPayload._ConnectType.ValueType  # 108
        CELLULAR_1XRTT: ClientPayload._ConnectType.ValueType  # 109
        CELLULAR_EHRPD: ClientPayload._ConnectType.ValueType  # 110
        CELLULAR_LTE: ClientPayload._ConnectType.ValueType  # 111
        CELLULAR_HSPAP: ClientPayload._ConnectType.ValueType  # 112

    class ConnectType(_ConnectType, metaclass=_ConnectTypeEnumTypeWrapper): ...
    CELLULAR_UNKNOWN: ClientPayload.ConnectType.ValueType  # 0
    WIFI_UNKNOWN: ClientPayload.ConnectType.ValueType  # 1
    CELLULAR_EDGE: ClientPayload.ConnectType.ValueType  # 100
    CELLULAR_IDEN: ClientPayload.ConnectType.ValueType  # 101
    CELLULAR_UMTS: ClientPayload.ConnectType.ValueType  # 102
    CELLULAR_EVDO: ClientPayload.ConnectType.ValueType  # 103
    CELLULAR_GPRS: ClientPayload.ConnectType.ValueType  # 104
    CELLULAR_HSDPA: ClientPayload.ConnectType.ValueType  # 105
    CELLULAR_HSUPA: ClientPayload.ConnectType.ValueType  # 106
    CELLULAR_HSPA: ClientPayload.ConnectType.ValueType  # 107
    CELLULAR_CDMA: ClientPayload.ConnectType.ValueType  # 108
    CELLULAR_1XRTT: ClientPayload.ConnectType.ValueType  # 109
    CELLULAR_EHRPD: ClientPayload.ConnectType.ValueType  # 110
    CELLULAR_LTE: ClientPayload.ConnectType.ValueType  # 111
    CELLULAR_HSPAP: ClientPayload.ConnectType.ValueType  # 112

    class _ConnectReason:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ConnectReasonEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload._ConnectReason.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        PUSH: ClientPayload._ConnectReason.ValueType  # 0
        USER_ACTIVATED: ClientPayload._ConnectReason.ValueType  # 1
        SCHEDULED: ClientPayload._ConnectReason.ValueType  # 2
        ERROR_RECONNECT: ClientPayload._ConnectReason.ValueType  # 3
        NETWORK_SWITCH: ClientPayload._ConnectReason.ValueType  # 4
        PING_RECONNECT: ClientPayload._ConnectReason.ValueType  # 5
        UNKNOWN: ClientPayload._ConnectReason.ValueType  # 6

    class ConnectReason(_ConnectReason, metaclass=_ConnectReasonEnumTypeWrapper): ...
    PUSH: ClientPayload.ConnectReason.ValueType  # 0
    USER_ACTIVATED: ClientPayload.ConnectReason.ValueType  # 1
    SCHEDULED: ClientPayload.ConnectReason.ValueType  # 2
    ERROR_RECONNECT: ClientPayload.ConnectReason.ValueType  # 3
    NETWORK_SWITCH: ClientPayload.ConnectReason.ValueType  # 4
    PING_RECONNECT: ClientPayload.ConnectReason.ValueType  # 5
    UNKNOWN: ClientPayload.ConnectReason.ValueType  # 6

    class _IOSAppExtension:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _IOSAppExtensionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload._IOSAppExtension.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        SHARE_EXTENSION: ClientPayload._IOSAppExtension.ValueType  # 0
        SERVICE_EXTENSION: ClientPayload._IOSAppExtension.ValueType  # 1
        INTENTS_EXTENSION: ClientPayload._IOSAppExtension.ValueType  # 2

    class IOSAppExtension(_IOSAppExtension, metaclass=_IOSAppExtensionEnumTypeWrapper): ...
    SHARE_EXTENSION: ClientPayload.IOSAppExtension.ValueType  # 0
    SERVICE_EXTENSION: ClientPayload.IOSAppExtension.ValueType  # 1
    INTENTS_EXTENSION: ClientPayload.IOSAppExtension.ValueType  # 2

    @typing.final
    class DNSSource(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        class _DNSResolutionMethod:
            ValueType = typing.NewType("ValueType", builtins.int)
            V: typing_extensions.TypeAlias = ValueType

        class _DNSResolutionMethodEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload.DNSSource._DNSResolutionMethod.ValueType], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
            SYSTEM: ClientPayload.DNSSource._DNSResolutionMethod.ValueType  # 0
            GOOGLE: ClientPayload.DNSSource._DNSResolutionMethod.ValueType  # 1
            HARDCODED: ClientPayload.DNSSource._DNSResolutionMethod.ValueType  # 2
            OVERRIDE: ClientPayload.DNSSource._DNSResolutionMethod.ValueType  # 3
            FALLBACK: ClientPayload.DNSSource._DNSResolutionMethod.ValueType  # 4
            MNS: ClientPayload.DNSSource._DNSResolutionMethod.ValueType  # 5

        class DNSResolutionMethod(_DNSResolutionMethod, metaclass=_DNSResolutionMethodEnumTypeWrapper): ...
        SYSTEM: ClientPayload.DNSSource.DNSResolutionMethod.ValueType  # 0
        GOOGLE: ClientPayload.DNSSource.DNSResolutionMethod.ValueType  # 1
        HARDCODED: ClientPayload.DNSSource.DNSResolutionMethod.ValueType  # 2
        OVERRIDE: ClientPayload.DNSSource.DNSResolutionMethod.ValueType  # 3
        FALLBACK: ClientPayload.DNSSource.DNSResolutionMethod.ValueType  # 4
        MNS: ClientPayload.DNSSource.DNSResolutionMethod.ValueType  # 5

        DNSMETHOD_FIELD_NUMBER: builtins.int
        APPCACHED_FIELD_NUMBER: builtins.int
        dnsMethod: global___ClientPayload.DNSSource.DNSResolutionMethod.ValueType
        appCached: builtins.bool
        def __init__(
            self,
            *,
            dnsMethod: global___ClientPayload.DNSSource.DNSResolutionMethod.ValueType | None = ...,
            appCached: builtins.bool | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["appCached", b"appCached", "dnsMethod", b"dnsMethod"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["appCached", b"appCached", "dnsMethod", b"dnsMethod"]) -> None: ...

    @typing.final
    class WebInfo(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        class _WebSubPlatform:
            ValueType = typing.NewType("ValueType", builtins.int)
            V: typing_extensions.TypeAlias = ValueType

        class _WebSubPlatformEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload.WebInfo._WebSubPlatform.ValueType], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
            WEB_BROWSER: ClientPayload.WebInfo._WebSubPlatform.ValueType  # 0
            APP_STORE: ClientPayload.WebInfo._WebSubPlatform.ValueType  # 1
            WIN_STORE: ClientPayload.WebInfo._WebSubPlatform.ValueType  # 2
            DARWIN: ClientPayload.WebInfo._WebSubPlatform.ValueType  # 3
            WIN32: ClientPayload.WebInfo._WebSubPlatform.ValueType  # 4
            WIN_HYBRID: ClientPayload.WebInfo._WebSubPlatform.ValueType  # 5

        class WebSubPlatform(_WebSubPlatform, metaclass=_WebSubPlatformEnumTypeWrapper): ...
        WEB_BROWSER: ClientPayload.WebInfo.WebSubPlatform.ValueType  # 0
        APP_STORE: ClientPayload.WebInfo.WebSubPlatform.ValueType  # 1
        WIN_STORE: ClientPayload.WebInfo.WebSubPlatform.ValueType  # 2
        DARWIN: ClientPayload.WebInfo.WebSubPlatform.ValueType  # 3
        WIN32: ClientPayload.WebInfo.WebSubPlatform.ValueType  # 4
        WIN_HYBRID: ClientPayload.WebInfo.WebSubPlatform.ValueType  # 5

        @typing.final
        class WebdPayload(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            USESPARTICIPANTINKEY_FIELD_NUMBER: builtins.int
            SUPPORTSSTARREDMESSAGES_FIELD_NUMBER: builtins.int
            SUPPORTSDOCUMENTMESSAGES_FIELD_NUMBER: builtins.int
            SUPPORTSURLMESSAGES_FIELD_NUMBER: builtins.int
            SUPPORTSMEDIARETRY_FIELD_NUMBER: builtins.int
            SUPPORTSE2EIMAGE_FIELD_NUMBER: builtins.int
            SUPPORTSE2EVIDEO_FIELD_NUMBER: builtins.int
            SUPPORTSE2EAUDIO_FIELD_NUMBER: builtins.int
            SUPPORTSE2EDOCUMENT_FIELD_NUMBER: builtins.int
            DOCUMENTTYPES_FIELD_NUMBER: builtins.int
            FEATURES_FIELD_NUMBER: builtins.int
            usesParticipantInKey: builtins.bool
            supportsStarredMessages: builtins.bool
            supportsDocumentMessages: builtins.bool
            supportsURLMessages: builtins.bool
            supportsMediaRetry: builtins.bool
            supportsE2EImage: builtins.bool
            supportsE2EVideo: builtins.bool
            supportsE2EAudio: builtins.bool
            supportsE2EDocument: builtins.bool
            documentTypes: builtins.str
            features: builtins.bytes
            def __init__(
                self,
                *,
                usesParticipantInKey: builtins.bool | None = ...,
                supportsStarredMessages: builtins.bool | None = ...,
                supportsDocumentMessages: builtins.bool | None = ...,
                supportsURLMessages: builtins.bool | None = ...,
                supportsMediaRetry: builtins.bool | None = ...,
                supportsE2EImage: builtins.bool | None = ...,
                supportsE2EVideo: builtins.bool | None = ...,
                supportsE2EAudio: builtins.bool | None = ...,
                supportsE2EDocument: builtins.bool | None = ...,
                documentTypes: builtins.str | None = ...,
                features: builtins.bytes | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing.Literal["documentTypes", b"documentTypes", "features", b"features", "supportsDocumentMessages", b"supportsDocumentMessages", "supportsE2EAudio", b"supportsE2EAudio", "supportsE2EDocument", b"supportsE2EDocument", "supportsE2EImage", b"supportsE2EImage", "supportsE2EVideo", b"supportsE2EVideo", "supportsMediaRetry", b"supportsMediaRetry", "supportsStarredMessages", b"supportsStarredMessages", "supportsURLMessages", b"supportsURLMessages", "usesParticipantInKey", b"usesParticipantInKey"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing.Literal["documentTypes", b"documentTypes", "features", b"features", "supportsDocumentMessages", b"supportsDocumentMessages", "supportsE2EAudio", b"supportsE2EAudio", "supportsE2EDocument", b"supportsE2EDocument", "supportsE2EImage", b"supportsE2EImage", "supportsE2EVideo", b"supportsE2EVideo", "supportsMediaRetry", b"supportsMediaRetry", "supportsStarredMessages", b"supportsStarredMessages", "supportsURLMessages", b"supportsURLMessages", "usesParticipantInKey", b"usesParticipantInKey"]) -> None: ...

        REFTOKEN_FIELD_NUMBER: builtins.int
        VERSION_FIELD_NUMBER: builtins.int
        WEBDPAYLOAD_FIELD_NUMBER: builtins.int
        WEBSUBPLATFORM_FIELD_NUMBER: builtins.int
        refToken: builtins.str
        version: builtins.str
        webSubPlatform: global___ClientPayload.WebInfo.WebSubPlatform.ValueType
        @property
        def webdPayload(self) -> global___ClientPayload.WebInfo.WebdPayload: ...
        def __init__(
            self,
            *,
            refToken: builtins.str | None = ...,
            version: builtins.str | None = ...,
            webdPayload: global___ClientPayload.WebInfo.WebdPayload | None = ...,
            webSubPlatform: global___ClientPayload.WebInfo.WebSubPlatform.ValueType | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["refToken", b"refToken", "version", b"version", "webSubPlatform", b"webSubPlatform", "webdPayload", b"webdPayload"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["refToken", b"refToken", "version", b"version", "webSubPlatform", b"webSubPlatform", "webdPayload", b"webdPayload"]) -> None: ...

    @typing.final
    class UserAgent(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        class _DeviceType:
            ValueType = typing.NewType("ValueType", builtins.int)
            V: typing_extensions.TypeAlias = ValueType

        class _DeviceTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload.UserAgent._DeviceType.ValueType], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
            PHONE: ClientPayload.UserAgent._DeviceType.ValueType  # 0
            TABLET: ClientPayload.UserAgent._DeviceType.ValueType  # 1
            DESKTOP: ClientPayload.UserAgent._DeviceType.ValueType  # 2
            WEARABLE: ClientPayload.UserAgent._DeviceType.ValueType  # 3
            VR: ClientPayload.UserAgent._DeviceType.ValueType  # 4

        class DeviceType(_DeviceType, metaclass=_DeviceTypeEnumTypeWrapper): ...
        PHONE: ClientPayload.UserAgent.DeviceType.ValueType  # 0
        TABLET: ClientPayload.UserAgent.DeviceType.ValueType  # 1
        DESKTOP: ClientPayload.UserAgent.DeviceType.ValueType  # 2
        WEARABLE: ClientPayload.UserAgent.DeviceType.ValueType  # 3
        VR: ClientPayload.UserAgent.DeviceType.ValueType  # 4

        class _ReleaseChannel:
            ValueType = typing.NewType("ValueType", builtins.int)
            V: typing_extensions.TypeAlias = ValueType

        class _ReleaseChannelEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload.UserAgent._ReleaseChannel.ValueType], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
            RELEASE: ClientPayload.UserAgent._ReleaseChannel.ValueType  # 0
            BETA: ClientPayload.UserAgent._ReleaseChannel.ValueType  # 1
            ALPHA: ClientPayload.UserAgent._ReleaseChannel.ValueType  # 2
            DEBUG: ClientPayload.UserAgent._ReleaseChannel.ValueType  # 3

        class ReleaseChannel(_ReleaseChannel, metaclass=_ReleaseChannelEnumTypeWrapper): ...
        RELEASE: ClientPayload.UserAgent.ReleaseChannel.ValueType  # 0
        BETA: ClientPayload.UserAgent.ReleaseChannel.ValueType  # 1
        ALPHA: ClientPayload.UserAgent.ReleaseChannel.ValueType  # 2
        DEBUG: ClientPayload.UserAgent.ReleaseChannel.ValueType  # 3

        class _Platform:
            ValueType = typing.NewType("ValueType", builtins.int)
            V: typing_extensions.TypeAlias = ValueType

        class _PlatformEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ClientPayload.UserAgent._Platform.ValueType], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
            ANDROID: ClientPayload.UserAgent._Platform.ValueType  # 0
            IOS: ClientPayload.UserAgent._Platform.ValueType  # 1
            WINDOWS_PHONE: ClientPayload.UserAgent._Platform.ValueType  # 2
            BLACKBERRY: ClientPayload.UserAgent._Platform.ValueType  # 3
            BLACKBERRYX: ClientPayload.UserAgent._Platform.ValueType  # 4
            S40: ClientPayload.UserAgent._Platform.ValueType  # 5
            S60: ClientPayload.UserAgent._Platform.ValueType  # 6
            PYTHON_CLIENT: ClientPayload.UserAgent._Platform.ValueType  # 7
            TIZEN: ClientPayload.UserAgent._Platform.ValueType  # 8
            ENTERPRISE: ClientPayload.UserAgent._Platform.ValueType  # 9
            SMB_ANDROID: ClientPayload.UserAgent._Platform.ValueType  # 10
            KAIOS: ClientPayload.UserAgent._Platform.ValueType  # 11
            SMB_IOS: ClientPayload.UserAgent._Platform.ValueType  # 12
            WINDOWS: ClientPayload.UserAgent._Platform.ValueType  # 13
            WEB: ClientPayload.UserAgent._Platform.ValueType  # 14
            PORTAL: ClientPayload.UserAgent._Platform.ValueType  # 15
            GREEN_ANDROID: ClientPayload.UserAgent._Platform.ValueType  # 16
            GREEN_IPHONE: ClientPayload.UserAgent._Platform.ValueType  # 17
            BLUE_ANDROID: ClientPayload.UserAgent._Platform.ValueType  # 18
            BLUE_IPHONE: ClientPayload.UserAgent._Platform.ValueType  # 19
            FBLITE_ANDROID: ClientPayload.UserAgent._Platform.ValueType  # 20
            MLITE_ANDROID: ClientPayload.UserAgent._Platform.ValueType  # 21
            IGLITE_ANDROID: ClientPayload.UserAgent._Platform.ValueType  # 22
            PAGE: ClientPayload.UserAgent._Platform.ValueType  # 23
            MACOS: ClientPayload.UserAgent._Platform.ValueType  # 24
            OCULUS_MSG: ClientPayload.UserAgent._Platform.ValueType  # 25
            OCULUS_CALL: ClientPayload.UserAgent._Platform.ValueType  # 26
            MILAN: ClientPayload.UserAgent._Platform.ValueType  # 27
            CAPI: ClientPayload.UserAgent._Platform.ValueType  # 28
            WEAROS: ClientPayload.UserAgent._Platform.ValueType  # 29
            ARDEVICE: ClientPayload.UserAgent._Platform.ValueType  # 30
            VRDEVICE: ClientPayload.UserAgent._Platform.ValueType  # 31
            BLUE_WEB: ClientPayload.UserAgent._Platform.ValueType  # 32
            IPAD: ClientPayload.UserAgent._Platform.ValueType  # 33
            TEST: ClientPayload.UserAgent._Platform.ValueType  # 34
            SMART_GLASSES: ClientPayload.UserAgent._Platform.ValueType  # 35

        class Platform(_Platform, metaclass=_PlatformEnumTypeWrapper): ...
        ANDROID: ClientPayload.UserAgent.Platform.ValueType  # 0
        IOS: ClientPayload.UserAgent.Platform.ValueType  # 1
        WINDOWS_PHONE: ClientPayload.UserAgent.Platform.ValueType  # 2
        BLACKBERRY: ClientPayload.UserAgent.Platform.ValueType  # 3
        BLACKBERRYX: ClientPayload.UserAgent.Platform.ValueType  # 4
        S40: ClientPayload.UserAgent.Platform.ValueType  # 5
        S60: ClientPayload.UserAgent.Platform.ValueType  # 6
        PYTHON_CLIENT: ClientPayload.UserAgent.Platform.ValueType  # 7
        TIZEN: ClientPayload.UserAgent.Platform.ValueType  # 8
        ENTERPRISE: ClientPayload.UserAgent.Platform.ValueType  # 9
        SMB_ANDROID: ClientPayload.UserAgent.Platform.ValueType  # 10
        KAIOS: ClientPayload.UserAgent.Platform.ValueType  # 11
        SMB_IOS: ClientPayload.UserAgent.Platform.ValueType  # 12
        WINDOWS: ClientPayload.UserAgent.Platform.ValueType  # 13
        WEB: ClientPayload.UserAgent.Platform.ValueType  # 14
        PORTAL: ClientPayload.UserAgent.Platform.ValueType  # 15
        GREEN_ANDROID: ClientPayload.UserAgent.Platform.ValueType  # 16
        GREEN_IPHONE: ClientPayload.UserAgent.Platform.ValueType  # 17
        BLUE_ANDROID: ClientPayload.UserAgent.Platform.ValueType  # 18
        BLUE_IPHONE: ClientPayload.UserAgent.Platform.ValueType  # 19
        FBLITE_ANDROID: ClientPayload.UserAgent.Platform.ValueType  # 20
        MLITE_ANDROID: ClientPayload.UserAgent.Platform.ValueType  # 21
        IGLITE_ANDROID: ClientPayload.UserAgent.Platform.ValueType  # 22
        PAGE: ClientPayload.UserAgent.Platform.ValueType  # 23
        MACOS: ClientPayload.UserAgent.Platform.ValueType  # 24
        OCULUS_MSG: ClientPayload.UserAgent.Platform.ValueType  # 25
        OCULUS_CALL: ClientPayload.UserAgent.Platform.ValueType  # 26
        MILAN: ClientPayload.UserAgent.Platform.ValueType  # 27
        CAPI: ClientPayload.UserAgent.Platform.ValueType  # 28
        WEAROS: ClientPayload.UserAgent.Platform.ValueType  # 29
        ARDEVICE: ClientPayload.UserAgent.Platform.ValueType  # 30
        VRDEVICE: ClientPayload.UserAgent.Platform.ValueType  # 31
        BLUE_WEB: ClientPayload.UserAgent.Platform.ValueType  # 32
        IPAD: ClientPayload.UserAgent.Platform.ValueType  # 33
        TEST: ClientPayload.UserAgent.Platform.ValueType  # 34
        SMART_GLASSES: ClientPayload.UserAgent.Platform.ValueType  # 35

        @typing.final
        class AppVersion(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            PRIMARY_FIELD_NUMBER: builtins.int
            SECONDARY_FIELD_NUMBER: builtins.int
            TERTIARY_FIELD_NUMBER: builtins.int
            QUATERNARY_FIELD_NUMBER: builtins.int
            QUINARY_FIELD_NUMBER: builtins.int
            primary: builtins.int
            secondary: builtins.int
            tertiary: builtins.int
            quaternary: builtins.int
            quinary: builtins.int
            def __init__(
                self,
                *,
                primary: builtins.int | None = ...,
                secondary: builtins.int | None = ...,
                tertiary: builtins.int | None = ...,
                quaternary: builtins.int | None = ...,
                quinary: builtins.int | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing.Literal["primary", b"primary", "quaternary", b"quaternary", "quinary", b"quinary", "secondary", b"secondary", "tertiary", b"tertiary"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing.Literal["primary", b"primary", "quaternary", b"quaternary", "quinary", b"quinary", "secondary", b"secondary", "tertiary", b"tertiary"]) -> None: ...

        PLATFORM_FIELD_NUMBER: builtins.int
        APPVERSION_FIELD_NUMBER: builtins.int
        MCC_FIELD_NUMBER: builtins.int
        MNC_FIELD_NUMBER: builtins.int
        OSVERSION_FIELD_NUMBER: builtins.int
        MANUFACTURER_FIELD_NUMBER: builtins.int
        DEVICE_FIELD_NUMBER: builtins.int
        OSBUILDNUMBER_FIELD_NUMBER: builtins.int
        PHONEID_FIELD_NUMBER: builtins.int
        RELEASECHANNEL_FIELD_NUMBER: builtins.int
        LOCALELANGUAGEISO6391_FIELD_NUMBER: builtins.int
        LOCALECOUNTRYISO31661ALPHA2_FIELD_NUMBER: builtins.int
        DEVICEBOARD_FIELD_NUMBER: builtins.int
        DEVICEEXPID_FIELD_NUMBER: builtins.int
        DEVICETYPE_FIELD_NUMBER: builtins.int
        DEVICEMODELTYPE_FIELD_NUMBER: builtins.int
        platform: global___ClientPayload.UserAgent.Platform.ValueType
        mcc: builtins.str
        mnc: builtins.str
        osVersion: builtins.str
        manufacturer: builtins.str
        device: builtins.str
        osBuildNumber: builtins.str
        phoneID: builtins.str
        releaseChannel: global___ClientPayload.UserAgent.ReleaseChannel.ValueType
        localeLanguageIso6391: builtins.str
        localeCountryIso31661Alpha2: builtins.str
        deviceBoard: builtins.str
        deviceExpID: builtins.str
        deviceType: global___ClientPayload.UserAgent.DeviceType.ValueType
        deviceModelType: builtins.str
        @property
        def appVersion(self) -> global___ClientPayload.UserAgent.AppVersion: ...
        def __init__(
            self,
            *,
            platform: global___ClientPayload.UserAgent.Platform.ValueType | None = ...,
            appVersion: global___ClientPayload.UserAgent.AppVersion | None = ...,
            mcc: builtins.str | None = ...,
            mnc: builtins.str | None = ...,
            osVersion: builtins.str | None = ...,
            manufacturer: builtins.str | None = ...,
            device: builtins.str | None = ...,
            osBuildNumber: builtins.str | None = ...,
            phoneID: builtins.str | None = ...,
            releaseChannel: global___ClientPayload.UserAgent.ReleaseChannel.ValueType | None = ...,
            localeLanguageIso6391: builtins.str | None = ...,
            localeCountryIso31661Alpha2: builtins.str | None = ...,
            deviceBoard: builtins.str | None = ...,
            deviceExpID: builtins.str | None = ...,
            deviceType: global___ClientPayload.UserAgent.DeviceType.ValueType | None = ...,
            deviceModelType: builtins.str | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["appVersion", b"appVersion", "device", b"device", "deviceBoard", b"deviceBoard", "deviceExpID", b"deviceExpID", "deviceModelType", b"deviceModelType", "deviceType", b"deviceType", "localeCountryIso31661Alpha2", b"localeCountryIso31661Alpha2", "localeLanguageIso6391", b"localeLanguageIso6391", "manufacturer", b"manufacturer", "mcc", b"mcc", "mnc", b"mnc", "osBuildNumber", b"osBuildNumber", "osVersion", b"osVersion", "phoneID", b"phoneID", "platform", b"platform", "releaseChannel", b"releaseChannel"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["appVersion", b"appVersion", "device", b"device", "deviceBoard", b"deviceBoard", "deviceExpID", b"deviceExpID", "deviceModelType", b"deviceModelType", "deviceType", b"deviceType", "localeCountryIso31661Alpha2", b"localeCountryIso31661Alpha2", "localeLanguageIso6391", b"localeLanguageIso6391", "manufacturer", b"manufacturer", "mcc", b"mcc", "mnc", b"mnc", "osBuildNumber", b"osBuildNumber", "osVersion", b"osVersion", "phoneID", b"phoneID", "platform", b"platform", "releaseChannel", b"releaseChannel"]) -> None: ...

    @typing.final
    class InteropData(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        ACCOUNTID_FIELD_NUMBER: builtins.int
        TOKEN_FIELD_NUMBER: builtins.int
        ENABLEREADRECEIPTS_FIELD_NUMBER: builtins.int
        accountID: builtins.int
        token: builtins.bytes
        enableReadReceipts: builtins.bool
        def __init__(
            self,
            *,
            accountID: builtins.int | None = ...,
            token: builtins.bytes | None = ...,
            enableReadReceipts: builtins.bool | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["accountID", b"accountID", "enableReadReceipts", b"enableReadReceipts", "token", b"token"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["accountID", b"accountID", "enableReadReceipts", b"enableReadReceipts", "token", b"token"]) -> None: ...

    @typing.final
    class DevicePairingRegistrationData(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        EREGID_FIELD_NUMBER: builtins.int
        EKEYTYPE_FIELD_NUMBER: builtins.int
        EIDENT_FIELD_NUMBER: builtins.int
        ESKEYID_FIELD_NUMBER: builtins.int
        ESKEYVAL_FIELD_NUMBER: builtins.int
        ESKEYSIG_FIELD_NUMBER: builtins.int
        BUILDHASH_FIELD_NUMBER: builtins.int
        DEVICEPROPS_FIELD_NUMBER: builtins.int
        eRegid: builtins.bytes
        eKeytype: builtins.bytes
        eIdent: builtins.bytes
        eSkeyID: builtins.bytes
        eSkeyVal: builtins.bytes
        eSkeySig: builtins.bytes
        buildHash: builtins.bytes
        deviceProps: builtins.bytes
        def __init__(
            self,
            *,
            eRegid: builtins.bytes | None = ...,
            eKeytype: builtins.bytes | None = ...,
            eIdent: builtins.bytes | None = ...,
            eSkeyID: builtins.bytes | None = ...,
            eSkeyVal: builtins.bytes | None = ...,
            eSkeySig: builtins.bytes | None = ...,
            buildHash: builtins.bytes | None = ...,
            deviceProps: builtins.bytes | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["buildHash", b"buildHash", "deviceProps", b"deviceProps", "eIdent", b"eIdent", "eKeytype", b"eKeytype", "eRegid", b"eRegid", "eSkeyID", b"eSkeyID", "eSkeySig", b"eSkeySig", "eSkeyVal", b"eSkeyVal"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["buildHash", b"buildHash", "deviceProps", b"deviceProps", "eIdent", b"eIdent", "eKeytype", b"eKeytype", "eRegid", b"eRegid", "eSkeyID", b"eSkeyID", "eSkeySig", b"eSkeySig", "eSkeyVal", b"eSkeyVal"]) -> None: ...

    USERNAME_FIELD_NUMBER: builtins.int
    PASSIVE_FIELD_NUMBER: builtins.int
    USERAGENT_FIELD_NUMBER: builtins.int
    WEBINFO_FIELD_NUMBER: builtins.int
    PUSHNAME_FIELD_NUMBER: builtins.int
    SESSIONID_FIELD_NUMBER: builtins.int
    SHORTCONNECT_FIELD_NUMBER: builtins.int
    CONNECTTYPE_FIELD_NUMBER: builtins.int
    CONNECTREASON_FIELD_NUMBER: builtins.int
    SHARDS_FIELD_NUMBER: builtins.int
    DNSSOURCE_FIELD_NUMBER: builtins.int
    CONNECTATTEMPTCOUNT_FIELD_NUMBER: builtins.int
    DEVICE_FIELD_NUMBER: builtins.int
    DEVICEPAIRINGDATA_FIELD_NUMBER: builtins.int
    PRODUCT_FIELD_NUMBER: builtins.int
    FBCAT_FIELD_NUMBER: builtins.int
    FBUSERAGENT_FIELD_NUMBER: builtins.int
    OC_FIELD_NUMBER: builtins.int
    LC_FIELD_NUMBER: builtins.int
    IOSAPPEXTENSION_FIELD_NUMBER: builtins.int
    FBAPPID_FIELD_NUMBER: builtins.int
    FBDEVICEID_FIELD_NUMBER: builtins.int
    PULL_FIELD_NUMBER: builtins.int
    PADDINGBYTES_FIELD_NUMBER: builtins.int
    YEARCLASS_FIELD_NUMBER: builtins.int
    MEMCLASS_FIELD_NUMBER: builtins.int
    INTEROPDATA_FIELD_NUMBER: builtins.int
    TRAFFICANONYMIZATION_FIELD_NUMBER: builtins.int
    username: builtins.int
    passive: builtins.bool
    pushName: builtins.str
    sessionID: builtins.int
    shortConnect: builtins.bool
    connectType: global___ClientPayload.ConnectType.ValueType
    connectReason: global___ClientPayload.ConnectReason.ValueType
    connectAttemptCount: builtins.int
    device: builtins.int
    product: global___ClientPayload.Product.ValueType
    fbCat: builtins.bytes
    fbUserAgent: builtins.bytes
    oc: builtins.bool
    lc: builtins.int
    iosAppExtension: global___ClientPayload.IOSAppExtension.ValueType
    fbAppID: builtins.int
    fbDeviceID: builtins.bytes
    pull: builtins.bool
    paddingBytes: builtins.bytes
    yearClass: builtins.int
    memClass: builtins.int
    trafficAnonymization: global___ClientPayload.TrafficAnonymization.ValueType
    @property
    def userAgent(self) -> global___ClientPayload.UserAgent: ...
    @property
    def webInfo(self) -> global___ClientPayload.WebInfo: ...
    @property
    def shards(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def dnsSource(self) -> global___ClientPayload.DNSSource: ...
    @property
    def devicePairingData(self) -> global___ClientPayload.DevicePairingRegistrationData: ...
    @property
    def interopData(self) -> global___ClientPayload.InteropData: ...
    def __init__(
        self,
        *,
        username: builtins.int | None = ...,
        passive: builtins.bool | None = ...,
        userAgent: global___ClientPayload.UserAgent | None = ...,
        webInfo: global___ClientPayload.WebInfo | None = ...,
        pushName: builtins.str | None = ...,
        sessionID: builtins.int | None = ...,
        shortConnect: builtins.bool | None = ...,
        connectType: global___ClientPayload.ConnectType.ValueType | None = ...,
        connectReason: global___ClientPayload.ConnectReason.ValueType | None = ...,
        shards: collections.abc.Iterable[builtins.int] | None = ...,
        dnsSource: global___ClientPayload.DNSSource | None = ...,
        connectAttemptCount: builtins.int | None = ...,
        device: builtins.int | None = ...,
        devicePairingData: global___ClientPayload.DevicePairingRegistrationData | None = ...,
        product: global___ClientPayload.Product.ValueType | None = ...,
        fbCat: builtins.bytes | None = ...,
        fbUserAgent: builtins.bytes | None = ...,
        oc: builtins.bool | None = ...,
        lc: builtins.int | None = ...,
        iosAppExtension: global___ClientPayload.IOSAppExtension.ValueType | None = ...,
        fbAppID: builtins.int | None = ...,
        fbDeviceID: builtins.bytes | None = ...,
        pull: builtins.bool | None = ...,
        paddingBytes: builtins.bytes | None = ...,
        yearClass: builtins.int | None = ...,
        memClass: builtins.int | None = ...,
        interopData: global___ClientPayload.InteropData | None = ...,
        trafficAnonymization: global___ClientPayload.TrafficAnonymization.ValueType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["connectAttemptCount", b"connectAttemptCount", "connectReason", b"connectReason", "connectType", b"connectType", "device", b"device", "devicePairingData", b"devicePairingData", "dnsSource", b"dnsSource", "fbAppID", b"fbAppID", "fbCat", b"fbCat", "fbDeviceID", b"fbDeviceID", "fbUserAgent", b"fbUserAgent", "interopData", b"interopData", "iosAppExtension", b"iosAppExtension", "lc", b"lc", "memClass", b"memClass", "oc", b"oc", "paddingBytes", b"paddingBytes", "passive", b"passive", "product", b"product", "pull", b"pull", "pushName", b"pushName", "sessionID", b"sessionID", "shortConnect", b"shortConnect", "trafficAnonymization", b"trafficAnonymization", "userAgent", b"userAgent", "username", b"username", "webInfo", b"webInfo", "yearClass", b"yearClass"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["connectAttemptCount", b"connectAttemptCount", "connectReason", b"connectReason", "connectType", b"connectType", "device", b"device", "devicePairingData", b"devicePairingData", "dnsSource", b"dnsSource", "fbAppID", b"fbAppID", "fbCat", b"fbCat", "fbDeviceID", b"fbDeviceID", "fbUserAgent", b"fbUserAgent", "interopData", b"interopData", "iosAppExtension", b"iosAppExtension", "lc", b"lc", "memClass", b"memClass", "oc", b"oc", "paddingBytes", b"paddingBytes", "passive", b"passive", "product", b"product", "pull", b"pull", "pushName", b"pushName", "sessionID", b"sessionID", "shards", b"shards", "shortConnect", b"shortConnect", "trafficAnonymization", b"trafficAnonymization", "userAgent", b"userAgent", "username", b"username", "webInfo", b"webInfo", "yearClass", b"yearClass"]) -> None: ...

global___ClientPayload = ClientPayload

@typing.final
class HandshakeMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class ClientFinish(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        STATIC_FIELD_NUMBER: builtins.int
        PAYLOAD_FIELD_NUMBER: builtins.int
        static: builtins.bytes
        payload: builtins.bytes
        def __init__(
            self,
            *,
            static: builtins.bytes | None = ...,
            payload: builtins.bytes | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["payload", b"payload", "static", b"static"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["payload", b"payload", "static", b"static"]) -> None: ...

    @typing.final
    class ServerHello(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        EPHEMERAL_FIELD_NUMBER: builtins.int
        STATIC_FIELD_NUMBER: builtins.int
        PAYLOAD_FIELD_NUMBER: builtins.int
        ephemeral: builtins.bytes
        static: builtins.bytes
        payload: builtins.bytes
        def __init__(
            self,
            *,
            ephemeral: builtins.bytes | None = ...,
            static: builtins.bytes | None = ...,
            payload: builtins.bytes | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["ephemeral", b"ephemeral", "payload", b"payload", "static", b"static"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["ephemeral", b"ephemeral", "payload", b"payload", "static", b"static"]) -> None: ...

    @typing.final
    class ClientHello(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        EPHEMERAL_FIELD_NUMBER: builtins.int
        STATIC_FIELD_NUMBER: builtins.int
        PAYLOAD_FIELD_NUMBER: builtins.int
        ephemeral: builtins.bytes
        static: builtins.bytes
        payload: builtins.bytes
        def __init__(
            self,
            *,
            ephemeral: builtins.bytes | None = ...,
            static: builtins.bytes | None = ...,
            payload: builtins.bytes | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["ephemeral", b"ephemeral", "payload", b"payload", "static", b"static"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["ephemeral", b"ephemeral", "payload", b"payload", "static", b"static"]) -> None: ...

    CLIENTHELLO_FIELD_NUMBER: builtins.int
    SERVERHELLO_FIELD_NUMBER: builtins.int
    CLIENTFINISH_FIELD_NUMBER: builtins.int
    @property
    def clientHello(self) -> global___HandshakeMessage.ClientHello: ...
    @property
    def serverHello(self) -> global___HandshakeMessage.ServerHello: ...
    @property
    def clientFinish(self) -> global___HandshakeMessage.ClientFinish: ...
    def __init__(
        self,
        *,
        clientHello: global___HandshakeMessage.ClientHello | None = ...,
        serverHello: global___HandshakeMessage.ServerHello | None = ...,
        clientFinish: global___HandshakeMessage.ClientFinish | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["clientFinish", b"clientFinish", "clientHello", b"clientHello", "serverHello", b"serverHello"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["clientFinish", b"clientFinish", "clientHello", b"clientHello", "serverHello", b"serverHello"]) -> None: ...

global___HandshakeMessage = HandshakeMessage
