from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId


class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    username: str
    phone_number: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Business(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Task(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    title: str
    description: str
    role: str
    due_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
