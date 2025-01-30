import requests
from typing import List, Dict
from fastapi import HTTPException
from fastapi import HTTPException
from .analysis_problems import LeetCodeProblemAnalyzerEnhanced
from fastapi.responses import StreamingResponse
import base64
from io import BytesIO
from Controller.db_init import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class ProblemController:

    @classmethod
    async def get_collection(cls) -> AsyncIOMotorDatabase:  # type: ignore
        database = await get_database()
        return database

    """
    Fetches problems from the LeetCode API using GraphQL.
    """

    BASE_URL = ""
    HEADERS = {"Content-Type": "application/json"}

    @staticmethod
    async def fetch_problems(limit: int = 300) -> List[Dict]:
        """
        Fetches problems from the LeetCode API.

        Args:
            limit: Number of problems to fetch. Defaults to 300.

        Returns:
            A list of dictionaries containing problem details.

        Raises:
            HTTPException: If there's an issue with the API request or data processing.
        """

        try:
            query = """
            query {
              problemsetQuestionListV2(
                categorySlug: ""
                limit: %d
                skip: 0
              ) {
                questions {
                  title
                  titleSlug
                  difficulty
                  topicTags {
                    name
                  }
                  acRate
                }
              }
            }
            """ % limit

            payload = {"query": query}
            response = requests.post(ProblemController.BASE_URL, json=payload, headers=ProblemController.HEADERS)
            response.raise_for_status()

            data = response.json()
            questions = data.get("data", {}).get("problemsetQuestionListV2", {}).get("questions", [])

            if not questions:
                return []

            formatted_problems = [
                {
                    "title": question["title"],
                    "title_slug": question["titleSlug"],
                    "difficulty": question["difficulty"].capitalize(),
                    "tags": [tag["name"] for tag in question["topicTags"]],
                    "acceptance_rate": round(question["acRate"], 2),
                    "details_url": f""
                }
                for question in questions
            ]

            return formatted_problems

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching data from LeetCode API: {e}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {e}"
            )

    @staticmethod
    async def recommend_problems(skill: str, tags: List[str] = None) -> List[Dict]:
        """
        Recommends problems based on user preferences like skill and tags.

        Args:
            skill: The skill level (beginner, intermediate, advanced).
            tags: A list of tags the user is interested in (e.g., ["Array", "Dynamic Programming"]).

        Returns:
            A list of recommended problems based on skill and acceptance rate.
        """

        try:
            # Increase initial fetch limit to improve chances of finding enough problems
            all_problems = await ProblemController.fetch_problems(limit=500)

            # Map skill to difficulty and acceptance rate thresholds
            skill_to_difficulty = {
                "beginner": {"difficulty": "Easy", "acceptance_rate_threshold": 0.7},
                "intermediate": {"difficulty": ["Easy", "Medium"], "acceptance_rate_threshold": 0.5},
                "advanced": {"difficulty": ["Hard", "Medium", "Easy"], "acceptance_rate_threshold": 0.4},
            }

            # Filter problems based on skill, difficulty, tags, and acceptance rate
            filtered_problems = [
                problem
                for problem in all_problems
                if (
                    problem["difficulty"] in skill_to_difficulty[skill]["difficulty"]
                    and (not tags or any(tag in problem["tags"] for tag in tags))
                    and problem["acceptance_rate"] <= skill_to_difficulty[skill]["acceptance_rate_threshold"]
                )
            ]

            # Ensure at least 10 problems are returned
            if len(filtered_problems) < 70:
                # If less than 10 problems found, increase fetch limit and try again
                all_problems = await ProblemController.fetch_problems(limit=1000)
                filtered_problems = [
                    problem
                    for problem in all_problems
                    if (
                        problem["difficulty"] in skill_to_difficulty[skill]["difficulty"]
                        and (not tags or any(tag in problem["tags"] for tag in tags))
                        and problem["acceptance_rate"] <= skill_to_difficulty[skill]["acceptance_rate_threshold"]
                    )
                ]
            try:
                status = await ProblemController.add_problems(filtered_problems[:70])
                return [
                    {"id":status.get('id'),"status":status.get('status'),"problems": filtered_problems[:70]}
                    ]# Return at most 10 problems
            except Exception as e:
                error_response = ErrorResponseModel(
                    status=False,
                    detail=f"{str(e)}"
                )
                raise HTTPException(
                status_code=500,
                detail=error_response
                )


        except Exception as e:
            error_response = ErrorResponseModel(
                status=False,
                detail=f"Internal Server Error: {e}"
            )
            raise HTTPException(
                status_code=500,
                detail=error_response
            )
    @classmethod
    async def add_problems(cls,problems: List[dict] = None) -> dict:
        try:
            collection = await cls.get_collection()
            problems_collections = collection["Problems"]

            document = {
                "problems": problems,
            }
            new_problems = await problems_collections.insert_one(document)
            return {
                "status":"True",
                "id":str(new_problems.inserted_id)
            }
        except Exception as e:
            return{
                "status":False,
                "detail":f"{str(e)}"
            }

    @classmethod
    async def get_problems_by_id(cls, id: str) -> dict:
        """
        Fetches a problems document by its ID.

        :param id: The ID of the document to fetch.
        :return: The document containing problems, or None if not found.
        """
        try:
            collection = await cls.get_collection()
            problems_collection = collection["Problems"]
            document = await problems_collection.find_one({"_id": ObjectId(id)})
            return document
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching problems by ID: {e}"
            )
    @staticmethod
    async def analysis_problems(id: str) -> dict:
        """
        Finds problems by ID from the database, performs analysis, and returns the results as a Base64-encoded ZIP file.

        :param id: The ID of the document containing the problems.
        :return: A dictionary with the analysis status and the Base64-encoded ZIP file.
        """
        try:
            # Fetch the problems document by ID
            document = await ProblemController.get_problems_by_id(id)
            if not document:
                return {
                    "status": False,
                    "detail": "No problems found for the given ID."
                }

            # Extract problems from the document
            problems = document.get("problems", [])
            if not problems or not isinstance(problems, list):
                return {
                    "status": False,
                    "detail": "No problems found in the document or invalid format."
                }

            # Perform analysis using LeetCodeProblemAnalyzerEnhanced
            analyzer = LeetCodeProblemAnalyzerEnhanced(problems)
            analysis_results = analyzer.analyze_all()

            # Generate a ZIP file of the analysis results
            zip_file = LeetCodeProblemAnalyzerEnhanced.generate_zip(analysis_results)
            zip_file_base64 = base64.b64encode(zip_file).decode("utf-8")

            return {
                "status": True,
                "file": zip_file_base64
            }

        except Exception as e:
            return {
                "status": False,
                "detail": f"Error during analysis: {str(e)}"
            }
