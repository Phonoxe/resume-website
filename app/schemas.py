from pydantic import BaseModel


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
    level: str | None = "A1"


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
    id: str | None = None
    password: str | None = None
    info: PersonnalInfo
    experiences: list[Experience] | None = None
    formations: list[Formation] | None = None
    skills: list[Skill] | None = None
