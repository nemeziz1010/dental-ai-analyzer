
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import Annotated

from models.schema import InferenceResponse
from services.dicom_processor import dicom_to_base64_png
from services.inference import get_roboflow_predictions, generate_llm_diagnostic_report


router = APIRouter(
    prefix="/analysis", 
    tags=["Analysis"]
)

@router.post(
    "/analyze", 
    response_model=InferenceResponse,
    summary="Analyze a Dental DICOM Image"
)
async def analyze_dicom_image(
    file: Annotated[UploadFile, File(description="A dental X-ray DICOM (.dcm) file.")]
):
    """
    Accepts a DICOM file, processes it, and returns AI-driven analysis.

    - **Converts** DICOM to PNG.
    - **Detects** pathologies using Roboflow.
    - **Generates** a diagnostic report using an LLM.
    """
    if not file.filename.endswith(('.dcm', '.rvg')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a .dcm or .rvg file."
        )

    try:
        file_bytes = await file.read()
        image_b64 = dicom_to_base64_png(file_bytes)
        annotations = get_roboflow_predictions(image_b64)

        
        report = generate_llm_diagnostic_report(annotations)
        
        return InferenceResponse(
            report=report,
            annotations=annotations,
            image_b64=image_b64
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal server error occurred.")

