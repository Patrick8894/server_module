from pydantic import BaseModel
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from ..business_logic_layer import get_user_service
from ..business_logic_layer.user_service import UserService
from typing import List

router = APIRouter(prefix="/user", tags=["user"])

_user_service = lambda: get_user_service()

class UserUpdateModel(BaseModel):
    name: str
    title: str
    secret: str
    password: str

class UserRetrieveModel(BaseModel):
    detail: str
    user_id: str
    name: str
    title: str
    secret: str

class UserDatadModel(BaseModel):
    user_id: str
    name: str
    title: str

class UserListModel(BaseModel):
    detail: str
    user_list: List[UserDatadModel]

class DefaultResponse(BaseModel):
    detail: str

@router.get("", description="Show all users.", response_model=UserListModel)
async def get_users(user_service: UserService = Depends(_user_service)):
    
    if (user_list := await user_service.get_users()) is None:
        raise HTTPException(status_code=500, detail="Failed to get users")

    return {"detail": "get success", "user_list": [{"user_id": item['_id'], "name": item['name'], "title": item['title']} for item in user_list]}

@router.get("/{user_id}", description="Show private user data.", response_model=UserRetrieveModel)
async def get_user(request: Request, user_id: str, user_service: UserService = Depends(_user_service)):

    if request.state.user_info["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not (user := await user_service.get_user(user_id)):
        raise HTTPException(status_code=404, detail="User not found or deleted")

    return {"detail": "get success", "user_id": user["_id"], "name": user["name"], "title": user["title"], "secret": user['secret']}

@router.put("/{user_id}", description="Update a user.", response_model=DefaultResponse)
async def update_user(request: Request, user_id: str, user_update: UserUpdateModel, user_service: UserService = Depends(_user_service)):

    if request.state.user_info["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not await user_service.get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found or deleted")

    if not await user_service.update_user(user_id, user_update.name, user_update.title, user_update.secret, user_update.password):
        raise HTTPException(status_code=500, detail="Failed to update user")

    return {"detail": "update success"}

@router.delete("/{user_id}", description="Delete a user.", response_model=DefaultResponse)
async def delete_user(request: Request, response: Response, user_id: str, user_service: UserService = Depends(_user_service)):
    
    if request.state.user_info["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not await user_service.get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found or deleted")

    if not await user_service.delete_user(user_id):
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
    response.delete_cookie("access_token")

    return {"detail": "delete success"}
    