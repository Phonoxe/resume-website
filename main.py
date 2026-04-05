from fastapi import FastAPI
from app.database import Base, engine
from app.routers import pages, users

# Create all DB tables on startup (no-op if they already exist)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(pages.router)
app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
