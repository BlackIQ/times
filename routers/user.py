# FastAPI
from fastapi import APIRouter, Depends

# Application
from dependencies.auth import get_current_user  # Get Current User
from schemas.user import ProfileSchema  # Schemas
from models import User  # Models

# Router
router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get("/me", response_model=ProfileSchema)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
