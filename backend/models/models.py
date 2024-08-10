from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Business(BaseModel):
    name: str

class Worker(BaseModel):
    username: str
    phone_number: str
    password: str
    role: str

class Document(BaseModel):
    name: str
    access_control: dict

class UserLogin(BaseModel):
    phone_number: str
    password: str

class PhoneNumberVerification(BaseModel):
    phone_number: str
    code: str

class BusinessSelection(BaseModel):
    phone_number: str
    business_id: str

class Task(BaseModel):
    title: str
    description: str
    role: str
    due_date: datetime
    document: Optional[str] = None

class TaskReport(BaseModel):
    task_id: str
    report: str
    