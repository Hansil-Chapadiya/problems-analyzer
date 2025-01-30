from fastapi import HTTPException, Header, Depends, Request
from functools import wraps
from config import params
from Controller.db_init import get_database
from response_error import ErrorResponseModel
from bson import ObjectId # type: ignore
import jwt

def get_authenticate_user(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        # Extract the `request` from kwargs to work with FastAPI's dependency injection
        request: Request = kwargs.get("request")
        if not request:
            error_response = ErrorResponseModel(status=False, detail="Request not found")
            raise HTTPException(status_code=400, detail=dict(error_response))

        token = request.headers.get('token')
        database = await get_database()

        if not token:
            error_response = ErrorResponseModel(status=False, detail="Missing token")
            raise HTTPException(status_code=401, detail=dict(error_response))
        try:
            decoded_token = jwt.decode(token, params['SECRET_KEY'], algorithms=['HS256'])
            _id = decoded_token.get('_id')
            user_details = await database['User'].find_one({"_id": ObjectId(_id)})

            if user_details and ObjectId(_id) == user_details['_id']:
                return await f(*args, **kwargs)  # Pass all arguments to the original function
            else:
                error_response = ErrorResponseModel(status=False, detail="User not found")
                raise HTTPException(status_code=401, detail=dict(error_response))
        except jwt.ExpiredSignatureError:
            error_response = ErrorResponseModel(status=False, detail="Token expired")
            raise HTTPException(status_code=401, detail=dict(error_response))
        except (jwt.InvalidTokenError, jwt.PyJWTError):
            error_response = ErrorResponseModel(status=False, detail="Invalid Token")
            raise HTTPException(status_code=401, detail=dict(error_response))
        except Exception as e:
            error_response = ErrorResponseModel(status=False, detail=str(e))
            raise HTTPException(status_code=500, detail=dict(error_response))
    return wrapper
