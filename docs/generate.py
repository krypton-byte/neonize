import subprocess
from pathlib import Path
import shlex
project_path = Path(__file__).parent.parent
def build():
    subprocess.call(shlex.split("sphinx-apidoc -o docs/source neonize neonize.proto"),cwd=project_path)
    subprocess.call(shlex.split("make html"),cwd=project_path / "docs")