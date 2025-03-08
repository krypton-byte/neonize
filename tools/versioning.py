import httpx
from colorama import init, Fore
import argparse
from pathlib import Path
import re

from tools import goneonize

from .value_changer import ValueChanger


init()


class Version:
    PY_PATH = Path(__file__).parent.parent / "neonize/__init__.py"
    PY_RE = r"__version__ = \"([\w\d\.]+)\""
    GO_PATH = Path(__file__).parent.parent / "goneonize/version.go"
    GO_RE = r"version \:\= \"([\w\d\.]+)\""
    GO_PY_PATH = Path(__file__).parent.parent / "neonize/download.py"
    GO_PY_RE = r"__GONEONIZE_VERSION__ = \"([\w\d\.]+)\""
    GO_GITHUB_RE = r"__GIT_RELEASE_URL__ = \"([\w\d\.\-\/\:]+)\""

    def __init__(self):
        self.__neonize = self.neonize
        self.__goneonize = self.goneonize

    def set_neonize_only(self, neonize_version: str):
        self.neonize = neonize_version
        self.goneonize = self.get_last_goneonize_release()
    
    def update_patch_semantic(self, version: str):
        version_semantic = [int(i) for i in version.split('.')]
        version_semantic[2] += 1
        return '.'.join(map(str, version_semantic))
    def update_minor_semantic(self, version: str):
        version_semantic = [int(i) for i in version.split('.')]
        version_semantic[1] += 1
        version_semantic[2] = 0
        return '.'.join(map(str, version_semantic))
    def update_major_semantic(self, version: str):
        version_semantic = [int(i) for i in version.split('.')]
        version_semantic[0] += 1
        version_semantic[1] = 0
        version_semantic[2] = 0
        return '.'.join(map(str, version_semantic))
    def update_patch(self):
        neonize = self.update_patch_semantic(self.neonize)
        self.neonize = neonize
        goneonize = self.update_patch_semantic(self.goneonize)
        self.goneonize = goneonize
    def update_minor(self):
        neonize = self.update_minor_semantic(self.neonize)
        self.neonize = neonize
        goneonize = self.update_minor_semantic(self.goneonize)
        self.goneonize = goneonize
    def update_major(self):
        neonize = self.update_major_semantic(self.neonize)
        self.neonize = neonize
        goneonize = self.update_major_semantic(self.goneonize)
        self.goneonize = goneonize
    @staticmethod
    def get_last_goneonize_release() -> str:
        with httpx.Client() as client:
            r = client.get("https://api.github.com/repos/krypton-byte/neonize/releases")
            return r.json()[0]["tag_name"]
    @property
    def github_url(self) -> str:
        return ValueChanger(open(self.GO_PY_PATH, "r").read()).extract('__GIT_RELEASE_URL__', str)
    
    @github_url.setter
    def github_url(self, url: str) -> None:
        changer = ValueChanger(open(self.GO_PY_PATH).read())
        modified = changer.set_value('__GIT_RELEASE_URL__', url).text
        with open(self.GO_PY_PATH, "w") as file:
            file.write(modified)
    @property
    def neonize(self):
        return ValueChanger(open(self.PY_PATH, "r").read()).extract('__version__', str)

    @neonize.setter
    def neonize(self, new_version: str):
        modified = ValueChanger(open(self.PY_PATH, "r").read()).set_value('__version__', new_version).text
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
        modified = ValueChanger(open(self.GO_PY_PATH, "r").read()).set_value('__GONEONIZE_VERSION__', new_version).text
        with open(self.GO_PY_PATH, "w") as gopy_path:
            gopy_path.write(modified)

    def __repr__(self):
        pre = (
            f"{Fore.RED}[{Fore.GREEN}neonize {Fore.YELLOW}%r {Fore.RED}<> {Fore.GREEN}goneonize {Fore.YELLOW}%r{Fore.RED}]{Fore.RESET}"
            % (self.__neonize, self.__goneonize)
        )
        post = f"""{pre}
{Fore.RED}├── {Fore.GREEN}URL: {Fore.YELLOW}{self.github_url}
{Fore.RED}├── {Fore.GREEN}neonize
{Fore.RED}│   ├── {Fore.BLUE}major {Fore.YELLOW}%s
{Fore.RED}│   ├── {Fore.BLUE}minor {Fore.YELLOW}%s
{Fore.RED}│   └── {Fore.BLUE}patch {Fore.YELLOW}%s
{Fore.RED}└── {Fore.GREEN}goneonize
{Fore.RED}    ├── {Fore.BLUE}major {Fore.YELLOW}%s
{Fore.RED}    ├── {Fore.BLUE}minor {Fore.YELLOW}%s
{Fore.RED}    └── {Fore.BLUE}patch {Fore.YELLOW}%s{Fore.RESET}

""" % (*self.neonize.split("."), *self.goneonize.split("."))
        return post


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    cmd = args.add_subparsers(title="cmd", dest="cmd", required=True)
    args.add_argument('--set-url', type=str, help='change github release url')
    cmd.add_parser("info")
    update = cmd.add_parser("update")
    update_type = update.add_subparsers(title="type", dest="update_type", required=True)
    update_type.add_parser("major")
    update_type.add_parser("minor")
    update_type.add_parser("patch")
    nz = cmd.add_parser("neonize")
    nz.add_argument("--set-version", type=str)
    gz = cmd.add_parser("goneonize")
    gz_group = gz.add_argument_group("version value")
    mutual = gz_group.add_mutually_exclusive_group()
    mutual.add_argument("--last", action="store_true")
    mutual.add_argument("--set-version", type=str)
    parse = args.parse_args()
    if parse.set_url:
        version = Version()
        version.github_url = parse.set_url
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
        case "update":
            update_type = parse.update_type
            version = Version()
            match update_type:
                case "major":
                    version.update_major()
                case "minor":
                    version.update_minor()
                case "patch":
                    version.update_patch()
