# FastAPI
from fastapi import APIRouter

# Application
from schemas.common import MessageSchema  # Common Schemas

# Router
router = APIRouter(
    prefix="",
    tags=["Application"],
)


@router.get("/", response_model=MessageSchema)
async def hi():
    return {"message": "Hey there! Welcome to Nova Blog API"}


@router.get("/health", response_model=MessageSchema)
async def healthcheck():
    # TODO: Add some healthcheck stuff
    return {"message": "Everything is running alright"}


@router.get("/ping", response_model=MessageSchema)
async def ping():
    return "pong"
