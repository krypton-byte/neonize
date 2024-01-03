import subprocess
import shlex
from pathlib import Path
def build():
    subprocess.call(
        shlex.split("bash build.sh"),
        cwd=Path(__file__).parent
    )