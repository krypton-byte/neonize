import asyncio
import logging
import os
import signal
import sys
import traceback
from neonize.aioze.client import NewAClient
from neonize.utils import jid, log

sys.path.insert(0, os.getcwd())

client = NewAClient("db.sqlite3")
log.setLevel(logging.DEBUG)


async def on_exit():
    await client.stop()


async def greet():
    for signame in {"SIGINT", "SIGTERM", "SIGABRT"}:
        client.loop.add_signal_handler(
            getattr(signal, signame),
            lambda: asyncio.create_task(on_exit()),
        )
    await client.connect()
    while not client.connected:  # Do not rely on this to detect if client is still connected
        await asyncio.sleep(0.1)
    await client.send_message(
        jid.build_jid("123456789"),
        "Hey There!",
    )
    await client.stop()


try:
    if __name__ == "__main__":
        client.loop.run_until_complete(greet())
except Exception:
    traceback.print_exc()
