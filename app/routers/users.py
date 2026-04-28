from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserORM
from app.schemas import User
from app.auth import verify_password, create_token, get_current_user
from app import crud

router = APIRouter()


@router.get("/me")
def get_me(current_user: UserORM = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "info": current_user.info,
        "experiences": current_user.experiences,
        "formations": current_user.formations,
        "skills": current_user.skills,
    }


@router.get("/user_database")
def see_database(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return [
        {
            "id": u.id,
            "info": u.info,
            "experiences": u.experiences,
            "formations": u.formations,
            "skills": u.skills,
        }
        for u in users
    ]


@router.post("/add_user")
def add_user(user: User, db: Session = Depends(get_db)):
    existing = crud.get_user_by_id(db, user.info.coordinate.email)
    if existing:
        return JSONResponse(
            status_code=400, content={"error": "This email is already registered"}
        )
    db_user = crud.create_user(db, user)
    return f"{db_user.info['name']} added to users!"


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_id(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/modify_user_name")
def set_user_name(
    name: str,
    current_user: UserORM = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    previous_name = crud.update_user_name(db, current_user, name)
    return f"{previous_name} was changed to {name}"


@router.delete("/delete_user")
def delete_user(id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    name = crud.delete_user(db, user)
    return f"{name} was removed"
