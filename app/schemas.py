from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from fastapi_users import schemas

# For Users
class UserRead(schemas.BaseUser[UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass   



# For Customers
class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class CustomerOut(BaseModel):
    id: UUID
    name: str
    phone: Optional[str]
    address: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

 

