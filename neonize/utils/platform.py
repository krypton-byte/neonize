import os
import platform
import shutil
import sys
from typing import Dict


def arch_normalizer(arch_: str) -> str:
    """
    Normalizes architecture names to a standardized format.

    :param arch_: The architecture name to be normalized.
    :type arch_: str
    :return: The normalized architecture name.
    :rtype: str
    """
    arch: Dict[str, str] = {
        "aarch64": "arm64",
        "x86_64": "amd64",
    }
    return arch.get(arch_, arch_)


def generated_name(os_name="", arch_name=""):
    """
    Generates a standardized filename based on the operating system and architecture.

    :param os_name: The name of the operating system, defaults to an empty string.
    :type os_name: str, optional
    :param arch_name: The name of the architecture, defaults to an empty string.
    :type arch_name: str, optional
    :return: The generated filename.
    :rtype: str
    """
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


def is_executable_installed(executable_name: str) -> bool:
    """
    Checks if an executable is available in the system's PATH.
    Args:
        executable_name: Name of the executable to find
    Returns:
        True if executable is found in PATH, False otherwise
    """
    # Handle Windows executable extensions
    if sys.platform.startswith("win"):
        # Check both with and without .exe extension
        for ext in (".exe", ".bat", ".cmd", ""):
            if shutil.which(executable_name + ext) is not None:
                return True
        return False

    # Unix-based systems (Linux/macOS)
    return shutil.which(executable_name) is not None
