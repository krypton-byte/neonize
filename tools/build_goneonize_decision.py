from io import BytesIO
import sys
from .github import Github
from zipfile import ZipFile
from hashlib import md5
from pathlib import Path

goneonize = Path(__file__).parent.parent / "goneonize"


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
        zipfile = ZipFile(BytesIO(github.get_last_neonize_release()))
        neonize_proto = ""
        defproto_sha = ""
        for file in zipfile.filelist:
            filename = file.filename
            if filename.endswith("Neonize.proto"):
                neonize_proto = md5(zipfile.read(file.filename)).hexdigest()
            elif file.filename.endswith(".sha"):
                defproto_sha = zipfile.read(filename).decode()
        with open(goneonize / "Neonize.proto", "rb") as file:
            current_neonize_proto = md5(file.read()).hexdigest()
        with open(goneonize / "defproto" / ".sha", "r") as file:
            current_defproto_sha = file.read()
        return not (neonize_proto == current_neonize_proto and defproto_sha == current_defproto_sha)
    except Exception:
        return True


if __name__ == "__main__":
    sys.exit(build_goneonize_decision())
