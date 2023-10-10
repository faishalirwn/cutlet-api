from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

import cutlet
import pysbd

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/transliterate", response_model=schemas.Song)
async def transliterate_lyrics(song: schemas.SongBase, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_uri(db, uri=song.uri)
    if db_song:
        return db_song
        # raise HTTPException(status_code=400, detail="Song already registered")

    katsu = cutlet.Cutlet()
    katsu.use_foreign_spelling = False
    katsu.add_exception("♪", "♪")

    senter = pysbd.Segmenter(language="ja", clean=False)
    ZKS = "　"  # full width space

    def romajify(text):
        out = ""
        for line in text.split("\n"):
            if line == "":
                continue
            for chunk in line.split(ZKS):
                for sent in senter.segment(chunk):
                    out += katsu.romaji(sent) + " "
            out += "\n"

        return out

    tl_lyrics = song.lyrics.replace(", ", "、").replace(",", "、")
    tl_lyrics = romajify(tl_lyrics)

    # if song.uri == "spotify:track:2U6mFmBDjaAu6oCCDRpRet":
    #     tl_lyrics = tl_lyrics.replace("hirakanu", "akanu")
    # elif song.uri == "spotify:track:7fKFmrw1RSwU5a9vCwk155":
    #     tl_lyrics = tl_lyrics.replace("Korourai", "Kororon")
    #     tl_lyrics = tl_lyrics.replace("oto", "ne")
    #     tl_lyrics = tl_lyrics.replace("1 kai", "ikkai")
    #     tl_lyrics = tl_lyrics.replace("Suutaryoku", "Kazu amata")
    #     tl_lyrics = tl_lyrics.replace("kne", "koto")
    #     tl_lyrics = tl_lyrics.replace("Kneba", "Kotoba")
    #     tl_lyrics = tl_lyrics.replace("shounenjou", "shounenba")
    #
    return crud.create_song(db=db, song=song, tl_lyrics=tl_lyrics)
