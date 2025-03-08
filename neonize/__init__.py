from .client import NewClient
from .utils.ffmpeg import FFmpeg
from .utils.iofile import TemporaryFile
from .events import Event
__version__ = '3.0.0'
__all__ = ('NewClient', 'FFmpeg', 'TemporaryFile', 'Event')