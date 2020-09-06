from fastapi import (
    FastAPI,
    Query,
    Path
)

import json

from typing import List

from enum import Enum
from pydantic import BaseModel, Field


class FilmsAddPayload(BaseModel):
    filmName: str = Field(..., max_length=50, example="James Bond")
    description: str = Field(None, max_length=300, example="Film About Spy")
    createdDate: str = Field(None, example="2000-12-12")
    actors: List[str] = Field([], example=["DeNiro, LuiVeton"])


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
def add_film_to_store(
        genre: FilmsGenre,
        films_payload: FilmsAddPayload
        ):

    with open("films.json", "r") as file:
        data = json.load(file)
        data[genre.name].append(films_payload)

        return data
