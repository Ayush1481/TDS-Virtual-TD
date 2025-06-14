import base64
import pytesseract
from PIL import Image
import io

def extract_text_from_base64(base64_str):
    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data))
    return pytesseract.image_to_string(image)