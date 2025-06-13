from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.courses import router as courses_router
from app.routes.users import router as users_router
from app.routes.admin import router as admin_router

app = FastAPI(title="UrTraining Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FRONTEND DOMEN!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
app.include_router(auth_router, prefix="/auth")
app.include_router(courses_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(admin_router, prefix="/admin")

@app.get("/")
def read_root():
    return FileResponse("static/login.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")

@app.get("/profile")
def profile():
    return FileResponse("static/profile.html")

@app.get("/security")
def security():
    return FileResponse("static/security.html")

@app.get("/admin")
def admin_panel():
    return FileResponse("static/admin.html")

@app.get("/register")
def register():
    return FileResponse("static/register.html")
