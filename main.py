# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import router as analysis_router
from core.config import settings

#  FastAPI app instance
app = FastAPI(
    title="Dental AI Analyzer API",
    description="An API to analyze dental X-rays using AI models.",
    version="1.0.0"
)

# Middleware

origins = [
    "http://localhost",
    "http://localhost:3000", 
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


# Routers
 
app.include_router(analysis_router)


@app.get("/", tags=["Root"])
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Dental AI Analyzer API!"}