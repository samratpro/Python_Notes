import uvicorn
from fastapi import FastAPI
from project import urls
from project.database import engine, Base
import user_app.urls

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

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(urls.router)
app.include_router(user_app.urls.router)

if __name__ == "__main__":
    uvicorn.run(app, port=4000)
