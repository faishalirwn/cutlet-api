from typing import List, Union
from datetime import datetime

from pydantic import BaseModel


class SongBase(BaseModel):
    uri: str
    lyrics: str


class SongCreate(SongBase):
    pass


class Song(SongBase):
    id: int
    transliterated_lyrics: str
    fetch_time: datetime

    class Config:
        orm_mode = True
