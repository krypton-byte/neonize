import os
import shlex
import subprocess
from pathlib import Path
from platform import system


def build():
    if system() == "Windows":
        subprocess.call(
            shlex.split("build.bat"),
            cwd=Path(__file__).parent,
            env=os.environ.update({"build_neonize": "1"}),
        )
    else:
        subprocess.call(
            shlex.split("bash build.sh"),
            cwd=Path(__file__).parent,
            env=os.environ.update({"build_neonize": "1"}),
        )
