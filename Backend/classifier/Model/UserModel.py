from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId # type: ignore
from .ObjectIDValidator import PyObjectId

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    role: str = Field(..., description="User role (e.g., user or admin)")
    preferences: Optional[dict] = Field(default={})

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
