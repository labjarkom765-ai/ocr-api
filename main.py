
import os
import tempfile

import easyocr
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="EasyOCR API",
    description="OCR API menggunakan EasyOCR",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

# Untuk development.
# Nanti setelah website Vercel sudah jadi,
# allow_origins bisa kita batasi hanya ke domain Vercel.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# EASYOCR
# ============================================================

print("Loading EasyOCR model...")

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

print("EasyOCR model loaded successfully.")


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "EasyOCR API is running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "success": True,
        "status": "healthy"
    }


# ============================================================
# OCR ENDPOINT
# ============================================================

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):

    # --------------------------------------------------------
    # Cek file
    # --------------------------------------------------------

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="File harus berupa JPG, PNG, atau WEBP."
        )

    # --------------------------------------------------------
    # Baca file
    # --------------------------------------------------------

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="File kosong."
        )

    # --------------------------------------------------------
    # Simpan sementara
    # --------------------------------------------------------

    original_filename = file.filename or "image.jpg"

    extension = os.path.splitext(
        original_filename
    )[1].lower()

    if not extension:
        extension = ".jpg"

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        # ----------------------------------------------------
        # Jalankan EasyOCR
        # ----------------------------------------------------

        results = reader.readtext(temp_path)

        # ----------------------------------------------------
        # Format hasil
        # ----------------------------------------------------

        texts = []
        detections = []

        for detection in results:

            box, text, confidence = detection

            texts.append(text)

            detections.append({
                "text": text,
                "confidence": float(confidence),
                "box": box
            })

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {
            "success": True,
            "filename": original_filename,
            "text": "\n".join(texts),
            "texts": texts,
            "detections": detections,
            "count": len(texts)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"OCR processing error: {str(e)}"
        )

    finally:

        # ----------------------------------------------------
        # Hapus file sementara
        # ----------------------------------------------------

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    import uvicorn

    port = int(
        os.environ.get(
            "PORT",
            8000
        )
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )

