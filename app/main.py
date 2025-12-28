from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.parser import extract_fio_and_topics
from app.excel_writer import generate_excel
import io

app = FastAPI()

# Frontenddan so‘rov kelishi uchun CORS ni yoqamiz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://docx-to-excel.vercel.app"],  # xavfsizlik uchun keyin frontend domeni bilan almashtiring
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI server is running!"}


@app.post("/convert")
async def convert_docx(file: UploadFile = File(...)):
    contents = await file.read()

    # Ma'lumotlarni ajratamiz
    parsed_data = extract_fio_and_topics(contents)

    # Excel faylga yozamiz
    excel_bytes = generate_excel(parsed_data)

    return StreamingResponse(io.BytesIO(excel_bytes),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=fio_va_mavzular.xlsx"})
