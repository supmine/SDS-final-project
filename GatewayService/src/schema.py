from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
import bson


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

class RequestEntrySchema(BaseModel):
    dataset_id: str

class Entry(BaseModel):
    entry_type: str
    entry: str


class DatasetSchema(BaseModel):
    description: str
    prelabel: str
    # owner: str
    reward_dataset: float
    entries: List[Entry]


class AnnotateSchema(BaseModel):
    dataset_id: str
    entry_id: str
    # labeler_id: str
    label: str

class PrelabelImageSchema(BaseModel):
    url: str
