import os
from google.cloud import vision

# Set the path to your Google Cloud Vision service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/m4/Documents/keys/your_key_file.json"

# Initialize client
client = vision.ImageAnnotatorClient()

# Load image file
image_path = "/Users/m4/Documents/mypython_project/sample_text_image.png"
with open(image_path, "rb") as image_file:
    content = image_file.read()

# Build Vision image object
image = vision.Image(content=content)

# Call API
response = client.text_detection(image=image)

# Extract and print text
texts = response.text_annotations
if texts:
    print("Detected text:")
    print(texts[0].description)
else:
    print("No text detected.")

# Handle errors
if response.error.message:
    raise Exception(f"Vision API error: {response.error.message}")
