from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "change_this_to_a_long_random_string"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    password: str | None = None
    info: PersonnalInfo
    experiences: list[Experience] | None = None
    formations: list[Formation] | None = None
    skills: list[Skill] | None = None


user_database = load_database()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = next((u for u in user_database if u.id == user_id), None)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


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
def read_profile(request: Request):
    return templates.TemplateResponse(request, "profile.html")


# A separate API route that returns the user data
@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


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
    if not user.password or user.password.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Password is required"})
    user.id = user.info.coordinate.email
    user.password = hash_password(user.password)  # hash before saving
    user_database.append(user)
    save_database()
    return f"{user.info.name} added to users!"


# Warning: The form_data.password is not hashed so we can access it. Idk if this is a security issue or not, but it is something to keep in mind
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((user for user in user_database if user.id == form_data.username), None)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}


# This route allows modification of a name given the id and the new name
@app.post("/modify_user_name")
def set_user_name(name: str, current_user: User = Depends(get_current_user)):
    previous_name = current_user.info.name
    current_user.info.name = name
    save_database()
    return f"{previous_name} was changed to {name}"


# This route deletes a user given its id
@app.delete("/delete_user")
def delete_user(id: int):
    user = user_database.pop(id)
    save_database()
    return f"{user.info.name} Was removed"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
