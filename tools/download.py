from colorama import Fore, init
import argparse
from pathlib import Path
import httpx
import asyncio
import sys
import platform
import requests
from tqdm import tqdm

sys.path.insert(0, Path(__file__).parent.__str__())
from goneonize import generated_name
from versioning import Version

os_name = platform.system().lower()
arch_name = platform.machine().lower()
init()


class UnsupportedPlatform(Exception):
    pass


def download(
    version: str,
    os: str,
    arch: str,
    chunk_size: int,
    path=Path(__file__).parent.parent / "neonize",
):
    name = (Path(__file__).parent.parent / "neonize") / generated_name(
        os_name, arch_name
    )
    print(
        f"{Fore.RED}[{Fore.GREEN}{name.name} {Fore.YELLOW}%r{Fore.RED}]{Fore.RESET}"
        % version
    )
    resp = requests.get(
        f"https://github.com/krypton-byte/neonize/releases/download/{version}/{generated_name(os_name, arch_name)}",
        stream=True,
    )
    if resp.status_code != 200:
        resp.close()
        raise UnsupportedPlatform(generated_name())
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


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("--os", default=os_name)
    arg.add_argument("--arch", default=arch_name)
    arg.add_argument("--version", type=str, help="last version as default")
    arg.add_argument("--chunk-size", type=int, help="default: 1024", default=1024)
    parse = arg.parse_args()
    if parse.version:
        version = parse.version
    else:
        version = Version.get_last_goneonize_release()
    download(version, parse.os, parse.arch, parse.chunk_size)
