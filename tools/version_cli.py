from colorama import init
import argparse
from .version import Version
from .github import Github

init()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    cmd = args.add_subparsers(title="cmd", dest="cmd", required=True)
    args.add_argument("--set-url", type=str, help="change github release url")
    cmd.add_parser("info")
    update = cmd.add_parser("update")
    update_type = update.add_subparsers(
        title="type", dest="update_type", required=True)
    update_type.add_parser("major")
    update_type.add_parser("minor")
    update_type.add_parser("patch")
    update_type.add_parser("post")
    nz = cmd.add_parser("neonize")
    neonize_version = nz.add_argument_group("version value")
    neonize_version.add_argument("--set-version", type=str)
    neonize_version.add_argument("--last", action="store_true")
    neonize_version.add_argument("--pypi-format", action="store_true")
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
            github = Github()
            if parse.set_version:
                version.neonize = parse.set_version
                print(version.neonize)
            elif parse.last:
                version.neonize = github.get_last_version()
                print(version.neonize)
            elif parse.pypi_format:
                print(version.version_pypi_standard)
            else:
                print(version.neonize)
        case "goneonize":
            version = Version()
            github = Github()
            if parse.last:
                version.goneonize = ".".join(
                    github.get_last_goneonize_version().split("."))
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
                case "post":
                    version.update_post()
            print(version.neonize)
