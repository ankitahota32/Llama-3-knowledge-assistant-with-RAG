import fitz # from pymupdf, is used to work with pdf
from pathlib import Path #used for clean and modern file path handling instead of raw strings

def extract_text(filepath: str) -> str:
    path = Path(filepath) # convert string to path object for easier handling 
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    if path.suffix.lower() == ".pdf":
        return extract_from_pdf(filepath) # if the file is a pdf, use the pdf extraction function
    elif path.suffix.lower() == ".txt":
        return extract_from_txt(filepath) # if the file is a txt, use the txt extraction function
    else: 
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
def extract_from_pdf(filepath: str) -> str:
    doc = fitz.open(filepath) # open the pdf document using fitz, which is a library for working with pdfs
    text="" # initialize an empty string to hold the extracted text
    for page in doc:
        text += page.get_text() # extract text from each page and append it to the text variable
    doc.close() # close the document to free up resources
    return text.strip() # return the extracted text, stripping any leading or trailing whitespace

def extract_from_txt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f: # open the text file in read mode with utf-8 encoding to handle a wide range of characters
        return f.read().strip() # read the entire contents of the file and return it, stripping any leading or trailing whitespace