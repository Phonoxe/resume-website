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


class Skill(BaseModel):
    name: str


class TechnicalSkill(Skill):
    description: str


class LanguageSkill(Skill):
    level: str | None = "A1"  # That is an example and will be modified in the future


class SoftSkill(Skill):
    description: str | None = None


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
    id: int | None = None
    info: PersonnalInfo
    experiences: list[Experience] | None = None
    formations: list[Formation] | None = None
    skills: list[Skill] | None = None


user_database = []


@app.get("/")
def read_root():
    return "This is Maxime's and Léopold's amazing website wouhou"


@app.get("/user_database")
def see_database():
    return user_database


@app.post("/add_user")
def add_user(user: User):
    user_database.append(user)
    user.id = len(user_database) - 1
    return f"{user.info.name} added to users!"


@app.post("/modify_user_name")
def set_user_name(id: int, name: str):
    previous_name = user_database[id].info.name
    user_database[id].info.name = name
    return f"{previous_name} was changed to {name}"


@app.delete("/delete_user")
def delete_user(id: int):
    user = user_database.pop(id)
    return f"{user.info.name} Was removed"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
