from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel
from ..business_logic_layer.user_service import UserService
from ..business_logic_layer import get_user_service

router = APIRouter(prefix="/auth", tags=["auth"])

_user_service = lambda: get_user_service()

class UserLoginModel(BaseModel):
    user_id: str
    password: str

class UserCreateModel(BaseModel):
    user_id: str
    name: str
    title: str
    secret: str
    password: str

class DefaultResponse(BaseModel):
    detail: str

@router.post("/login", description="Login to the system.", response_model=DefaultResponse)
async def login(request: Request, response: Response, user_login: UserLoginModel, user_service: UserService = Depends(_user_service)):

    if request.cookies.get("access_token"):
        raise HTTPException(status_code=401, detail="Already logged in")
    
    if (user_info := await user_service.user_login(user_login.user_id, user_login.password)) is None:
        raise HTTPException(status_code=401, detail="Login failed")
    
    if (token := user_service.generate_user_token(user_info)) is None:
        raise HTTPException(status_code=500, detail="Failed to generate token")
    
    response.set_cookie("access_token", token)

    return {"detail": "login success"}

@router.post("/logout", description="Logout from the system.", response_model=DefaultResponse)
async def logout(request: Request, response: Response):

    if not (request.cookies.get("access_token")):
        raise HTTPException(status_code=401, detail="Not logged in")

    response.delete_cookie("access_token")

    return {"detail": "logout success"}

@router.post("/register", description="Register to the system.", response_model=DefaultResponse)
async def register(user_create: UserCreateModel, user_service: UserService = Depends(_user_service)):

    if await user_service.get_user(user_create.user_id):
        raise HTTPException(status_code=409, detail="User already exists")
    
    if not await user_service.create_user(user_create.user_id, user_create.name, user_create.title, user_create.secret, user_create.password):
        raise HTTPException(status_code=500, detail="Register failed")
    
    return {"detail": "register success"}