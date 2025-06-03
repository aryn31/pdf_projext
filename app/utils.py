import pdfplumber
from PIL import Image

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def extract_images_from_pdf(file):
    images = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            for img_dict in page.images:
                try:
                    im = page.to_image(resolution=150).original
                    cropped = im.crop((img_dict["x0"], img_dict["top"], img_dict["x1"], img_dict["bottom"]))
                    images.append(cropped)
                except Exception:
                    continue
    return images
