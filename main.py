from fastapi import FastAPI,Body,Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mis APIS FastAPI"
app.version = "0.9.0"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5,max_length=15)
    overview: str = Field(min_length=15,max_length=50)
    year: int = Field(default=2024, le=2024)
    rating: float = Field(default=0,ge=0.0,le=10)
    categoria: str = Field(min_length=5,max_length=25)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripción de la movie",
                "year": 2024,
                "rating": 0.0,
                "categoria": "Acción"
            }
        }

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
    return HTMLResponse('<h1>Hello world Movies</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies():
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'])
def get_movies(id: int = Path(ge=1,le=2000)):
    return JSONResponse(content=list(filter(lambda x: x['id'] == id, movies)))

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=25)):
    return JSONResponse(content=list(filter(lambda x: x['categoria'] == category, movies)))

@app.post('/movies_add',tags=['CRUD'],response_model=dict)
# def add_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: int = Body(), categoria: str = Body()):
def add_movies(movie: Movie) -> dict:
    # movies.append(
    #     {"id": id, "title": title, "overview": overview, "year": year, "rating": rating, "categoria": categoria}
    # )
    movies.append(movie.model_dump())
    return JSONResponse(content={"message" : "Película adicionada"})

@app.put('/movies/{id}',tags=['CRUD'])
def actu_movies(id: int, movie: Movie):    
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["categoria"] = movie.categoria
            return JSONResponse(content={"message" : "Película modificada"})  
    return   JSONResponse(content={"message" : "Película no encontrada"})          
    # return JSONResponse(content=list(filter(lambda x: x['id'] == id, movies)))


@app.delete('/movies/{id}', tags=['CRUD'])
def delete_movies_by_id(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message" : "Película eliminada"})  
    return   JSONResponse(content={"message" : "Película no encontrada"})    
    # return JSONResponse(content=movies)


# @app.post('/movies_add',tags=['CRUD'])
# def add_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: int = Body(), categoria: str = Body()):
#     movies.append(
#         {"id": id, "title": title, "overview": overview, "year": year, "rating": rating, "categoria": categoria}
#     )
#     return title

