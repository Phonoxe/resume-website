from sqlalchemy import Column, String, JSON
from app.database import Base


class UserORM(Base):
    """Maps to the 'users' table in the database. One instance = one row."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # user's email
    password = Column(String, nullable=True)  # bcrypt hash
    info = Column(JSON, nullable=False)  # PersonnalInfo dict
    experiences = Column(JSON, nullable=True)
    formations = Column(JSON, nullable=True)
    skills = Column(JSON, nullable=True)
