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
    return MessageSchema(message="Hey there! Welcome to Nova Blog API")


@router.get("/health", response_model=MessageSchema)
async def healthcheck():
    return MessageSchema(message="Everything is running alright")


@router.get("/ping", response_model=MessageSchema)
async def ping():
    return MessageSchema(message="pong")
