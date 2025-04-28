from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Returns the current status of the server",
)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok") 