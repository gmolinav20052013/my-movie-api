from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

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

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies():
    db = Session()    
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'])
def get_movies(id: int = Path(ge=1,le=2000)):    
    # datamovies = list(filter(lambda x: x['id'] == id, movies))    
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result:
        return JSONResponse(status_code=200,content=jsonable_encoder(result))
    return JSONResponse(status_code=404,content=[])

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=25)):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.categoria == category).all()
    if result:
        return JSONResponse(status_code=200,content=jsonable_encoder(result))
    return JSONResponse(status_code=404,content=[])
    # return JSONResponse(content=list(filter(lambda x: x['categoria'] == category, movies)))

@movie_router.post('/movies_add',tags=['CRUD'],response_model=dict)
# def add_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: int = Body(), categoria: str = Body()):
def add_movies(movie: Movie) -> dict:
    # movies.append(
    #     {"id": id, "title": title, "overview": overview, "year": year, "rating": rating, "categoria": categoria}
    # )
    
    db = Session()
    new_movie = MovieModel(**movie.__dict__)
    db.add(new_movie)
    db.commit()
    
    
    # movies.append(movie.model_dump())
    return JSONResponse(content={"message" : "Película adicionada"})

@movie_router.put('/movies/{id}',tags=['CRUD'], status_code=200)
def actu_movies(id: int, movie: Movie):    
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return   JSONResponse(status_code=404,content={"message" : "Película no encontrada"})           
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.categoria = movie.categoria
    db.commit()
    return JSONResponse(status_code=200, content={"message" : "Película modificada"})  
    # for item in movies:
    #     if item["id"] == id:
    #         item["title"] = movie.title
    #         item["overview"] = movie.overview
    #         item["year"] = movie.year
    #         item["rating"] = movie.rating
    #         item["categoria"] = movie.categoria

       
    # return JSONResponse(content=list(filter(lambda x: x['id'] == id, movies)))


@movie_router.delete('/movies/{id}', tags=['CRUD'],status_code=200)
def delete_movies_by_id(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return   JSONResponse(status_code=404,content={"message" : "Película no encontrada"}) 
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content={"message" : "Película eliminada"})  

    # for item in movies:
    #     if item["id"] == id:
    #         movies.remove(item)
    #         return JSONResponse(status_code=200,content={"message" : "Película eliminada"})  
    # return   JSONResponse(status_code=404,content={"message" : "Película no encontrada"})    
    # return JSONResponse(content=movies)


# @movie_router.post('/movies_add',tags=['CRUD'])
# def add_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: int = Body(), categoria: str = Body()):
#     movies.append(
#         {"id": id, "title": title, "overview": overview, "year": year, "rating": rating, "categoria": categoria}
#     )
#     return title

