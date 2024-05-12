from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator

import re


class ContactModel(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phonenumber: str
    birthday: date
    description: Optional[str] = Field(default=None, max_length=150)

    @validator("phonenumber")
    def phone_validation(cls, phone):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if phone and not re.search(regex, phone, re.I):
            raise ValueError("Phone Number Invalid.")
        return phone


class ContactUpdateSchema(ContactModel):
    name: str
    surname: str
    email: EmailStr
    phonenumber: str
    birthday: date
    description: str


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True