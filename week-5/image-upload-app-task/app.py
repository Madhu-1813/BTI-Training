from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil

# Create FastAPI application
app = FastAPI(title="Image Upload API")

# Directory where images will be stored
UPLOAD_DIR = "/data/images"

# Create directory if it does not exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health_check():
    return {
        "message": "Image Upload API is running"
    }


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload PNG image and save it in Docker volume.
    """

    # Allow only PNG files
    if file.content_type != "image/png":
        raise HTTPException(
            status_code=400,
            detail="Only PNG files are allowed."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse(
        status_code=200,
        content={
            "message": "File uploaded successfully",
            "filename": file.filename,
            "location": file_path
        }
    )


@app.get("/images")
def list_images():
    """
    List all uploaded images.
    """

    files = os.listdir(UPLOAD_DIR)

    return {
        "count": len(files),
        "images": files
    }