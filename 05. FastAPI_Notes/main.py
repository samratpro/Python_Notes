import uvicorn
from fastapi import FastAPI
from app.routes import (
    home,
    users,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Custom Title",
    description="Custom description.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, port=4000)
