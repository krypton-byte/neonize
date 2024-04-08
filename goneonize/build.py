import os
import platform
import shlex
import argparse
import subprocess
import re
import shutil
from pathlib import Path
from typing import Dict

cwd = os.path.dirname(__file__)
shell = [
    "protoc --go_out=. Neonize.proto def.proto",
    "protoc --python_out=../neonize/proto --mypy_out=../neonize/proto def.proto Neonize.proto",
    "protoc --go_out=. --go-grpc_out=. -I . Neonize.proto def.proto",
]


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
        ext = "so"
    elif os_name == "darwin":
        ext = "dylib"
    else:
        ext = "so"
    return f"neonize-{os_name}-{arch_name}.{ext}"


def __build():
    args = argparse.ArgumentParser()
    args.add_argument("--os", default=platform.system().lower())
    args.add_argument("--arch", default=platform.machine().lower())
    parse = args.parse_args()
    filename = generated_name(parse.os, parse.arch)
    for sh in shell:
        subprocess.call(shlex.split(sh), cwd=cwd)
    if (Path(cwd) / "defproto").exists():
        shutil.rmtree(f"{cwd}/defproto")
    os.mkdir(f"{cwd}/defproto")
    os.rename(f"{cwd}/github.com/krypton-byte/neonize/defproto/", f"{cwd}/defproto")
    shutil.rmtree(f"{cwd}/github.com")
    subprocess.call(
        shlex.split(f"go build -buildmode=c-shared -ldflags=-s -o {filename} main.go"),
        cwd=cwd,
        env=os.environ.update({"CGO_ENABLED": "1"}),
    )
    if (Path(cwd).parent / filename).exists():
        os.remove(os.path.dirname(cwd) + "/" + filename)
    os.rename(f"{cwd}/{filename}", os.path.dirname(cwd) + "/" + filename)


def build_proto():
    for sh in shell:
        subprocess.call(shlex.split(sh), cwd=cwd)
    if (Path(cwd) / "defproto").exists():
        shutil.rmtree(f"{cwd}/defproto")
    os.mkdir(f"{cwd}/defproto")
    os.rename(f"{cwd}/github.com/krypton-byte/neonize/defproto/", f"{cwd}/defproto")
    shutil.rmtree(f"{cwd}/github.com")


def build_neonize():
    os_name = os.environ.get("GOOS") or platform.system().lower()
    arch_name = os.environ.get("GOARCH") or platform.machine().lower()
    print(f"os: {os_name}, arch: {arch_name}")
    filename = generated_name(os_name, arch_name)
    print(filename)
    subprocess.call(
        shlex.split(f"go build -buildmode=c-shared -ldflags=-s -o {filename} "),
        cwd=cwd,
        env=os.environ.update({"CGO_ENABLED": "1"}),
    )
    if (Path(cwd).parent / f"neonize/{filename}").exists():
        os.remove(os.path.dirname(cwd) + "/neonize/" + filename)
    os.rename(f"{cwd}/{filename}", os.path.dirname(cwd) + "/neonize/" + filename)


def set_version():
    args = argparse.ArgumentParser()
    args.add_argument("version", nargs=1, type=str)
    parse = args.parse_args()
    subprocess.call(["poetry", "version", parse.version[0]], cwd=cwd, env=os.environ)
    with open(cwd + "/version.go", "r") as file:
        new_code = re.sub(r'"([\d\.]+)"', f'"{parse.version[0]}"', file.read())
        with open(cwd + "/version.go", "w") as f:
            f.write(new_code)


def build():
    args = argparse.ArgumentParser()
    sub = args.add_subparsers(dest="build", required=True)
    sub.add_parser("goneonize")
    sub.add_parser("proto")
    sub.add_parser("all")
    parse = args.parse_args()
    match parse.build:
        case "goneonize":
            build_neonize()
        case "proto":
            build_proto()
        case "all":
            build_proto()
            build_neonize()


def build_android():
    filename = generated_name("android", "aarch4")
    for sh in shell:
        subprocess.call(shlex.split(sh), cwd=cwd)
    if (Path(cwd) / "defproto").exists():
        shutil.rmtree(f"{cwd}/defproto")
    os.mkdir(f"{cwd}/defproto")
    os.rename(f"{cwd}/github.com/krypton-byte/neonize/defproto/", f"{cwd}/defproto")
    shutil.rmtree(f"{cwd}/github.com")
    os.environ.update(
        {
            "CGO_ENABLED": "1",
            "CC": "/home/krypton-byte/Pictures/android-ndk-r26b/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android28-clang",
            "CXX": "/home/krypton-byte/Pictures/android-ndk-r26b/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android28-clang++",
        }
    )
    subprocess.call(
        shlex.split(f"go build -buildmode=c-shared -ldflags=-s -o {filename} main.go"),
        cwd=cwd,
        env=os.environ,
    )
    if (Path(cwd).parent / filename).exists():
        os.remove(os.path.dirname(cwd) + "/" + filename)
    os.rename(f"{cwd}/{filename}", os.path.dirname(cwd) + "/" + filename)
    # command = shlex.split("build.bat " if os.name == "nt" else "bash build.sh "+platform.machine())
    # subprocess.call(
    #     command,
    #     cwd=os.path.dirname(__file__),
    #     env=os.environ.update({"build_neonize": "1"}),
    #     shell=os.name == "nt",
    # )
