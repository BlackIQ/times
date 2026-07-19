# FastAPI
from fastapi import FastAPI

# Routers
from routers import (
    auth,
    user,
    post,
    comment,
    note,
    reply,
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
        {"name": "Comment", "description": "Write something for a person"},
        {"name": "Note", "description": "Make a fast idea"},
        {"name": "Reply", "description": "Leave something on an idea"},
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
app.include_router(comment.router, prefix="/api")  # Comment
app.include_router(note.router, prefix="/api")  # Note
app.include_router(reply.router, prefix="/api")  # Reply
