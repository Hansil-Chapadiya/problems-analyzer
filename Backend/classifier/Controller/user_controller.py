from fastapi import HTTPException, Body
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from config import params
from Controller.db_init import get_database
from Controller.check_password import verify_password
from Controller.hash_password import hash_password
from Model.UserModel import UserCreate
from response_error import ErrorResponseModel
import jwt


class UserController:
    @classmethod
    async def get_collection(cls) -> AsyncIOMotorDatabase:  # type: ignore
        database = await get_database()
        return database

    @classmethod
    async def user_login(cls, data: dict = Body(...)) -> JSONResponse:
        try:
            email = data.get("email")
            password = data.get("password")
            collection = await cls.get_collection()
            users = collection["User"]

            email_found = await users.find_one({"email": email})
            if email_found:
                password_matched = verify_password(
                    password, email_found["password"]
                )
                if password_matched:
                    if email_found and isinstance(email_found, dict) and "_id" in email_found:
                        token = jwt.encode(
                            {
                                "_id": str(email_found["_id"]),  # Convert ObjectId to string
                                "exp": datetime.utcnow() + timedelta(minutes=2880),
                            },
                            params["API_KEY"],
                            algorithm="HS256",
                        )
                    return JSONResponse(content={"detail": {"status": True, "token": token}})
                else:
                    error_response = ErrorResponseModel(
                        status=False,
                        detail=f"Incorrect Password"
                    )
                    raise HTTPException(status_code=401, detail=dict(error_response))
            else:
                error_response = ErrorResponseModel(
                    status=False,
                    detail=f"Incorrect email"
                )
                raise HTTPException(status_code=404, detail=dict(error_response))
        except IndexError:
            error_response = ErrorResponseModel(
                status=False,
                detail=f"Index error"
            )
            raise HTTPException(status_code=404, detail=dict(error_response))

    @classmethod
    async def create_user(cls, user_data: UserCreate) -> JSONResponse:
        try:
            collection = await cls.get_collection()
            users = collection["User"]

            # Check if the email already exists
            existing_user = await users.find_one({"email": user_data.email})
            if existing_user:
                error_response = ErrorResponseModel(
                    status=False,
                    detail="Email already registered"
                )
                raise HTTPException(status_code=400, detail=dict(error_response))

            # Create a new user
            user_dict = user_data.dict()
            user_dict["password"] = hash_password(user_dict["password"])
            user_dict["created_at"] = datetime.utcnow().isoformat()
            user_dict["updated_at"] = user_dict["created_at"]

            new_user = await users.insert_one(user_dict)
            return JSONResponse(content={"status": True, "user_id": str(new_user.inserted_id)})

        except Exception as e:
            error_response = ErrorResponseModel(
                status=False,
                detail=f"{e}"
            )
            raise HTTPException(status_code=500, detail=dict(error_response))