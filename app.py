import gradio as gr
import os
from google.cloud import vision
from PyPDF2 import PdfReader
from PIL import Image
import io

# Point to your credentials JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "smartocr.json"
client = vision.ImageAnnotatorClient()

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file.name)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text or "No text found in PDF."
    else:
        image = Image.open(file.name)
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')
        content = byte_array.getvalue()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        if response.error.message:
            return f"Error: {response.error.message}"
        return response.text_annotations[0].description if response.text_annotations else "No text found."

demo = gr.Interface(
    fn=extract_text,
    inputs=gr.File(label="Upload an Image or PDF", file_types=[".pdf", ".png", ".jpg", ".jpeg"]),
    outputs="text",
    title="Smart OCR Tool",
    description="Upload an image or PDF to extract text using Google Cloud Vision API."
)

if __name__ == "__main__":
    demo.launch()


