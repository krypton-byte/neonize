import httpx
from colorama import init, Fore
import argparse
from pathlib import Path
import re


init()


class Version:
    PY_PATH = Path(__file__).parent.parent / "neonize/__init__.py"
    PY_RE = r"__version__ = \"([\w\d\.]+)\""
    GO_PATH = Path(__file__).parent.parent / "goneonize/version.go"
    GO_RE = r"version \:\= \"([\w\d\.]+)\""
    GO_PY_PATH = Path(__file__).parent.parent / "neonize/download.py"
    GO_PY_RE = r"__GONEONIZE_VERSION__ = \"([\w\d\.]+)\""

    def __init__(self):
        self.__neonize = self.neonize
        self.__goneonize = self.goneonize

    def set_neonize_only(self, neonize_version: str):
        self.neonize = neonize_version
        self.goneonize = self.get_last_goneonize_release()

    @staticmethod
    def get_last_goneonize_release() -> str:
        with httpx.Client() as client:
            r = client.get("https://api.github.com/repos/krypton-byte/neonize/releases")
            return r.json()[0]["tag_name"]

    @property
    def neonize(self):
        return re.findall(self.PY_RE, open(self.PY_PATH, "r").read())[0]

    @neonize.setter
    def neonize(self, new_version: str):
        modified = re.sub(
            self.PY_RE,
            '__version__ = "%s"' % new_version,
            open(self.PY_PATH, "r").read(),
            count=1,
        )
        with open(self.PY_PATH, "w") as file:
            file.write(modified)
            self.__neonize = new_version

    @property
    def goneonize(self):
        return re.findall(self.GO_RE, open(self.GO_PATH, "r").read())[0]

    @goneonize.setter
    def goneonize(self, new_version: str):
        modified = re.sub(
            self.GO_RE,
            'version := "%s"' % new_version,
            open(self.GO_PATH, "r").read(),
            count=1,
        )
        with open(self.GO_PATH, "w") as file:
            file.write(modified)
            self.__goneonize = new_version
            modified = re.sub(
                self.GO_PY_RE,
                '__GONEONIZE_VERSION__ = "%s"' % new_version,
                open(self.GO_PY_PATH, "r").read(),
            )
            with open(self.GO_PY_PATH, "w") as gopy_path:
                gopy_path.write(modified)

    def __repr__(self):
        pre = (
            f"{Fore.RED}[{Fore.GREEN}neonize {Fore.YELLOW}%r {Fore.RED}<> {Fore.GREEN}goneonize {Fore.YELLOW}%r{Fore.RED}]{Fore.RESET}"
            % (self.__neonize, self.__goneonize)
        )
        post = f"""{pre}
{Fore.RED}├── {Fore.GREEN}neonize
{Fore.RED}│   ├── {Fore.BLUE}major {Fore.YELLOW}%s
{Fore.RED}│   ├── {Fore.BLUE}minor {Fore.YELLOW}%s
{Fore.RED}│   └── {Fore.BLUE}patch {Fore.YELLOW}%s
{Fore.RED}└── {Fore.GREEN}goneonize
{Fore.RED}    ├── {Fore.BLUE}major {Fore.YELLOW}%s
{Fore.RED}    ├── {Fore.BLUE}minor {Fore.YELLOW}%s
{Fore.RED}    └── {Fore.BLUE}patch {Fore.YELLOW}%s{Fore.RESET}

""" % (*self.__neonize.split("."), *self.__goneonize.split("."))
        return post


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    cmd = args.add_subparsers(title="cmd", dest="cmd", required=True)
    cmd.add_parser("info")
    nz = cmd.add_parser("neonize")
    nz.add_argument("--set-version", type=str)
    gz = cmd.add_parser("goneonize")
    gz_group = gz.add_argument_group("version value")
    mutual = gz_group.add_mutually_exclusive_group()
    mutual.add_argument("--last", action="store_true")
    mutual.add_argument("--set-version", type=str)
    parse = args.parse_args()
    match parse.cmd:
        case "info":
            print(Version())
        case "neonize":
            version = Version()
            if parse.set_version:
                version.neonize = parse.set_version
            print(version.neonize)
        case "goneonize":
            version = Version()
            if parse.last:
                version.goneonize = version.get_last_goneonize_release()
            elif parse.set_version:
                version.goneonize = parse.set_version
            print(version.goneonize)
