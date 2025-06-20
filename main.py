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

# --- Middleware ---
# CORS middleware to allow cross-origin requests from our frontend
# crucial for development when frontend and backend run on different ports
origins = [
    "http://localhost",
    "http://localhost:3000", # Default for React
    "http://localhost:5173", # Default for Vite/React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)


# --- Routers ---
# Include the analysis router 
app.include_router(analysis_router)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Dental AI Analyzer API!"}