# Unused, but kept for reference and archival purposes

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

subapi = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@subapi.post("/", response_model=schemas.Song)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_uri(db, uri=song.uri)
    if db_song:
        raise HTTPException(status_code=400, detail="Song already registered")
    return crud.create_song(db=db, song=song)


# @subapi.get("/", response_model=List[schemas.Song])
# def read_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     songs = crud.get_songs(db, skip=skip, limit=limit)
#     return songs


# @subapi.get("/{song_id}", response_model=schemas.Song)
# def read_song(song_id: int, db: Session = Depends(get_db)):
#     db_song = crud.get_song(db, song_id=song_id)
#     if db_song is None:
#         raise HTTPException(status_code=404, detail="Song not found")
#     return db_song
