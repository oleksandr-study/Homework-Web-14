from datetime import datetime, timedelta

from typing import List

from sqlalchemy import or_, and_, extract
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas.contact import ContactModel, ContactUpdateSchema


async def get_contacts_by_params(name: str, surname: str, email: str, skip: int, limit: int, db: Session, user: User) -> List[Contact]:
    """
    The get_contacts_by_params function returns a list of contacts that match the parameters passed in.
        If no parameters are passed, it will return all contacts for the user.
    
    :param name: str: Filter the contacts by name
    :param surname: str: Filter the contacts by surname
    :param email: str: Filter the contacts by email
    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of results returned
    :param db: Session: Access the database
    :param user: User: Get the user_id from the database
    :return: A list of contacts that match the parameters
    :doc-author: Trelent
    """
    if name or surname or email:
        return db.query(Contact).filter(and_(or_(Contact.name == name, Contact.surname == surname, Contact.email == email), Contact.user_id == user.id)).offset(skip).limit(limit).all()
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def create_contact(body: ContactModel, db: Session, user: User) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Create a new contact
    :param db: Session: Create a database session
    :param user: User: Get the user id from the token and then use it to create a contact
    :return: The contact object
    :doc-author: Trelent
    """
    contact = Contact(name=body.name, surname=body.surname, email=body.email, 
                   phonenumber=body.phonenumber, birthday=body.birthday, description=body.description, user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: Session, user: User) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactUpdateSchema): A schema containing all fields that can be updated for a Contact object.
            db (Session): An open connection to the database, provided by FastAPI's dependency injection system.
            user (User): The currently logged-in user, provided by FastAPI's dependency injection system via AuthMiddleware(). 
    
    :param contact_id: int: Get the contact from the database
    :param body: ContactUpdateSchema: Validate the data that is being passed in to the function
    :param db: Session: Access the database
    :param user: User: Check if the user is authorized to update a contact
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phonenumber = body.phonenumber
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.
            user (User): The user who is removing this contact from their list of contacts.
        Returns: 
            Contact | None: If successful, returns a Contact object representing the deleted record in JSON format; otherwise, returns None.
    
    :param contact_id: int: Identify which contact to delete
    :param db: Session: Pass the database session to the function
    :param user: User: Identify the user who is making the request
    :return: The contact object if it exists, otherwise it returns none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact(contact_id: int, db: Session, user: User) -> Contact:
    """
    The get_contact function returns a contact from the database.
        Args:
            contact_id (int): The id of the contact to be retrieved.
            db (Session): A connection to the database.
            user (User): The user who is requesting this information.
        Returns: 
            Contact: A single Contact object that matches both the id and user_id provided.
    
    :param contact_id: int: Specify the contact id of the contact we want to get
    :param db: Session: Pass in the database session
    :param user: User: Check if the user is authorized to get this contact
    :return: The contact object with the specified id
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_birthdays_in_7_days(db: Session, user: User) -> List[Contact]:
    """
    The get_birthdays_in_7_days function returns a list of contacts whose birthdays are within the next 7 days.
    
    
    :param db: Session: Pass the database session to the function
    :param user: User: Get the user_id from the user model
    :return: A list of contacts that have birthdays in the next 7 days
    :doc-author: Trelent
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=7)

    contact = (db.query(Contact).filter(
                and_(
                    or_(
                        and_(
                            extract("month", Contact.birthday) == today.month,
                            extract("day", Contact.birthday) >= today.day,
                            extract("day", Contact.birthday) <= end_date.day,
                        ),
                        and_(
                            extract("month", Contact.birthday) == end_date.month,
                            extract("day", Contact.birthday) >= today.day,
                            extract("day", Contact.birthday) <= end_date.day,
                        ),
                    ),
                Contact.user_id == user.id)
            ).all())
    return contact