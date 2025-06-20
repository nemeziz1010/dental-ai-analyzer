# models/schema.py

from pydantic import BaseModel
from typing import List, Tuple

class Annotation(BaseModel):
    """
    Defines the structure for a single bounding box annotation.
    """
    x: float
    y: float
    width: float
    height: float
    class_name: str  # e.g., "cavity", "periapical lesion"
    confidence: float

class InferenceResponse(BaseModel):
    """
    Defines the final JSON response structure sent to the frontend.
    """
    report: str
    annotations: List[Annotation]
    # We will send the image back as a base64 encoded string for easy display
    image_b64: str