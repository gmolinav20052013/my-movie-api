from fastapi import FastAPI,Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "Mis APIS FastAPI"
app.version = "0.9.0"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15)
    overview: str
    year: str
    rating: float
    categoria: str

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vios",
        "year": "2009",
        "rating": 7.8,
        "categoria": "Acción"        
    }    ,
     {
        "id": 2,
        "title": "Godfhater",
        "overview": "La vida de la familia Corleone",
        "year": "1972",
        "rating": 9.0,
        "categoria": "Drama/Suspenso"        
    }    
]



@app.get('/',tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movies(id: int):
    return list(filter(lambda x: x['id'] == id, movies))

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return list(filter(lambda x: x['categoria'] == category, movies))

@app.post('/movies_add',tags=['CRUD'])
# def add_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: int = Body(), categoria: str = Body()):
def add_movies(movie: Movie):
    # movies.append(
    #     {"id": id, "title": title, "overview": overview, "year": year, "rating": rating, "categoria": categoria}
    # )
    movies.append(movie)
    return movies

@app.put('/movies/{id}',tags=['CRUD'])
def actu_movies(id: int, movie: Movie):    
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["categoria"] = movie.categoria
    return list(filter(lambda x: x['id'] == id, movies))


@app.delete('/movies/{id}', tags=['CRUD'])
def delete_movies_by_id(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return movies


# @app.post('/movies_add',tags=['CRUD'])
# def add_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: int = Body(), categoria: str = Body()):
#     movies.append(
#         {"id": id, "title": title, "overview": overview, "year": year, "rating": rating, "categoria": categoria}
#     )
#     return title

