from fastapi import FastAPI
from pydantic import BaseModel

import cutlet
import pysbd
import urllib.request, json 

app = FastAPI()


class Song(BaseModel):
    uri: str
    lyrics: str
    provider: str


@app.post("/api/transliterate")
async def transliterate_lyrics(song: Song):
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
    tl_lyrics = song.lyrics.replace("watakushi", "watashi").replace("Watakushi", "Watashi")
    tl_lyrics = song.lyrics.replace("1 tsu", "hitotsu").replace("1tsu", "hitotsu").replace("2 tsu", "futatsu").replace("2tsu", "futatsu")
    tl_lyrics = song.lyrics.replace("1 byou", "ichibyou").replace("1byou", "ichibyou")

    with urllib.request.urlopen("https://raw.githubusercontent.com/faishalirwn/cutlet-api/main/corrections.json") as url:
        data = json.load(url)
        print("Logs:", song.uri, song.provider)
        if song.uri in data[song.provider]:
            print("Exist")
            for correction in data[song.provider][song.uri]:
                tl_lyrics = tl_lyrics.replace(correction[0], correction[1])

    return tl_lyrics
