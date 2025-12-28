import io
from docx import Document
import re

def clean_topic(text: str) -> str:
    # Oxiridagi nuqtalar, raqamlar, bo‘sh joylarni olib tashlash
    cleaned = re.sub(r"[.\s]*\.*\d+\s*$", "", text)
    return cleaned.strip()

def extract_fio_and_topics(file_bytes) -> list[tuple[str, str]]:
    doc = Document(io.BytesIO(file_bytes))
    pairs = []
    current_authors = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # FIO (oddiy ism yoki A.B.Ism uslubida)
        if re.match(r"^([A-Z][a-z]+\s[A-Z][a-z]+|[A-Z]\.[A-Z]\.[A-Z][a-z]+)$", text):
            current_authors.append(text)

        # MAVZU: katta harflarda
        elif text.isupper():
            topic = clean_topic(text)
            for author in current_authors:
                pairs.append((author, topic))
            current_authors = []

    return pairs
