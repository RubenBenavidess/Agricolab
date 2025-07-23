# Basic Route

# Framework for exposing the API with Python
from fastapi import APIRouter

router = APIRouter(tags=["infra"])


@router.get("/health", summary="Readiness probe")
def health():
    return {"status": "ok"}
