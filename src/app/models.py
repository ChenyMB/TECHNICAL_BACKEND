from pydantic import BaseModel


class Person(BaseModel):
    full_name: str
    gender: str
    location: str
    email: str
    birth_date: str
    picture_url: str
