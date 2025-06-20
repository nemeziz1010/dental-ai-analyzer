# services/dicom_processor.py

import pydicom
import numpy as np
from PIL import Image
import base64
from io import BytesIO

def dicom_to_base64_png(file_bytes: bytes) -> str:
    """
    Reads DICOM file bytes, converts to a PNG image, and returns it as a Base64 encoded string.

    Args:
        file_bytes: The raw byte content of the .dcm file.

    Returns:
        A Base64 encoded string representation of the image.
    """
    try:
        # Read the DICOM file from in-memory bytes
        dicom_file = pydicom.dcmread(BytesIO(file_bytes))

        # Get the pixel data array
        pixel_array = dicom_file.pixel_array

        # Normalize the pixel array to 0-255 range for image conversion
        # This is a critical step for proper visualization
        if pixel_array.dtype != np.uint8:
            pixel_array = pixel_array.astype(float)
            pixel_array = (np.maximum(pixel_array, 0) / pixel_array.max()) * 255.0
            pixel_array = pixel_array.astype(np.uint8)

        # Create an image from the numpy array using Pillow
        image = Image.fromarray(pixel_array)
        
        # Save the image to an in-memory buffer
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        
        # Encode the buffer's content to Base64
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return img_str

    except Exception as e:
        # Handle potential errors, e.g., file is not a valid DICOM
        print(f"Error processing DICOM file: {e}")
        raise ValueError("Could not process the provided file as a DICOM image.")