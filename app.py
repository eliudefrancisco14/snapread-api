# import fastAPI
from fastapi import FastAPI
from fastapi import UploadFile
from PIL import Image
import pytesseract
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS to allow any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# create a endpoint that receive a image and return a json with text of this image using OCR
@app.post("/api/snapread/ocr")
async def upload_image(file: UploadFile):
    """
    Receive an image file (png, jpg, or jpeg) and return the extracted text using OCR.
    """
    # Check if the uploaded file is of a valid type
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        return {"error": "Invalid file type. Only PNG, JPG, and JPEG are supported."}

    # Read the file content
    image_bytes = await file.read()
    # Convert bytes to a PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)

    return {"text": text}
