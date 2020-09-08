from fastapi import (
    FastAPI,
    Query,
    Path,
    status,
    HTTPException
)

import json
from datetime import date

from typing import List, Dict

from enum import Enum
from pydantic import BaseModel, Field


class FilmsAddPayload(BaseModel):
    filmName: str = Field(..., max_length=50)
    description: str = Field(None, max_length=300)
    createdDate: date = Field(None)
    actors: List[str] = Field([])

    class Config:
        schema_extra = {
            "example": {
                "filmName": "7 Times of Spring",
                "description": "Film About Soviet Spy In Nazi Germany",
                "createdDate": "1980-09-23",
                "actors": ["Tichonov", "Bronevoy"]
            }
        }


class FilmsGenre(str, Enum):
    detective = "detective"
    criminal = "criminal"
    action = "action"


app = FastAPI()


@app.get("/films/{genre}", status_code=status.HTTP_200_OK, response_model=List[FilmsAddPayload])
def get_list_films_by_genre(
        genre: FilmsGenre = Path(..., description="Genre Of Films The List You Want To Get"),
        offset: int = Query(0),
        limit: int = Query(25)
        ):

    with open("films.json") as file:
        data = json.load(file)

        return data.get(genre.name)[offset: offset + limit]


@app.get("/films/by-name/{film_name}", status_code=status.HTTP_200_OK, response_model=FilmsAddPayload)
def get_film_by_name(
        film_name: str = Path(...)
        ):

    with open("films.json") as file:
        data = json.load(file)

        list_of_films = []
        for lists in data.values():
            list_of_films += lists

        for film in list_of_films:
            if film_name in film.values():
                return film

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {film_name} Not Found")


@app.post("/films/{genre}", status_code=status.HTTP_201_CREATED, response_model=Dict[str, List[FilmsAddPayload]])
def add_film_to_store(
        genre: FilmsGenre,
        films_payload: FilmsAddPayload,
        ):

    with open("films.json", "r") as file:
        data = json.load(file)
        data[genre.name].append(films_payload)

        return data
