from .version import Version
from goneonize import generated_name
from colorama import Fore, init
import argparse
from pathlib import Path
import sys
import platform
import requests
from tqdm import tqdm

from .github import Github

sys.path.insert(0, Path(__file__).parent.__str__())

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
    name = (Path(__file__).parent.parent / "neonize") / \
        generated_name(os_name, arch_name)
    print(
        f"{Fore.RED}[{Fore.GREEN}{name.name} {Fore.YELLOW}%r{Fore.RED}]{Fore.RESET}" %
        version)
    username, repository = Version().github_url.split("/")[-2:]
    resp = requests.get(
        f"https://github.com/{username}/{repository}/releases/download/{version}/{generated_name(os_name, arch_name)}",
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
    version = arg.add_mutually_exclusive_group(required=True)
    version.add_argument("--last", action="store_true")
    version.add_argument("--version", type=str, help="goneonize version")
    arg.add_argument(
        "--chunk-size",
        type=int,
        help="default: 1024",
        default=1024)
    parse = arg.parse_args()
    github = Github()
    if parse.version:
        target_version = parse.version
    else:
        target_version = github.get_last_goneonize_version()
    download(target_version, parse.os, parse.arch, parse.chunk_size)
