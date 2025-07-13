import fitz  # PyMuPDF

def extract_text(file, file_type):
    if file_type == "pdf":
        return extract_text_from_pdf(file)
    elif file_type == "txt":
        return extract_text_from_txt(file)
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_txt(file):
    return file.read().decode("utf-8")
