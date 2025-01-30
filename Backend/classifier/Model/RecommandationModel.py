from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId # type: ignore
from .ObjectIDValidator import PyObjectId
class Recommendation(BaseModel):
    user_id: PyObjectId
    problem_id: PyObjectId
    reason: str
    recommended_at: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
