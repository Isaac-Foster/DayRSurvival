from dataclasses import dataclass
from base64 import b64encode

@dataclass
class User:
    login: str
    passwd: str

    def __post_init__(self):
        ...