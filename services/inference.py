# services/inference.py

from inference_sdk import InferenceHTTPClient
from typing import List
import openai
import random
from datetime import datetime

from core.config import settings
from models.schema import Annotation

# --- Roboflow Client (Unchanged) ---
ROBOFLOW_CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=settings.ROBOFLOW_API_KEY
)

# --- OpenAI Client Initialization (Unchanged) ---
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
    Generates a formal diagnostic report using OpenAI GPT API.
    Includes patient name, doctor name, date, bullet-pointed Findings and Interpretation.
    """
    if not openai_client:
        print("Warning: OPENAI_API_KEY not set. Falling back to mock report.")
        return generate_mock_diagnostic_report(annotations)

    if not annotations:
        return "No significant pathologies were detected by the object detection model. The visible tooth structures appear to be within normal limits. Recommend routine clinical follow-up."

    # --- Generate names and date ---
    patient_names = ["John Smith", "Jane Doe", "Peter Jones", "Mary Williams", "David Brown"]
    doctor_names = ["Dr. Emily Carter", "Dr. Rajeev Menon", "Dr. Hannah Liu", "Dr. Miguel Sánchez", "Dr. Aditi Verma"]

    patient_name = random.choice(patient_names)
    doctor_name = random.choice(doctor_names)
    exam_date = datetime.now().strftime("%B %d, %Y")

    # --- Collect structured findings ---
    findings_lines = []
    interpretation_lines = []

    for i, ann in enumerate(annotations):
        location = "right side" if ann.x / 1024 > 0.5 else "left side"
        findings_lines.append(
            f"- A **{ann.class_name}** was detected with approximately **{ann.confidence:.0%}** confidence on the **{location}** of the radiograph."
        )

        if "cavity" in ann.class_name.lower():
            interpretation_lines.append(
                "- The **cavity** indicates a localized region of tooth decay, often due to poor oral hygiene causing erosion of the enamel and dentin."
            )
        elif "periapical" in ann.class_name.lower() or "pa" in ann.class_name.lower():
            interpretation_lines.append(
                "- The **periapical abscess (PA)** suggests an inflammatory or infectious lesion at the root tip, commonly resulting from untreated caries or trauma."
            )
        else:
            interpretation_lines.append(
                f"- The **{ann.class_name}** likely represents a dental pathology requiring further clinical correlation."
            )

    findings_block = "\n".join(findings_lines)
    interpretation_block = "\n".join(interpretation_lines)

    # --- Prompt Construction ---
    system_prompt = (
        "You are a senior dental radiologist. Write professional diagnostic reports in fluent English using Markdown formatting. "
        "Include a title, structured sections with headings like **Findings**, **Interpretation**, **Recommendations**, and **Conclusion**. "
        "Use bullet points only where appropriate. Avoid generic summaries; describe relevant clinical insights clearly."
    )

    user_prompt = f"""
### Diagnostic Report

**Patient Name:** {patient_name}  
**Exam Date:** {exam_date}  
**Radiologist:** {doctor_name}

---

**Findings:**  
{findings_block}

---

**Interpretation:**  
{interpretation_block}

---

Please continue by generating:

- **Recommendations**: Clear, actionable clinical advice for each finding.
- **Conclusion**: A 2-3 sentence summary of the overall diagnostic impression and next steps.

End the report with a disclaimer.
"""

    try:
        print("Sending enhanced structured prompt to OpenAI...")
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.45,
            max_tokens=650
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
        return "No significant pathologies were detected in the provided X-ray image. The visible tooth structures appear to be within normal limits. Recommend routine follow-up."

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
