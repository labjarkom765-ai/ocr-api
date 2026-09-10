# EasyOCR API

Backend OCR menggunakan FastAPI dan EasyOCR.

## Features

- FastAPI REST API
- EasyOCR
- CPU inference
- JPG support
- PNG support
- WEBP support
- CORS support
- JSON response
- Swagger API documentation

## Endpoints

### GET /

Menampilkan status API.

### GET /health

Health check untuk server.

### POST /ocr

Mengirim gambar untuk diproses menggunakan EasyOCR.

Field upload:

file
Response

Contoh:

{
    "success": true,
    "filename": "test.jpg",
    "text": "HELLO WORLD",
    "texts": [
        "HELLO WORLD"
    ],
    "detections": [
        {
            "text": "HELLO WORLD",
            "confidence": 0.98,
            "box": [
                [10, 20],
                [300, 20],
                [300, 60],
                [10, 60]
            ]
        }
    ],
    "count": 1
}
Run Local

Install dependency:

pip install -r requirements.txt

Jalankan:

uvicorn main:app --reload

API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs
Railway

Start command:

uvicorn main:app --host 0.0.0.0 --port $PORT

Setelah deployment Railway selesai, endpoint dapat dipanggil oleh frontend Vercel.

Architecture
Vercel
   |
   | POST /ocr
   v
Railway
   |
   +-- FastAPI
   |
   +-- EasyOCR
   |
   v
JSON OCR Result
   |
   v
Vercel
