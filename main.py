from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mis APIS FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)


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
