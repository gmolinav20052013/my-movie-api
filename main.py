from fastapi import FastAPI,Body,Path, Query, Request, HTTPException,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()
app.title = "Mis APIS FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'gmolinav2005@gmail.com':
            raise HTTPException(status_code=403, detail= 'Credenciales son inválidas')

class User(BaseModel):
    email: str
    password: str

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

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "gmolinav2005@gmail.com" and user.password == 'admin':
        token = create_token(user.__dict__)
    return JSONResponse(status_code=200,content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies():
    return JSONResponse(status_code=200,content=movies)

@app.get('/movies/{id}', tags=['movies'])
def get_movies(id: int = Path(ge=1,le=2000)):    
    datamovies = list(filter(lambda x: x['id'] == id, movies))    
    if len(datamovies) > 0:
        return JSONResponse(status_code=200,content=datamovies)
    return JSONResponse(status_code=404,content=[])

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=25)):
    return JSONResponse(content=list(filter(lambda x: x['categoria'] == category, movies)))

@app.post('/movies_add',tags=['CRUD'],response_model=dict)
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

@app.put('/movies/{id}',tags=['CRUD'], status_code=200)
def actu_movies(id: int, movie: Movie):    
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["categoria"] = movie.categoria
            return JSONResponse(status_code=200, content={"message" : "Película modificada"})  
    return   JSONResponse(status_code=404,content={"message" : "Película no encontrada"})          
    # return JSONResponse(content=list(filter(lambda x: x['id'] == id, movies)))


@app.delete('/movies/{id}', tags=['CRUD'],status_code=200)
def delete_movies_by_id(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200,content={"message" : "Película eliminada"})  
    return   JSONResponse(status_code=404,content={"message" : "Película no encontrada"})    
    # return JSONResponse(content=movies)


# @app.post('/movies_add',tags=['CRUD'])
# def add_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: int = Body(), categoria: str = Body()):
#     movies.append(
#         {"id": id, "title": title, "overview": overview, "year": year, "rating": rating, "categoria": categoria}
#     )
#     return title

