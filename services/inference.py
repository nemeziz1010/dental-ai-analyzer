
from inference_sdk import InferenceHTTPClient
from typing import List
import openai
import random
from datetime import datetime

from core.config import settings
from models.schema import Annotation

ROBOFLOW_CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=settings.ROBOFLOW_API_KEY
)

openai_client = None
if settings.OPENAI_API_KEY:
    try:
        openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    except Exception as e:
        print(f"Could not initialize OpenAI client: {e}")
        openai_client = None


def get_roboflow_predictions(image_b64: str) -> List[Annotation]:
    """
    Sends a base64 encoded image to the Roboflow API and parses the predictions.
    (This function remains unchanged)
    """
    try:
        result = ROBOFLOW_CLIENT.infer(image_b64, model_id=settings.ROBOFLOW_MODEL_ID)
        predictions = result.get('predictions', []) if isinstance(result, dict) else result[0].get('predictions', [])
        
        parsed_annotations = []
        for pred in predictions:
            annotation = Annotation(
                x=pred['x'],
                y=pred['y'],
                width=pred['width'],
                height=pred['height'],
                class_name=pred['class'],
                confidence=pred['confidence']
            )
            parsed_annotations.append(annotation)
        return parsed_annotations
    except Exception as e:
        print(f"Error calling Roboflow API: {e}")
        raise RuntimeError("Failed to get predictions from Roboflow.")

def generate_llm_diagnostic_report(annotations: List[Annotation]) -> str:
    """
    Generates a formal diagnostic report using OpenAI GPT API with a simplified prompt.
    """
    if not openai_client:
        print("Warning: OPENAI_API_KEY not set. Falling back to mock report.")
        return generate_mock_diagnostic_report(annotations)

    if not annotations:
        return "No significant pathologies were detected by the object detection model. The visible tooth structures appear to be within normal limits. Recommend routine clinical follow-up."

    
    findings_data = []
    for ann in annotations:
        location = "right side" if ann.x / 1024 > 0.5 else "left side"
        findings_data.append(
            f"- A '{ann.class_name}' was detected with {ann.confidence:.0%} confidence on the {location} of the image."
        )
    findings_summary = "\n".join(findings_data)
    
    system_prompt = (
        "You are a dental radiologist writing a professional diagnostic report using Markdown. "
        "Your tone must be clinical and objective. The report should contain '**Clinical Findings:**' and '**Clinical Recommendations:**' sections. "
        "Do not create a main title for the report."
    )

    user_prompt = f"""Based on the data below, please write a diagnostic report. For each finding, you must include the pathology name, its confidence level, and its location.

**Detected Pathologies Data:**
{findings_summary}
"""

    try:
        print("Sending descriptive prompt to OpenAI...")
        completion = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.45,
            max_tokens=400
        )

        report = completion.choices[0].message.content
        disclaimer = (
            "\n\n*Disclaimer: This diagnostic report has been generated using AI for educational purposes. "
            "All interpretations must be clinically reviewed and validated by a licensed dental professional.*"
        )
        return report + disclaimer

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        print("Falling back to mock report due to API error.")
        return generate_mock_diagnostic_report(annotations)


def generate_mock_diagnostic_report(annotations: List[Annotation]) -> str:
    """
    A fallback mock report generator.
    (This function is kept as a fallback)
    """
    if not annotations:
        return "No significant pathologies were detected in the provided X-ray image. The visible tooth structures appear to be within normal limits. Recommend routine clinical follow-up."

    pathology_counts = {}
    for ann in annotations:
        pathology_counts[ann.class_name] = pathology_counts.get(ann.class_name, 0) + 1
    
    report_lines = ["**Clinical Diagnostic Report (Mock)**", "\n", "Findings:"]
    
    for pathology, count in pathology_counts.items():
        plural = "s" if count > 1 else ""
        report_lines.append(f"- Detected {count} instance{plural} of suspected **{pathology}**.")

    report_lines.append("\n" + "Recommendations:")
    if "cavity" in pathology_counts:
        report_lines.append("- Potential carious lesions noted. Clinical examination and possibly restorative treatment are advised.")
    if "periapical lesion" in pathology_counts:
        report_lines.append("- Signs consistent with periapical inflammation are present. Endodontic evaluation is recommended to confirm and treat.")

    report_lines.append("\n" + "*Disclaimer: This is an AI-generated report. All findings should be clinically correlated by a qualified dental professional.*")
    
    return "\n".join(report_lines)
