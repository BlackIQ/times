# Libs
from fastapi import FastAPI  # FastAPI

# Application
from routers import application  # Routers: Application
from routers import auth  # Routers: Authentication
from routers import user  # Routers: User
from routers import follow  # Routers: Follow
from routers import post  # Routers: Post
from routers import comment  # Routers: Comment

# FastAPI Application
app = FastAPI(
    title="The Amir Times",
    version="0.1.0",
    summary="The Amir Times (Backend) by Amirhossein",
    openapi_tags=[
        {"name": "Application", "description": "Application relation things"},
        {"name": "Authentication", "description": "Authentication Endpoints"},
        {"name": "User", "description": "Manage your account"},
        {"name": "Follow", "description": "Follow each other"},
        {"name": "Post", "description": "Publish what is in your mind"},
        {"name": "Comment", "description": "Write something for a person"},
        {"name": "Like", "description": "Show how you love the post"},
    ],
    servers=[
        {"url": "https://times.amirhossein.info", "description": "Production"},
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
