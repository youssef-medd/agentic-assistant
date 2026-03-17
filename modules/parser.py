from __future__ import annotations
from io import BytesIO
from typing import Iterable
from pypdf import PdfReader
def _extract_pdf_text_bytes(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    parts: list[str] = []
    for page in reader.pages:
        content = (page.extract_text() or "").strip()
        if content:
            parts.append(content)
    return "\n\n".join(parts).strip()
def _extract_pdf_with_fallback(pdf_file) -> tuple[str, str]:
    try:
        if hasattr(pdf_file, "getvalue"):  
            data = pdf_file.getvalue()
        else:
            try:
                pdf_file.seek(0)
            except Exception:
                pass
            data = pdf_file.read()
        if isinstance(data, str):
            data = data.encode("utf-8", errors="ignore")
    except Exception as e:
        return "", f"[Could not read file bytes: {e}]"
    try:
        text = _extract_pdf_text_bytes(data)
        if text:
            return text, "[Extracted text from PDF successfully]"
    except Exception as e:
        return "", f"[Error reading PDF structure: {e}]"
    return "", 
def process_files(uploaded_files: Iterable) -> str:
    combined_parts: list[str] = []
    for file in uploaded_files:
        file_type = getattr(file, "type", "") or ""
        name = getattr(file, "name", "uploaded_file")
        try:
            if file_type == "application/pdf":
                text, info = _extract_pdf_with_fallback(file)
                header = f"--- Content from {name} (PDF) ---"
                block = header + "\n" + (text or "[EMPTY]") + "\n" + info
                combined_parts.append(block)
            elif "text" in file_type:
                try:
                    file.seek(0)
                except Exception:
                    pass
                raw = file.read()
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", errors="replace")
                header = f"--- Content from {name} (TEXT) ---"
                combined_parts.append(header + "\n" + raw)
        except Exception as e:
            combined_parts.append(f"[Error parsing {name}: {e}]")
    return "\n\n".join(combined_parts).strip()