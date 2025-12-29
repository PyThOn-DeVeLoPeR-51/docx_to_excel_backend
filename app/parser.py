import io
from docx import Document
import re

def clean_topic(text: str) -> str:
    cleaned = re.sub(r"[.\s]*\.*\d+\s*$", "", text)
    return cleaned.strip()

def is_likely_topic(text: str) -> bool:
    return (
        text.isupper()
        or (len(text) > 20 and sum(c.isupper() for c in text) > 5)
    )

def is_likely_author(text: str) -> bool:
    # Kengaytirilgan oddiy FIO aniqlovchi shartlar
    words = text.strip().split()
    return (
        1 <= len(words) <= 3 and
        all(w[0].isupper() for w in words if w)
    )

def extract_all_text(doc: Document) -> list[str]:
    texts = []

    for para in doc.paragraphs:
        if para.text.strip():
            texts.append(para.text.strip())

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if para.text.strip():
                        texts.append(para.text.strip())
    return texts

def extract_fio_and_topics(file_bytes) -> list[tuple[str, str]]:
    doc = Document(io.BytesIO(file_bytes))
    texts = extract_all_text(doc)

    pairs = []
    current_authors = []

    for text in texts:
        # Agar bu muallif bo‘lsa → saqlab qo‘yamiz
        if is_likely_author(text):
            current_authors.append(text)

        # Agar bu mavzu bo‘lsa → mualliflar bilan bog‘laymiz
        elif is_likely_topic(text) and current_authors:
            topic = clean_topic(text)
            for author in current_authors:
                pairs.append((author, topic))
            current_authors = []

        # Aks holda → boshqa matn, hech narsa qilinmaydi

    return pairs
