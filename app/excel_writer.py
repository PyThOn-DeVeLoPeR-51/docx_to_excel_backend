from openpyxl import Workbook
import io

def generate_excel(data: list[tuple[str, str]]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.append(["NAME", "TITLE"])

    for fio, topic in data:
        ws.append([fio, topic])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream.read()
