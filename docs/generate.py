import os
import shlex
import subprocess
from pathlib import Path

project_path = Path(__file__).parent.parent

os.environ["SPHINX"] = "1"


def build():
    subprocess.call(
        shlex.split("sphinx-apidoc -o docs/source neonize neonize.proto neonize.utils"),
        cwd=project_path,
        env=os.environ,
    )
    subprocess.call(shlex.split("make html"), cwd=project_path / "docs")
