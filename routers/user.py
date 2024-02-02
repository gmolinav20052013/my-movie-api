from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "gmolinav2005@gmail.com" and user.password == 'admin':
        token = create_token(user.__dict__)
    return JSONResponse(status_code=200,content=token)
