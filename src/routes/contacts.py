from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas.contact import ContactModel, ContactUpdateSchema, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=["Contacts"])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts_by_params(name: str = None, surname: str = None, email: str = None, skip: int = 0, limit: int = 10, 
                                  db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts_by_params function returns a list of contacts that match the parameters provided.
        If no parameters are provided, all contacts will be returned.
    
    :param name: str: Search for contacts by name
    :param surname: str: Filter the contacts by surname
    :param email: str: Search for a contact by email
    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contacts_by_params(name, surname, email, skip, limit, db, current_user)
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Pass the data from the request body to the function
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the auth_service
    :return: A contactmodel object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, db, current_user)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function returns a contact by its id.
        If the contact does not exist, it raises an HTTP 404 error.
    
    
    :param contact_id: int: Specify the contact id to retrieve
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdateSchema, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, body and db as parameters.
        It returns the updated contact.
    
    :param body: ContactUpdateSchema: Pass the request body to the function
    :param contact_id: int: Identify the contact to be updated
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user id of the logged in user
    :return: A contactupdateschema object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            current_user (User, optional): The user currently logged in and making this request. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/birthdays/", response_model=List[ContactResponse])
async def birthdays_in_7_days(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The birthdays_in_7_days function returns a list of contacts with birthdays in the next 7 days.
    
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user id from the token
    :return: A list of contacts, but i want to return a list of names
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_birthdays_in_7_days(db, current_user)
    return contact