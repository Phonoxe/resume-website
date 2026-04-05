from sqlalchemy.orm import Session
from app.models import UserORM
from app.schemas import User
from app.auth import hash_password


def get_user_by_id(db: Session, user_id: str) -> UserORM | None:
    return db.query(UserORM).filter(UserORM.id == user_id).first()


def get_all_users(db: Session) -> list[UserORM]:
    return db.query(UserORM).all()


def create_user(db: Session, user: User) -> UserORM:
    db_user = UserORM(
        id=user.info.coordinate.email,
        password=hash_password(user.password),
        info=user.info.model_dump(),
        experiences=[e.model_dump() for e in user.experiences]
        if user.experiences
        else None,
        formations=[f.model_dump() for f in user.formations]
        if user.formations
        else None,
        skills=[s.model_dump() for s in user.skills] if user.skills else None,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # syncs the returned object with what's now in the DB
    return db_user


def update_user_name(db: Session, user: UserORM, new_name: str) -> str:
    previous_name = user.info["name"]
    # JSON columns require full reassignment to trigger SQLAlchemy change detection
    user.info = {**user.info, "name": new_name}
    db.commit()
    return previous_name


def delete_user(db: Session, user: UserORM) -> str:
    name = user.info["name"]
    db.delete(user)
    db.commit()
    return name
