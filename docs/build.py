from subprocess import call
from pathlib import Path
import shlex
workdir = Path(__file__).parent.parent
def build():
    call(shlex.split("poetry run sphinx-apidoc -o docs/source neonize neonize.proto neonize.utils"))
    call(shlex.split("poetry run make html"), cwd=workdir / "docs")
    with open(workdir / "docs/_build/html/.nojekyll", "wb") as file:
        file.write(b"")