import pdfplumber
import docx
import aiofiles
from fastapi import UploadFile
import tempfile
import os

async def extract_text(file: UploadFile):
    """Extracts text from PDF, DOCX, or TXT files safely."""
    try:
        suffix = file.filename.split(".")[-1]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}")

        # Async read from UploadFile
        file_bytes = await file.read()
        temp_file.write(file_bytes)
        temp_file.close()

        # Decide how to extract
        if suffix.lower() == "pdf":
            text = extract_text_from_pdf(temp_file.name)
        elif suffix.lower() == "docx":
            text = extract_text_from_docx(temp_file.name)
        elif suffix.lower() == "txt":
            text = await extract_text_from_txt(temp_file.name)
        else:
            text = None

        # Clean up
        os.remove(temp_file.name)
        return text if text else "No extractable text found."

    except Exception as e:
        return f"Error extracting text: {str(e)}"


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF (sync)."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = [p.extract_text() for p in pdf.pages if p.extract_text()]
            text = "\n".join(pages)
            return text if text else "No text found in PDF."
    except Exception as e:
        return f"PDF error: {str(e)}"


def extract_text_from_docx(docx_path):
    """Extract text from a DOCX (sync)."""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text if text else "No text found in DOCX."
    except Exception as e:
        return f"DOCX error: {str(e)}"


async def extract_text_from_txt(txt_path):
    """Extract text from a TXT file asynchronously."""
    try:
        async with aiofiles.open(txt_path, 'r', encoding="utf-8") as f:
            text = await f.read()
            return text if text else "No text found in TXT."
    except Exception as e:
        return f"TXT error: {str(e)}"
