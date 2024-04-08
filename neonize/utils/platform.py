import os
from typing import Dict
import platform


def arch_normalizer(arch_: str) -> str:
    arch: Dict[str, str] = {
        "aarch64": "arm64",
        "x86_64": "amd64",
    }
    return arch.get(arch_, arch_)


def generated_name(os_name="", arch_name=""):
    os_name = os_name or platform.system().lower()
    arch_name = arch_normalizer(arch_name or platform.machine().lower())
    if os_name == "windows":
        ext = "dll"
    elif os_name == "linux":
        is_android = "android" in os.popen("uname -a").read().strip().lower()
        if is_android:
            os_name = "android"
        ext = "so"
    elif os_name == "darwin":
        ext = "dylib"
    else:
        ext = "so"
    return f"neonize-{os_name}-{arch_name}.{ext}"
