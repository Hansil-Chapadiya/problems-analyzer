from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId # type: ignore
from .ObjectIDValidator import PyObjectId
class UserProgress(BaseModel):
    user_id: PyObjectId
    problem_id: PyObjectId
    status: str = Field(..., description="Solved, Attempted, Skipped")
    attempts: int = Field(default=0)
    last_attempted_at: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
