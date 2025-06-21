from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.courses import router as courses_router
from app.routes.users import router as users_router
from app.routes.admin import router as admin_router

# Database imports
from app.database import engine
from app.models.database_models import Base

app = FastAPI(
    title="UrTraining Backend API",
    description="A comprehensive training platform API for fitness courses and user management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # Initialize sample data
        from app.init_sample_data import init_sample_data
        init_sample_data()
        
    except Exception as e:
        print(f"Error creating database tables: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FRONTEND DOMEN!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router, tags=["Base"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(courses_router, prefix="/api", tags=["Courses"])
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

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
