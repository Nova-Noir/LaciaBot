from typing import List
from pydantic import BaseModel, Extra


class SoutubotResult(BaseModel, extra=Extra.ignore):
    thumbnail: str
    language: str
    urls: List[str]
    fullname: str
    accuracy: float
