from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Interest(BaseModel):
    name: str
    description: str


class Coordinates(BaseModel):
    tel: str
    email: str


class PersonnalInfo(BaseModel):
    name: str
    birth_date: str | None = None
    home: str | None = None
    coordinate: Coordinates | None = None
    interest: list[Interest] | None = None


class LanguageSkill(BaseModel):
    language: str
    level: str


class TechnicalSkill(BaseModel):
    name: str
    description: str


class SoftSkill(BaseModel):
    name: str


class Experience(BaseModel):
    type: str
    description: str
    starting_date: str
    ending_date: str


class Formation(BaseModel):
    ref: str
    description: str
    starting_date: str
    ending_date: str


class Photo(BaseModel):
    photo_id: str


class User(BaseModel):
    info: PersonnalInfo
    # We'll add the rest later


user_database = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/user_database")
def see_database():
    return user_database


@app.post("/add_user")
def add_user(person: PersonnalInfo):
    user_database.append(person)
    return f"{person.name} added to users!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
