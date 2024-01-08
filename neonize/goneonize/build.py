import os
import shlex
import subprocess


def build():
    command = shlex.split("build.bat" if os.name == "nt" else "bash build.sh")
    subprocess.call(
        command,
        cwd=os.path.dirname(__file__),
        env=os.environ.update({"build_neonize": "1"}),
        shell=os.name == "nt",
    )
