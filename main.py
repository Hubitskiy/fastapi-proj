from fastapi import (
    FastAPI,
    Query,
    Path,
    Request,
    status,
    exceptions,
    HTTPException,
    responses,
    encoders,
)

import json

from typing import List, Dict
from datetime import date

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


@app.exception_handler(exceptions.RequestValidationError)
def validation_exception(request: Request, exc: exceptions.RequestValidationError):
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=encoders.jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get(
    "/films/{genre}",
    status_code=status.HTTP_200_OK,
    response_model=List[FilmsAddPayload],
    tags=["films"],
    summary="Get List Films By Genre"
    )
def get_list_films_by_genre(
        genre: FilmsGenre = Path(..., description="Genre Of Films The List You Want To Get"),
        offset: int = Query(0),
        limit: int = Query(25)
        ):

    with open("films.json") as file:
        data = json.load(file)

        return data.get(genre.name)[offset: offset + limit]


@app.get(
    "/films/by-name/{film_name}",
    status_code=status.HTTP_200_OK,
    response_model=FilmsAddPayload,
    tags=["films"],
    summary="Get List Films By Name"
    )
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


@app.post(
    "/films/{genre}",
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, List[FilmsAddPayload]],
    tags=["films"],
    summary="Add Film By List Film",
    response_description="Return List Films In This Genre"
    )
def add_film_to_store(
        genre: FilmsGenre,
        films_payload: FilmsAddPayload,
        ):
    """
    - **filmName**: Name are creating film
    - **description**: Description are creating film
    - **createdDate**: Date when film was created
    - **actors**: List actors participating in film
    """

    with open("films.json", "r") as file:
        data = json.load(file)
        encoded_payload = encoders.jsonable_encoder(films_payload)
        data[genre.name].append(encoded_payload)

        return data


@app.put(
    "/films/{film_name}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, List[FilmsAddPayload]],
    tags=["films"],
    description="Use this endpoint for update films"
)
def update_film_by_name(
        film_name: str,
        films_payload: FilmsAddPayload,
        ):
    with open("films.json") as file:
        data = json.load(file)

        list_of_films = []
        for lists in data.values():
            list_of_films += lists

        for film in list_of_films:
            if film_name in film.values():
                film.update(films_payload)
                encoded_data = encoders.jsonable_encoder(data)
                return encoded_data

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {film_name} Not Found")
