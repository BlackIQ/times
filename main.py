# FastAPI
from fastapi import FastAPI

# Routers
from routers import (
    auth,
    user,
)

# FastAPI Application
app = FastAPI(
    title="Mahi Final Project",
    version="1.0.0",
    summary="The last project that Mahi creates FrontEnd for.",
    openapi_tags=[
        {"name": "Authentication", "description": "OAuth2 Endpoints"},
        {"name": "User", "description": "OAuth2 Endpoints"},
        {"name": "Post", "description": "Publish what is in your mind"},
        {"name": "Note", "description": "Make a fast idea"},
        {"name": "Comment", "description": "Write something for a person"},
    ],
)


@app.get("/")
async def hi():
    return {"message": "Hey there! Welcome to Mahis final project"}


# Routers
app.include_router(auth.router, prefix="/api")  # Authentication
app.include_router(user.router, prefix="/api")  # User
