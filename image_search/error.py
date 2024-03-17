from dataclasses import dataclass


@dataclass
class Error:
    code: int
    message: str
