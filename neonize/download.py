import os
from pathlib import Path

import requests
from tqdm import tqdm

from .utils.platform import generated_name

__GONEONIZE_VERSION__ = "0.12.0"
__GIT_RELEASE_URL__ = "https://github.com/krypton-byte/neonize"


class UnsupportedPlatform(Exception):
    pass


def __download(url: str, fname: str, chunk_size: int = 65536):
    resp = requests.get(url, stream=True, timeout=30)
    if resp.status_code != 200:
        resp.close()
        raise UnsupportedPlatform(generated_name())
    total = int(resp.headers.get("content-length", 0))
    tmp_name = f"{fname}.tmp"
    try:
        with (
            open(tmp_name, "wb") as file,
            tqdm(
                desc=Path(fname).name, total=total, unit="iB", unit_scale=True, unit_divisor=1024
            ) as bar,
        ):
            for data in resp.iter_content(chunk_size=chunk_size):
                if data:
                    size = file.write(data)
                    bar.update(size)
            bar.n = total
        os.replace(tmp_name, fname)
    except Exception:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
        raise


def download():
    __download(
        f"{__GIT_RELEASE_URL__}/releases/download/{__GONEONIZE_VERSION__}/{generated_name()}",
        f"{os.path.dirname(__file__)}/{generated_name()}",
    )


if __name__ == "__main__":
    download()
