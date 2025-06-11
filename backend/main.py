from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.courses import router as courses_router

app = FastAPI(title="UrTraining Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FRONTEND DOMEN!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(auth_router, prefix="/auth")
app.include_router(courses_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to UrTraining API! We are in process"}
