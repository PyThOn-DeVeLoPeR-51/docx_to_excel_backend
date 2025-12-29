import io
from docx import Document
import re

def clean_topic(text: str) -> str:
    return re.sub(r"[.\s]*\.*\d+\s*$", "", text).strip()

def is_likely_topic(text: str) -> bool:
    return (
        text.isupper()
        or (len(text) > 20 and sum(c.isupper() for c in text) > 5)
    )

def is_likely_author(text: str) -> bool:
    words = text.strip().split()
    return (
        1 <= len(words) <= 3
        and any(w[0].isupper() for w in words if w)
        and not text.isupper()  # To‘liq katta harf bo‘lsa — bu mavzu
    )

def extract_all_text(doc: Document) -> list[str]:
    texts = []

    for para in doc.paragraphs:
        t = para.text.strip()
        if t:
            texts.append(t)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    t = para.text.strip()
                    if t:
                        texts.append(t)
    return texts

def extract_fio_and_topics(file_bytes) -> list[tuple[str, str]]:
    doc = Document(io.BytesIO(file_bytes))
    texts = extract_all_text(doc)

    pairs = []
    current_authors = []
    last_topic = ""

    for text in texts:
        if is_likely_topic(text):
            # Avvalgi mualliflar bilan bog‘lash
            topic = clean_topic(text)
            if current_authors:
                for author in current_authors:
                    pairs.append((author, topic))
                current_authors = []
            last_topic = topic

        elif is_likely_author(text):
            current_authors.append(text)
            if last_topic:
                pairs.append((text, last_topic))

        # boshqa matnlar e'tiborsiz qoldiriladi

    return pairs
