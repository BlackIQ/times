# FastAPI
from fastapi import FastAPI

# Routers
from routers import (
    application,
    auth,
    user,
    follow,
    post,
    comment,
)

# FastAPI Application
app = FastAPI(
    title="Nova Backend",
    version="0.1.0",
    summary="Amirhossein Jornal Backend by Amirhossein",
    openapi_tags=[
        {"name": "Application", "description": "Application relation things"},
        {"name": "Authentication", "description": "Authentication Endpoints"},
        {"name": "User", "description": "Manage your account"},
        {"name": "Follow", "description": "Follow each other"},
        {"name": "Post", "description": "Publish what is in your mind"},
        {"name": "Comment", "description": "Write something for a person"},
    ],
    servers=[
        {"url": "https://jornal.amirhossein.info", "description": "Production"},
        {"url": "http://127.0.0.1:8000", "description": "Development"},
    ],
)


# Routers
app.include_router(application.router, prefix="")  # Application
app.include_router(auth.router, prefix="/api")  # Authentication
app.include_router(user.router, prefix="/api")  # User
app.include_router(follow.router, prefix="/api")  # Follow
app.include_router(post.router, prefix="/api")  # Post
app.include_router(comment.router, prefix="/api")  # Comment
