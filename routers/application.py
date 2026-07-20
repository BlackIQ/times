# FastAPI
from fastapi import APIRouter

# Application
from schemas.application import MessageSchema

# Router
router = APIRouter(
    prefix="",
    tags=["Application"],
)


@router.get("/", response_model=MessageSchema)
async def hi():
    return {"message": "Hey there! Welcome to Mahis final project"}


@router.get("/health", response_model=MessageSchema)
async def healthcheck():
    return {"message": "Everything is running alright"}


@router.get("/ping", response_model=MessageSchema)
async def ping():
    return "pong"
