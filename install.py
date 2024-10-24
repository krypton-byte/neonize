from io import BytesIO
from pathlib import Path
from tqdm import tqdm
from neonize.download import UnsupportedPlatform, generated_name, __download
import importlib.metadata
import os, requests
import zipfile




def go_build():
    temp = os.mkdir('tmp')
    version = importlib.metadata.version("neonize")
    content = requests.get(f"https://codeload.github.com/krypton-byte/neonize/zip/refs/tags/{version}").content
    zip_obj = zipfile.ZipFile(BytesIO(content))
    for file in zip_obj.namelist():
        if file.startswith(f'neonize-{version}/goneonize'):
            zip_obj.extractall('tmp')
    
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