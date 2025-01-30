from fastapi import APIRouter, HTTPException, Body, Depends, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from response_error import ErrorResponseModel
from Controller.check_secret_key import authenticate_api_key
from Controller.problem_controller import ProblemController
from Controller.user_controller import UserController
from Controller.user_authenticate import get_authenticate_user
from Model.ProblemModel import ProblemBase
from Model.UserModel import UserCreate
from config import params
import jwt
import zipfile
import os
import re
from typing import List

UserRouter = APIRouter()

# Helper function to get API key from header
async def get_api_key(api_key: str = Depends(APIKeyHeader(name="API-Key"))):
    if api_key and not authenticate_api_key(api_key):
        error_response = ErrorResponseModel(
            status=False,
            detail="Invalid API-Key"
        )
        raise HTTPException(status_code=404, detail=dict(error_response))
    return api_key

# Problem Classification
@UserRouter.post("/user/classify")
async def classify_problems(data: dict = Body(...), api_key: str = Depends(get_api_key)):
    """
    Classifies problems for a user based on their skill level and provides detailed analysis.

    :param data: Input data containing user skill level.
    :param api_key: API key for authentication.
    :return: JSON response containing recommended problems and analysis.
    """
    try:
        # Extract user skill level
        user_skill = data.get("skill", "beginner").lower()

        # Define skill mapping to difficulty levels
        skill_difficulty_map = {
            "beginner": ["800", "1000"],
            "intermediate": ["800", "1000", "1200"],
            "master": ["1200", "1500"],
            "gm": ["1500", "2000"]
        }

        # Map user skill to difficulties
        difficulties = skill_difficulty_map.get(user_skill, ["800"])

        # Fetch problems from the ProblemController
        all_problems = await ProblemController.fetch_problems()

        # Filter problems based on the user's skill level
        recommended_problems = [
            {
                "problem_id": p["problem_id"],
                "title": p["title"],
                "difficulty": p["difficulty"],
                "tags": p["tags"],
                "details_url": p["details_url"]
            }
            for p in all_problems
            if str(p["difficulty"]) in difficulties
        ]

        # Analyze the recommended problems
        total_problems = len(recommended_problems)
        difficulty_distribution = {d: 0 for d in ["800", "1000", "1200", "1500", "2000"]}
        tag_distribution = {}
        total_difficulty = 0

        for p in recommended_problems:
            # Difficulty distribution
            difficulty_distribution[str(p["difficulty"])] += 1

            # Tag distribution
            for tag in p["tags"]:
                tag_distribution[tag] = tag_distribution.get(tag, 0) + 1

            # Total difficulty for calculating average
            total_difficulty += int(p["difficulty"])

        # Calculate additional metrics
        avg_difficulty = round(total_difficulty / total_problems, 2) if total_problems > 0 else 0
        difficulty_distribution_percentage = {
            d: round((count / total_problems) * 100, 2) for d, count in difficulty_distribution.items()
        }
        total_unique_tags = len(tag_distribution)
        most_common_tags = sorted(tag_distribution.items(), key=lambda x: x[1], reverse=True)[:5]

        # Response data
        response_data = {
            "status":True,
            "problems": recommended_problems,
            "analysis": {
                "total_problems": total_problems,
                "average_difficulty": avg_difficulty,
                "difficulty_distribution": difficulty_distribution,
                "difficulty_distribution_percentage": difficulty_distribution_percentage,
                "tag_distribution": tag_distribution,
                "total_unique_tags": total_unique_tags,
                "most_common_tags": most_common_tags,
            }
        }

        return JSONResponse(content=response_data)

    except HTTPException as e:
        error_response = ErrorResponseModel(status=False, detail=str(e.detail))
        raise HTTPException(status_code=e.status_code, detail=dict(error_response))
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=dict(error_response))

# Problem Recommendation
@UserRouter.get("/user/recommend")
@get_authenticate_user
async def recommend_problems(
    request: Request,
    difficulty: int = None,
    tags: List[str] = None,
    api_key: str = Depends(get_api_key)
):
    try:
        recommended_problems = await ProblemController.recommend_problems(difficulty, tags)
        return JSONResponse(content=recommended_problems)
    except HTTPException as e:
        error_response = ErrorResponseModel(status=False, detail=str(e.detail))
        raise HTTPException(status_code=e.status_code, detail=dict(error_response))
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=dict(error_response))

# Problem Details
@UserRouter.get("/user/problem-details/{contest_id}/{index}")
@get_authenticate_user
async def problem_details(request: Request, contest_id: int, index: str, api_key: str = Depends(get_api_key)):
    try:
        problem_detail = await ProblemController.get_problem_details(contest_id, index)
        return JSONResponse(content=problem_detail)
    except HTTPException as e:
        error_response = ErrorResponseModel(status=False, detail=str(e.detail))
        raise HTTPException(status_code=e.status_code, detail=dict(error_response))
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=dict(error_response))

@UserRouter.post("/user/login")
async def user_login(data: dict = Body(...), api_key: str = Depends(get_api_key)):
    try:
        user = await UserController.user_login(data)
        if user:
            return user
        else:
            error_response = ErrorResponseModel(status=False, detail="User not found")
            raise HTTPException(status_code=404, detail=dict(error_response))
    except HTTPException as e:
        error_response = ErrorResponseModel(status=False, detail=str(e.detail))
        raise HTTPException(status_code=e.status_code, detail=dict(error_response))
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=dict(error_response))

@UserRouter.post("/user/register")
async def register_user(
    request: Request,
    register_data: UserCreate = Body(...),
    api_key: str = Depends(get_api_key)
) -> JSONResponse:
    try:
        registration_creation = await UserController.create_user(register_data)
        return registration_creation
    except HTTPException as e:
        error_response = ErrorResponseModel(status=False, detail=str(e.detail))
        raise HTTPException(status_code=e.status_code, detail=dict(error_response))
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=dict(error_response))


@UserRouter.post("/user/classify/tags")
@get_authenticate_user
async def classify_problems(data: dict,request: Request, api_key: str = Depends(get_api_key)):
    """
    Classify problems based on user-provided skill and tags.

    :param data: Input data containing user skill level and optional tags.
    :param api_key: API key for authentication.
    :return: JSON response with classified problems.
    """
    try:
        user_skill = data.get("skill", "beginner").lower()
        user_tags = data.get("tags", [])
        # Fetch recommended problems using the ProblemController
        problems = await ProblemController.recommend_problems(user_skill, user_tags)

        if not problems:
            return JSONResponse(
                content={
                    "status": True,
                    "problems": [],
                    "message": "No problems found for the given skill and tags."
                }
            )

        return JSONResponse(content={"status": True, "problems": problems})

    except HTTPException as e:
        return JSONResponse(content={"status": False, "detail": str(e.detail)})
    except Exception as e:
        return JSONResponse(
            content={"status": False, "detail": f"Internal server error: {e}"}
        )


@UserRouter.get("/user/analysis/{id}")
@get_authenticate_user
async def analysis(id: str,request: Request, api_key: str = Depends(get_api_key)):
    """
    Classify problems based on user-provided skill and tags.

    :param data: Input data containing user skill level and optional tags.
    :param api_key: API key for authentication.
    :return: JSON response with classified problems.
    """
    try:
        # print(problems)
        # Fetch recommended problems using the ProblemController
        analysis_report = await ProblemController.analysis_problems(id)

        return JSONResponse(content={"status": True, "analysis": analysis_report})

    except HTTPException as e:
        return JSONResponse(content={"status": False, "detail": str(e.detail)})
    except Exception as e:
        return JSONResponse(
            content={"status": False, "detail": f"Internal server error: {e}"}
        )
