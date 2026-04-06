from fastapi import FastAPI
from app.routes.automate import router as automate_router

app = FastAPI(title="Automation of Scripts", description="A collection of scripts will get sorted automatically.", version="1.0.0")

app.include_router(automate_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Automation of Scripts API!"}

