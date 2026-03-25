from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Interest(BaseModel):
    name: str
    description: str


class PersonnalInfo(BaseModel):
    name: str
    birth_date: str
    home: str
    coordinate: dict
    interest: list[Interest]


class LanguageSkill(BaseModel):
    language: str
    level: str


class Experience(BaseModel):
    type: str
    description: str
    starting_date: str
    ending_date: str


class Formation(BaseModel):
    ref: str
    description: __repr_str__


@app.get("/")
def read_root():
    return {"Hello": "World"}
