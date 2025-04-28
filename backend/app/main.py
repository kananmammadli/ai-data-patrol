from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .api.v1.endpoints import users, auth, health

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataPatrol API",
    description="API for DataPatrol - Data Quality Monitoring System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to DataPatrol API"} 