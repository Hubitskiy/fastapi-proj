from fastapi import FastAPI, Query, Path

from typing import List
import json

from enum import Enum
from pydantic import BaseModel


class FilmsAddPayload(BaseModel):
    filmName: str
    description: str
    createdDate: str


class FilmsGenre(str, Enum):
    detective = "detective"
    criminal = "criminal"
    action = "action"


app = FastAPI()


@app.get("/films/{genre}")
def get_list_films_by_genre(
        genre: FilmsGenre = Path(..., description="Genre Of Films The List You Want To Get"),
        offset: int = Query(0),
        limit: int = Query(25)
        ):

    with open("films.json") as file:
        data = json.load(file)

        return {
            "films": data.get(genre.name)[offset: offset + limit]
        }


@app.post("/films/{genre}")
def add_film_to_store(genre: FilmsGenre, filmspayload: FilmsAddPayload):
    with open("films.json") as file:
        data = json.load(file)
        films_by_genre = data[genre.name]
        films_by_genre.append(filmspayload)

        return films_by_genre
