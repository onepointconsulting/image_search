from dataclasses import dataclass
from enum import IntEnum


class ErrorCode(IntEnum):
    NOT_FOUND = 1
    DESCRIPTION_MISSING = 2
    SAVE_FAILED = 3
    UNKNOWN = 1000


@dataclass
class Error:
    code: int
    message: str
