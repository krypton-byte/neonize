from enum import Enum
from pathlib import Path
import shutil
import subprocess
import os
import platform

WORKDIR = Path(__file__).parent.parent
fname = "-".join(["neonize", os.popen("uv run task version neonize --pypi-format").read().strip()])
wheel_name = fname + "-py3-none-any.whl"
os_name = os.environ.get("GOOS") or platform.system().lower()
arch_name = os.environ.get("GOARCH") or platform.machine().lower()
arch_name = {
    "aarch64": "arm64",
    "x86_64": "amd64",
}.get(arch_name, arch_name)


class OS(Enum):
    MAC = "macosx"
    LINUX = "manylinux2014"
    WINDOWS = "win"

    # ANDROID = "android"
    @classmethod
    def auto(cls):
        if os_name == "windows":
            return cls.WINDOWS
        elif os_name == "linux":
            return cls.LINUX
        elif os_name == "darwin":
            return cls.MAC
        raise OSError(
            "The binary for your operating system is not yet available. Please check back later. If you need immediate assistance, you can also contact the author of the library for support."
        )


class ARCH(Enum):
    X86_64 = "x86_64"
    X86 = "x86"
    AMD64 = "amd64"
    AARCH64 = "aarch64"
    I386 = "i686"
    S390X = "s390x"
    ARM = "armv7l"
    ARM64 = "arm64"
    RISCV64 = "riscv64"

    @classmethod
    def auto(cls, os: OS):
        if arch_name == "arm64":
            if os in [OS.MAC, OS.WINDOWS]:
                return cls.ARM64
            return cls.AARCH64
        elif arch_name == "amd64":
            if os == OS.WINDOWS:
                return cls.AMD64
            return cls.X86_64
        elif arch_name == "386":
            if os == OS.WINDOWS:
                return cls.X86
            return cls.I386
        elif arch_name == "arm":
            return cls.ARM
        elif arch_name == "s390x":
            return cls.S390X
        raise OSError("Unsupported architecture")


def repack(_os: OS, arch: ARCH):
    try:
        subprocess.call(["wheel", "unpack", WORKDIR / "dist" / wheel_name], cwd=WORKDIR / "dist")
        wheel_path = WORKDIR / "dist" / fname / (fname + ".dist-info") / "WHEEL"
        wheel = open(wheel_path, "r").read()
        arch_value = arch.value
        if _os == OS.MAC:
            arch_value = f"12_0_{arch_value}"
        with open(wheel_path, "w") as file:
            if _os == OS.WINDOWS and arch == ARCH.X86:
                file.write(wheel.replace("py3-none-any", "py310-none-win32"))
                print(wheel.replace("py3-none-any", "py310-none-win32"))
            else:
                file.write(wheel.replace("py3-none-any", f"py310-none-{_os.value}_{arch_value}"))
                print(wheel.replace("py3-none-any", f"py310-none-{_os.value}_{arch_value}"))
        subprocess.call(["wheel", "pack", WORKDIR / "dist" / fname], cwd=WORKDIR / "dist")
        os.remove(WORKDIR / "dist" / wheel_name)
        os.remove(WORKDIR / "dist" / (fname + ".tar.gz"))
        shutil.rmtree(WORKDIR / "dist" / fname)
    except FileNotFoundError:
        print("general wheel file not found\nhint: uv build")


if __name__ == "__main__":
    _os = OS.auto()
    repack(_os, ARCH.auto(_os.auto()))
