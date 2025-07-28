import ctypes
import logging
import queue
import threading

from ..proto.Neonize_pb2 import LogEntry

try:
    from colorlog import ColoredFormatter
except Exception:
    ColoredFormatter = None

log = logging.getLogger(__name__)
_log_ = log

if ColoredFormatter:
    formatter = ColoredFormatter(
        "%(asctime)s.%(msecs)03d %(log_color)s[%(name)s %(levelname)s] - %(message)s%(reset)s",
        datefmt="%H:%M:%S",
        log_colors={
            "INFO": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
else:
    stream_handler = logging.StreamHandler()

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d [%(name)s %(levelname)s] - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    handlers=[stream_handler],
)

clientlogger = logging.getLogger("whatsmeow.Client")
dblogger = logging.getLogger("Whatsmeow.Database")


_log_queue = queue.Queue()


def _worker():
    while True:
        binary, size = _log_queue.get()
        if binary is None:
            break  # sentinel for shutdown
        try:
            log_msg = LogEntry.FromString(ctypes.string_at(binary, size))
            if log_msg.Name == "Client":
                log = clientlogger
            elif log_msg.Name == "Database":
                log = dblogger
            else:
                name = log_msg.Name.replace("/", ".")
                log = logging.getLogger(f"whatsmeow.{name}")
            level_fn = getattr(log, log_msg.Level.lower(), log.info)
            level_fn(log_msg.Message)
        except Exception:
            _log_.exception("Failed to handle WhatsMeow log")
        finally:
            _log_queue.task_done()


_thread = threading.Thread(target=_worker, daemon=True)
_thread.start()


def log_whatsmeow(binary: int, size: int):
    _log_queue.put((binary, size))


def shutdown_log_worker():
    _log_queue.put((None, 0))
    _thread.join()
