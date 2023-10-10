from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, index=True)
    uri = Column(String, unique=True, index=True)
    lyrics = Column(String)
    transliterated_lyrics = Column(String)
    fetch_time = Column(DateTime(timezone=True), server_default=func.now())
