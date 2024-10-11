from enum import Enum


class LogType(str, Enum):
    info = "info"
    warnning = "warn"
    error = "error"

