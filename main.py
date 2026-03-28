from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_FILE = Path("data/database.json")


def load_database():
    if DB_FILE.exists():
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            return [User(**user) for user in data]
    return []


def save_database():
    with open(DB_FILE, "w") as f:
        json.dump([user.model_dump() for user in user_database], f, indent=2)


class Interest(BaseModel):
    name: str
    description: str


class Coordinates(BaseModel):
    tel: str | None = None
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
    id: str | None = 0
    info: PersonnalInfo
    experiences: list[Experience] | None = None
    formations: list[Formation] | None = None
    skills: list[Skill] | None = None


user_database = load_database()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/sign_up", response_class=HTMLResponse)
def read_signup(request: Request):
    return templates.TemplateResponse(request, "signup.html")


@app.get("/login", response_class=HTMLResponse)
def read_login(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.get("/profile", response_class=HTMLResponse)
def read_profile(request: Request, id: str):
    user = next((u for u in user_database if u.id == id), None)
    if not user:
        return JSONResponse(status_code=404, content="User not found")
    return templates.TemplateResponse(request, "profile.html", {"user": user})


@app.get("/modify_name", response_class=HTMLResponse)
def read_modify_name(request: Request):
    return templates.TemplateResponse(request, "modify_name.html")


# This route returns the list of users
@app.get("/user_database")
def see_database():
    return user_database


# This route verifies if the given id correspond to a user, if yes, returns it
@app.get("/get_user")
def get_user(id: str):
    for user in user_database:
        if user.id == id:
            return user
    return JSONResponse(status_code=404, content="User not found")


# This route adds a new user to the users list
@app.post("/add_user")
def add_user(user: User):
    if user.id == 0:
        user.id = user.info.coordinate.email
    user_database.append(user)
    save_database()
    return f"{user.info.name} added to users!"


# This route allows modification of a name given the id and the new name
@app.post("/modify_user_name")
def set_user_name(id: str, name: str):
    for user in user_database:
        if user.id == id:
            previous_name = user.info.name
            user.info.name = name
            save_database()
            return f"{previous_name} was changed to {name}"
    return JSONResponse(status_code=404, content="User not found")


# This route deletes a user given its id
@app.delete("/delete_user")
def delete_user(id: int):
    user = user_database.pop(id)
    save_database()
    return f"{user.info.name} Was removed"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
