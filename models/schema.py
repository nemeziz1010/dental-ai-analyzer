
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
    class_name: str  # "cavity"
    confidence: float

class InferenceResponse(BaseModel):
    """
    Defines the final JSON response structure sent to the frontend.
    """
    report: str
    annotations: List[Annotation]
    
    image_b64: str