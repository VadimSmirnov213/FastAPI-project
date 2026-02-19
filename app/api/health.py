from fastapi import APIRouter
from app import schemas

router = APIRouter(tags=["health"])


@router.get("/health", response_model=schemas.HealthResponse)
def health_check():
    return schemas.HealthResponse(
        status="ok",
        message="API is running"
    )

