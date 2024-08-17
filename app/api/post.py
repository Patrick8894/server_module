from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, HTTPException
from ..business_logic_layer import get_post_service
from ..business_logic_layer.post_service import PostService
from typing import List
from datetime import datetime

router = APIRouter(prefix="/post", tags=["post"])

_post_service = lambda: get_post_service()

class PostCreateModel(BaseModel):
    title: str
    description: str

class PostUpdateModel(BaseModel):
    title: str
    description: str

class PostRetrieveModel(BaseModel):
    detail: str
    post_id: str
    title: str
    description: str
    user_id: str
    user_name: str
    created_timestamp: datetime
    edited_timestamp: datetime

class PostDatadModel(BaseModel):
    post_id: str
    title: str
    description: str
    user_id: str
    user_name: str
    created_timestamp: datetime
    edited_timestamp: datetime

class PostListModel(BaseModel):
    detail: str
    post_list: List[PostDatadModel]

class DefaultResponse(BaseModel):
    detail: str

@router.get("/all", description="Show all posts.", response_model=PostListModel)
async def get_posts(post_service: PostService = Depends(_post_service)):
    
    if (post_list := await post_service.get_posts()) is None:
        raise HTTPException(status_code=500, detail="Failed to get posts")

    return {"detail": "get success", "post_list": [{"post_id": item['post_id'], "title": item['title'], "description": item['description'], "user_id": item['user_id'], 
                                                    "user_name": item['user_name'], "created_timestamp": datetime.fromtimestamp(item['created_timestamp']), 
                                                    "edited_timestamp": datetime.fromtimestamp(item['edited_timestamp'])} for item in post_list]}

@router.get("/{post_id}", description="Show a posts.", response_model=PostRetrieveModel)
async def get_post(post_id: str, post_service: PostService = Depends(_post_service)):

    if not (post := await post_service.get_post(post_id)):
        raise HTTPException(status_code=404, detail="Post not found or deleted")

    return {"detail": "get success", "post_id": post['post_id'], "title": post['title'], "description": post['description'], "user_id": post['user_id'], "user_name": post['user_name'], 
            "created_timestamp": datetime.fromtimestamp(post['created_timestamp']), "edited_timestamp": datetime.fromtimestamp(post['edited_timestamp'])}

@router.post("", description="Create a posts.", response_model=DefaultResponse)
async def create_post(request: Request, post_create: PostCreateModel, post_service: PostService = Depends(_post_service)):

    if not await post_service.create_post(request.state.user_info["user_id"], post_create.title, post_create.description):
        raise HTTPException(status_code=500, detail="Failed to create post")

    return {"detail": "create success"}

@router.put("/{post_id}", description="Update a posts.", response_model=DefaultResponse)
async def update_post(request: Request, post_id: str, post_update: PostUpdateModel, post_service: PostService = Depends(_post_service)):

    if not (post := await post_service.get_post(post_id)):
        raise HTTPException(status_code=404, detail="Post not found or deleted")
    
    if request.state.user_info["user_id"] != post['user_id']:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not await post_service.update_post(post_id, post_update.title, post_update.description):
        raise HTTPException(status_code=500, detail="Failed to update post")

    return {"detail": "update success"}

@router.delete("/{post_id}", description="Delete a user.", response_model=DefaultResponse)
async def delete_post(request: Request, post_id: str, post_service: PostService = Depends(_post_service)):
    
    if not (post := await post_service.get_post(post_id)):
        raise HTTPException(status_code=404, detail="Post not found or deleted")

    if request.state.user_info["user_id"] != post['user_id']:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not await post_service.delete_post(post_id):
        raise HTTPException(status_code=500, detail="Failed to delete post")

    return {"detail": "delete success"}
    