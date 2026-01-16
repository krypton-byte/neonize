import asyncio
# import subprocess
import os
from .version import Version

async def check_goneonize_change():
    result = await asyncio.create_subprocess_exec(
            "git",
            "diff",
            "--quiet",
            os.environ["BVHOOK_CURRENT_TAG"],
            "--",
            "goneonize/",
            ":(exclude)goneonize/version.go",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    await result.wait()
    print("returncode:", result.returncode)
    return result.returncode != 0

async def main():
    changed = await check_goneonize_change()
    version = Version()
    version.neonize = os.environ["BVHOOK_NEW_VERSION_TAG"]
    if changed:
        print("goneonize/ changed, bumping goneonize version...")
        version.goneonize = os.environ["BVHOOK_NEW_VERSION_TAG"]
    else:
        print("goneonize/ not changed, skipping goneonize version bump.")
    print("version:", version)
    return 0
if __name__ == "__main__":
    asyncio.run(main())
# r = subprocess.run(["uv", "run", "-m","tools.action"], capture_output=True)
# with open(".stdout.txt", "wb") as f:
#     f.write(r.stdout)
# with open(".stderr.txt", "wb") as f:
#     f.write(r.stderr)
# print("status:", r.returncode)
# print("stdout:", r.stdout.decode())
# print("stderr:", r.stderr.decode())
# import os
# print("BVHOOK_NEW_VERSION_TAG:", os.environ.get("BVHOOK_NEW_VERSION_TAG"))
# print("BVHOOK_CURRENT_TAG:", os.environ.get("BVHOOK_CURRENT_TAG"))