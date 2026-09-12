# Libs
from fastapi import APIRouter  # FastAPI

# Application
from schemas.common import MessageSchema  # Schemas: Common

# Router
router = APIRouter(
    prefix="",
    tags=["Application"],
)


@router.get("/", response_model=MessageSchema)
async def hi():
    return MessageSchema(message="Hey there! Welcome to The Amir Times API")


@router.get("/health", response_model=MessageSchema)
async def healthcheck():
    return MessageSchema(message="Everything is running alright")


@router.get("/ping", response_model=MessageSchema)
async def ping():
    return MessageSchema(message="pong")
