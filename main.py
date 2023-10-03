import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import cutlet
import pysbd 

app = FastAPI()


class Lyrics(BaseModel):
    uri: str
    text: str
    

@app.post("/transliterate")
async def transliterate_lyrics(lyrics: Lyrics):
    # Code to transliterate the lyrics to romaji
    katsu = cutlet.Cutlet()
    katsu.use_foreign_spelling = False
    katsu.add_exception("♪", "♪")

    print(lyrics.uri)

    senter = pysbd.Segmenter(language="ja", clean=False)
    ZKS = "　" # full width space
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
    romaji_lyrics = romajify(f"""{lyrics.text.strip()}""")

    if lyrics.uri == "spotify:track:2U6mFmBDjaAu6oCCDRpRet":
        romaji_lyrics = romaji_lyrics.replace("hirakanu", "akanu")
    elif lyrics.uri == "spotify:track:7fKFmrw1RSwU5a9vCwk155":
        romaji_lyrics = romaji_lyrics.replace("Korourai", "Kororon")
        romaji_lyrics = romaji_lyrics.replace("oto", "ne")
        romaji_lyrics = romaji_lyrics.replace("1 kai", "ikkai")
        romaji_lyrics = romaji_lyrics.replace("Suutaryoku", "Kazu amata")
        romaji_lyrics = romaji_lyrics.replace("kne", "koto")
        romaji_lyrics = romaji_lyrics.replace("Kneba", "Kotoba")
        romaji_lyrics = romaji_lyrics.replace("shounenjou", "shounenba")

    return {"romaji": romaji_lyrics}

if __name__ == "__main__":
    try:
        port = os.environ.get("PORT", "5000")
        port = int(port)
    except ValueError:
        port = 5000
    uvicorn.run("main:app", host='0.0.0.0', port=port, log_level="info")