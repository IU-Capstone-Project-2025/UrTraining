from fastapi import FastAPI
from app.routes.base import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="UrTraining Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FRONTEND DOMEN!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to UrTraining API! We are in process"}
