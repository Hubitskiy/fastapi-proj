from fastapi import FastAPI


app = FastAPI()


list_of_films_by_genre = {
    "detective": [
        "Seven",
        "Sleven Lucky number",
        "Sherlock Holmes"
    ],
    "criminal": [
        "Pulp fiction",
        "God Father",
        "Once Upon Timer in America"
    ],
    "action": [
        "Lethal Weapon",
        "Die Hard",
        "Inglourious Basterds"
    ]
}


@app.get("/films/{genre}")
def get_list_films_by_genre(genre: str):
    return list_of_films_by_genre.get(genre,
        {
            "Error": "Films doesnt found"
        })
