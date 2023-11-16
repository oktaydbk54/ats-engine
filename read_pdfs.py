import PyPDF2
import hashlib

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

    filename = f'resumes/resume_{text_hash}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

    return text # filename de döndürülebilir duruma göre.
