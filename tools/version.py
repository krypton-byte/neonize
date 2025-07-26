from colorama import init, Fore
from pathlib import Path
import re

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

    def update_post_semantic(self, version: str):
        version_semantic = [int(i) for i in version.split(".")]
        if len(version_semantic) < 4:
            version_semantic.append(0)
        version_semantic[3] += 1
        return ".".join(map(str, version_semantic))

    def update_patch_semantic(self, version: str):
        version_semantic = [int(i) for i in version.split(".")][:3]
        version_semantic[2] += 1
        return ".".join(map(str, version_semantic))

    def update_minor_semantic(self, version: str):
        version_semantic = [int(i) for i in version.split(".")][:3]
        version_semantic[1] += 1
        version_semantic[2] = 0
        return ".".join(map(str, version_semantic))

    def update_major_semantic(self, version: str):
        version_semantic = [int(i) for i in version.split(".")][:3]
        version_semantic[0] += 1
        version_semantic[1] = 0
        version_semantic[2] = 0
        return ".".join(map(str, version_semantic))

    def update_post(self):
        neonize = self.update_post_semantic(self.neonize)
        parts = neonize.split(".")
        if len(parts) > 3:
            parts[-1] = f"post{parts[-1]}"
        self.neonize = ".".join(parts)
        goneonize = self.update_post_semantic(self.goneonize)
        self.goneonize = goneonize

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

    @property
    def github_url(self) -> str:
        return ValueChanger(open(self.GO_PY_PATH, "r").read()
                            ).extract("__GIT_RELEASE_URL__", str)

    @github_url.setter
    def github_url(self, url: str) -> None:
        changer = ValueChanger(open(self.GO_PY_PATH).read())
        modified = changer.set_value("__GIT_RELEASE_URL__", url).text
        with open(self.GO_PY_PATH, "w") as file:
            file.write(modified)

    @property
    def neonize(self):
        return ".".join(
            re.findall(
                r"\d+", ValueChanger(open(self.PY_PATH, "r").read()
                                     ).extract("__version__", str)
            )
        )

    @neonize.setter
    def neonize(self, new_version: str):
        modified = (
            ValueChanger(
                open(
                    self.PY_PATH,
                    "r").read()).set_value(
                "__version__",
                new_version).text
        )
        with open(self.PY_PATH, "w") as file:
            file.write(modified)
            self.__neonize = new_version

    @property
    def goneonize(self):
        return ".".join(
            re.findall(
                r"\d+",
                re.findall(
                    self.GO_RE,
                    open(
                        self.GO_PATH,
                        "r").read())[0])
        )

    @property
    def version_pypi_standard(self):
        parts = self.neonize.split(".")
        if len(parts) > 3:
            parts[-1] = f"post{parts[-1]}"
        return ".".join(parts)

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
        modified = (
            ValueChanger(open(self.GO_PY_PATH, "r").read())
            .set_value("__GONEONIZE_VERSION__", new_version)
            .text
        )
        with open(self.GO_PY_PATH, "w") as gopy_path:
            gopy_path.write(modified)

    def __repr__(self):
        neonize = [int(i) for i in self.neonize.split(".")]
        neonize.append(0)
        neonize_str = ".".join(list(map(str, neonize))[:3])
        if neonize[3]:
            neonize_str += f".post{neonize[3]}"
        goneonize = [int(i) for i in self.goneonize.split(".")]
        goneonize.append(0)
        goneonize_str = ".".join(list(map(str, neonize))[:3])
        if goneonize[3]:
            goneonize_str += f".post{goneonize[3]}"
        pre = (
            f"{Fore.RED}[{Fore.GREEN}neonize {Fore.YELLOW}%r {Fore.RED}<> {Fore.GREEN}goneonize {Fore.YELLOW}%r{Fore.RED}]{Fore.RESET}"
            % (neonize_str, goneonize_str)
        )
        post = f"""{pre}
{Fore.RED}├── {Fore.GREEN}URL: {Fore.YELLOW}{self.github_url}
{Fore.RED}├── {Fore.GREEN}neonize
{Fore.RED}│   ├── {Fore.BLUE}major {Fore.YELLOW}%s
{Fore.RED}│   ├── {Fore.BLUE}minor {Fore.YELLOW}%s
{Fore.RED}│   └── {Fore.BLUE}patch {Fore.YELLOW}%s
{Fore.RED}│   └── {Fore.BLUE}post  {Fore.YELLOW}%s
{Fore.RED}└── {Fore.GREEN}goneonize
{Fore.RED}    ├── {Fore.BLUE}major {Fore.YELLOW}%s
{Fore.RED}    ├── {Fore.BLUE}minor {Fore.YELLOW}%s
{Fore.RED}    ├── {Fore.BLUE}patch {Fore.YELLOW}%s
{Fore.RED}    └── {Fore.BLUE}post  {Fore.YELLOW}%s{Fore.RESET}

""" % (*neonize[:4], *goneonize[:4])
        return post
