import sys
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.parent.__str__())
from tools.version import Version
import os

if __name__ == "__main__":
    version = Version()
    version.neonize = os.environ["BVHOOK_NEW_VERSION_TAG"]
print(dict(os.environ))