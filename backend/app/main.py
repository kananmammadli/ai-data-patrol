from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from app.core.logging_config import get_logger
from app.api.v1 import checks, severity
from app.core.scheduler import start_scheduler

app = FastAPI(
    title="Data-Patrol",
    description="A data quality monitoring system",
    version="0.1.0"
)

logger = get_logger("data-patrol")

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total HTTP requests', ['method', 'endpoint'])

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to Data-Patrol API"}

@app.on_event("startup")
async def startup_event():
    start_scheduler()

app.include_router(checks.router)
app.include_router(severity.router)
