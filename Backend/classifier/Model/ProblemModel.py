from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId # type: ignore
from .ObjectIDValidator import PyObjectId
class ProblemBase(BaseModel):
    title: str
    difficulty: str = Field(..., description="Difficulty level: Easy, Medium, Hard")
    tags: list[str] = Field(default=[])
    acceptance_rate: float = Field(..., ge=0, le=100)
    url: Optional[str]

class ProblemInDB(ProblemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
