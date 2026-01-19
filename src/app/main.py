from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .models import Person
from .randomuser_service import get_people
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Random User API Exam",
    version="1.0.0",
    description="REST API that returns a list of 10 people with data obtained from the Base API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/people", response_model=list[Person])
async def people():
    try:
        people_list = await get_people(results=10)
        return people_list
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={"message": "Error while consulting the external API.", "detail": str(e)},
        )