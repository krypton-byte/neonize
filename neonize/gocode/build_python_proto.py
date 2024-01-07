from pathlib import Path

for fp in (Path(__file__).parent.parent / "proto").iterdir():
    if fp.is_file() and not (
        fp.name.startswith("__init__") and "sys.path" in fp.read_text()
    ):
        text = fp.read_text()
        fp.write_text(
            "import sys\nfrom pathlib import Path\nsys.path.insert(0, Path(__file__).parent.__str__())\n"
            + text
        )
