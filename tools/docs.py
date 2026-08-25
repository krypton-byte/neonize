import os
import shlex
from pathlib import Path
from subprocess import call

workdir = Path(__file__).parent.parent


def build():
    env = os.environ
    env["SPHINX"] = "true"
    call(
        shlex.split("uv run sphinx-apidoc -o docs/source neonize neonize.proto neonize.utils"),
        env=env,
    )
    call(shlex.split("uv run make html"), cwd=workdir / "docs")
    with open(workdir / "docs/_build/html/.nojekyll", "wb") as file:
        file.write(b"")


if __name__ == "__main__":
    build()
