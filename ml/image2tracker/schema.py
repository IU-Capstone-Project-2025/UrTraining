from typing import Optional

from pydantic import BaseModel


class Image2TrackerRequest(BaseModel):
    query: Optional[str] = None
    image: str


class Image2TrackerResponse(BaseModel):
    response: str
