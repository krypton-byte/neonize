from io import BytesIO
import os
import sys
from .github import Github
from zipfile import ZipFile
from hashlib import md5
from pathlib import Path
import glob

goneonize = Path(__file__).parent.parent / "goneonize"


def get_diff():
    ignore = ["goneonize/defproto", "goneonize/go.mod", "goneonize/go.sum"]
    file_paths = glob.glob("goneonize/**/*", recursive=True)
    files = []
    for file in file_paths:
        if (
            os.path.isfile(file)
            and not file.startswith("goneonize/defproto")
            and not file.startswith("goneonize/neonize")
            and "__pycache__" not in file
            and file not in ignore
        ):
            files.append(file)
    files.append("goneonize/defproto/.sha")
    files.remove("goneonize/version.go")
    return files


def get_current_md5():
    data = get_diff()
    result = {}
    for file in data:
        with open(Path(__file__).parent.parent / file, "rb") as fd:
            result[file] = md5(fd.read()).hexdigest()
    return result


def check(gh: ZipFile):
    hash_file = get_current_md5()
    files = list(hash_file)
    folder = gh.filelist[0].filename.split("/")[0]
    for file in files:
        if hash_file[file] != md5(gh.read(f"{folder}/{file}")).hexdigest():
            return True
    return False


def build_goneonize_decision() -> bool:
    """
    Determines whether the Goneonize build process should be triggered.

    This function compares the latest release of Neonize's `Neonize.proto` and `.sha` file
    with the local versions. If there is a difference, it indicates that Goneonize needs
    to be rebuilt.

    Returns:
        bool: True if Goneonize should be rebuilt, False otherwise.
    """
    try:
        github = Github()
        zipfile = ZipFile(
            BytesIO(
                github.download_neonize(
                    github.get_last_goneonize_version())))
        return check(zipfile)
    except Exception:
        return True


if __name__ == "__main__":
    sys.exit(not build_goneonize_decision())
