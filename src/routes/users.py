import pickle

import cloudinary
import cloudinary.uploader

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas.user import UserDb

router = APIRouter(prefix='/users', tags=["Users"])

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function returns the current user's information.
    ---
    get:
    tags: [users] # This is a tag that can be used to group operations by resources or any other qualifier.
    summary: Returns the current user's information.
    description: Returns the current user's information based on their JWT token in their request header.
    responses: # The possible responses this operation can return, along with descriptions and examples of each response type (if applicable).
    &quot;200&quot;:  # HTTP status code 200 indicates success! In this case, it means we successfully returned a User
    
    :param current_user: User: Get the user object from the database
    :return: The current user object
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.
    Args:
    file (UploadFile): The image to be uploaded.
    current_user (User): The user whose avatar is being updated.
    db (Session): A database session object for interacting with the database.
    
    :param file: UploadFile: Upload the file to cloudinary
    :param current_user: User: Get the user object from the database
    :param db: Session: Get the database session from the dependency injection
    :return: The user object, which is then serialized to json by fastapi
    :doc-author: Trelent
    """
    public_id = f"ContactsApp/{user.email}"
    r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    src_url = cloudinary.CloudinaryImage(public_id)\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user