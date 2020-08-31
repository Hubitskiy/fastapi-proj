from fastapi import FastAPI, Query

from typing import List

from enum import Enum
from pydantic import BaseModel


class FilmsAddPayload(BaseModel):
    films: List[str]


class FilmsGenre(str, Enum):
    detective = "detective"
    criminal = "criminal"
    action = "action"


app = FastAPI()


list_of_films_by_genre = {
    "detective": [
        "Seven",
        "Sleven Lucky number",
        "Sherlock Holmes",
        "Prestige",
        "Death Note"
    ],
    "criminal": [
        "Pulp fiction",
        "God Father",
        "Once Upon Timer in America",
        "Joker",
        "Professional"
    ],
    "action": [
        "Lethal Weapon",
        "Die Hard",
        "Inglourious Basterds",
        "007",
        "Batman"
    ]
}


@app.get("/films/{genre}")
def get_list_films_by_genre(genre: FilmsGenre, skip: int = 0, limit: int = 25):
    return {
        "films": list_of_films_by_genre.get(genre.name)[skip: skip + limit]
    }


@app.post("/films/{genre}")
def add_film_to_store(genre: FilmsGenre, filmspayload: FilmsAddPayload):
    return list_of_films_by_genre[genre] + filmspayload.films
