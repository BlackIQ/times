# FastAPI
from fastapi import FastAPI

# Routers
from routers import (
    auth,
    post,
    user,
    note,
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
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Development"},
        {"url": "https://final.mahi.amirhossein.info", "description": "Production"},
    ],
)


@app.get("/")
async def hi():
    return {"message": "Hey there! Welcome to Mahis final project"}


# Routers
app.include_router(auth.router, prefix="/api")  # Authentication
app.include_router(user.router, prefix="/api")  # User
app.include_router(post.router, prefix="/api")  # Post
app.include_router(note.router, prefix="/api")  # Note
