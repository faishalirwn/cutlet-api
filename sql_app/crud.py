from sqlalchemy.orm import Session

from . import models, schemas


# def get_song(db: Session, song_id: int):
#     return db.query(models.Song).filter(models.Song.id == song_id).first()


def get_song_by_uri(db: Session, uri: str):
    return db.query(models.Song).filter(models.Song.uri == uri).first()


# def get_songs(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Song).offset(skip).limit(limit).all()


def create_song(db: Session, song: schemas.SongCreate, tl_lyrics: str):
    db_song = models.Song(
        uri=song.uri,
        lyrics=song.lyrics,
        source=song.source,
        transliterated_lyrics=tl_lyrics,
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
