import importlib.metadata
import os
from .utils.platform import generated_name
import requests
from pathlib import Path
from tqdm import tqdm


class UnsupportedPlatform(Exception):
    pass


def __download(url: str, fname: str, chunk_size=1024):
    resp = requests.get(url, stream=True)
    if resp.status_code != 200:
        resp.close()
        raise UnsupportedPlatform(generated_name())
    total = int(resp.headers.get("content-length", 0))
    with open(fname, "wb") as file, tqdm(
        desc=Path(fname).name,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)
        bar.n = total
    bar.close()


def download():
    version = importlib.metadata.version("neonize")
    __download(
        f"https://github.com/krypton-byte/neonize/releases/download/{version}/{generated_name()}",
        f"{os.path.dirname(__file__)}/{generated_name()}",
    )


if __name__ == "__main__":
    download()
