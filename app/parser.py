import io
from docx import Document
import re

def clean_topic(text: str) -> str:
    """Mavzu matnidan oxiridagi nuqtalar, raqamlar va bo‘sh joylarni olib tashlaydi"""
    cleaned = re.sub(r"[.\s]*\.*\d+\s*$", "", text)
    return cleaned.strip()

def is_likely_topic(text: str) -> bool:
    """Matn katta harflarda yozilganmi yoki ilmiy mavzuga o‘xshaydimi — harflar soniga qaraydi"""
    return (
        text.isupper()
        or len(text) > 20 and sum(c.isupper() for c in text) > 5
    )

def is_likely_author(text: str) -> bool:
    """Muallif FIOsini aniqlash: A.B.Ism, Ism Familiya, yoki ruscha/kirilcha variantlar"""
    # Har xil variantlarga moslashuvchan regex
    patterns = [
        r"^[A-ZА-ЯЎҚҒҲ]\.[A-ZА-ЯЎҚҒҲ]\.\s?[A-ZА-ЯЎҚҒҲa-zа-яўқғҳ’ʼʻ]+$",       # A.B. Ism
        r"^[A-ZА-ЯЎҚҒҲ][a-zа-яўқғҳʼ’ʻ]+\s[A-ZА-ЯЎҚҒҲ][a-zа-яўқғҳʼ’ʻ]+$",        # Ism Familiya
        r"^[A-ZА-ЯЎҚҒҲ][a-zа-яўқғҳʼ’ʻ]+$",                                     # Faqat bitta so‘z
    ]
    return any(re.match(p, text) for p in patterns)

def extract_text_from_tables(doc: Document) -> list[str]:
    """Hujjatdagi barcha jadvaldagi matnlarni olish"""
    texts = []
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell_text = cell.text.strip()
                if cell_text:
                    texts.append(cell_text)
    return texts

def extract_fio_and_topics(file_bytes) -> list[tuple[str, str]]:
    doc = Document(io.BytesIO(file_bytes))
    texts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    texts += extract_text_from_tables(doc)

    pairs = []
    current_authors = []

    for text in texts:
        # Muallifni ajratamiz
        if is_likely_author(text):
            current_authors.append(text)

        # Mavzuni ajratamiz
        elif is_likely_topic(text):
            topic = clean_topic(text)
            for author in current_authors:
                pairs.append((author, topic))
            current_authors = []

    return pairs
