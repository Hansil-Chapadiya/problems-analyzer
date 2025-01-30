# # main.py
from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode as OAuthFlowAuthorizationCodeModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
from user_router import UserRouter
# from participant_router import ParticipantRouter
# from .Controller.db_init import connect_to_mongo
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# async def lifespan(app: FastAPI):
#     await connect_to_mongo(app)

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="token",tokenUrl="token")

app.include_router(UserRouter)
# app.include_router(ParticipantRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
