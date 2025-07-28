from typing import Optional
from colorama import Fore, init
import shutil
from pathlib import Path
import os
import platform
import requests
from tqdm import tqdm
import zipfile
from dataclasses import dataclass
import argparse


os_name = platform.system().lower()
arch_name = platform.machine().lower()
init()

WORKDIR = Path(__file__).parent.parent
SHA_FILE = WORKDIR / "goneonize/defproto/.sha"


@dataclass
class FileValue:
    proto: int = 0
    dropped: int = 0
    folder: int = 0


@dataclass
class ProtoCommit:
    upgradeable: bool
    sha: Optional[str]


def remove_not_proto(path: Path, value: FileValue):
    for file in path.iterdir():
        if file.is_dir():
            value.folder += 1
            remove_not_proto(file, value)
        elif not file.name.endswith(".proto"):
            os.remove(file)
            value.dropped += 1
        else:
            value.proto += 1


class UnsupportedPlatform(Exception):
    pass


def download_whatsmeow():
    chunk_size = 1024
    name = WORKDIR / "whatsmeow.zip"
    print(
        f"{Fore.RED}[{Fore.GREEN}{name.name} {Fore.YELLOW}'HEAD'{Fore.RED}]{Fore.RESET}")
    resp = requests.get(
        "https://github.com/tulir/whatsmeow/archive/refs/heads/main.zip", stream=True
    )
    total = int(resp.headers.get("content-length", 0))
    with (
        open(name, "wb") as file,
        tqdm(
            desc=Path(name).name,
            total=total,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar,
    ):
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)
        bar.n = total
    bar.close()
    # unzip
    with zipfile.ZipFile("whatsmeow.zip") as zfile:
        for name in filter(lambda x: x.startswith(
                "whatsmeow-main/proto"), zfile.namelist()):
            zfile.extract(name, ".dest")
    # remove != .proto
    value = FileValue()
    remove_not_proto(Path(__file__).parent.parent / ".dest", value)
    print(f"{Fore.BLUE}[INFO] File extraction complete:")
    print(f"{Fore.RED}  - {Fore.GREEN}{value.folder} {Fore.YELLOW}folders created")
    print(f"{Fore.RED}  - {Fore.GREEN}{value.dropped}{Fore.YELLOW} files skipped/dropped")
    # remove defproto
    shutil.rmtree(WORKDIR / "goneonize/defproto/")
    shutil.move(
        WORKDIR /
        ".dest/whatsmeow-main/proto",
        WORKDIR /
        "goneonize/defproto")
    shutil.copy(
        WORKDIR /
        "goneonize/Neonize.proto",
        WORKDIR /
        "goneonize/defproto/")
    print(
        f"{Fore.RED}  - {Fore.GREEN}{value.proto} {Fore.YELLOW}proto files processed and moved to 'defproto'"
    )
    os.remove(WORKDIR / "whatsmeow.zip")
    shutil.rmtree(WORKDIR / ".dest")
    print(f"{Fore.BLUE}[INFO] Work directory cleaned up successfully.")
    git_proto_sha = ""
    last_sha_commit = requests.get(
        "https://api.github.com/repos/tulir/whatsmeow/contents/").json()
    for result in filter(
            lambda item: item["name"] == "proto", last_sha_commit):
        git_proto_sha = result["sha"]
        break
    with open(SHA_FILE, "w") as file:
        file.write(git_proto_sha)


def upgradable() -> ProtoCommit:
    git_proto_sha = ""
    last_sha_commit = requests.get(
        "https://api.github.com/repos/tulir/whatsmeow/contents/").json()
    for result in filter(
            lambda item: item["name"] == "proto", last_sha_commit):
        git_proto_sha = result["sha"]
        break
    if SHA_FILE.exists():
        return ProtoCommit(
            upgradeable=SHA_FILE.read_text().strip() != git_proto_sha, sha=git_proto_sha
        )
    else:
        SHA_FILE.touch()
    return ProtoCommit(upgradeable=True, sha=None)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--force",
        help="force update",
        default=False,
        action="store_true")
    parse = args.parse_args()
    proto = upgradable()
    if proto.upgradeable:
        print(f"{Fore.BLUE}[INFO] A proto update is available.")
    if proto.upgradeable or parse.force:
        download_whatsmeow()
    else:
        print(f"{Fore.BLUE}[INFO] No proto update is available.")
