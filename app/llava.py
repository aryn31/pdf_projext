import base64
import requests
from io import BytesIO
from PIL import Image

def query_llava(image: Image.Image, prompt="Describe this image"):
    # Convert to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    b64_image = base64.b64encode(buffered.getvalue()).decode()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llava",
            "prompt": prompt,
            "images": [b64_image],
            "stream": False
        }
    )
    return response.json()["response"]
