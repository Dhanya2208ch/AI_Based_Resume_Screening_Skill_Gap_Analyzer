import fitz  # PyMuPDF
from docx import Document
import os

class ResumeParser:
    """Extract text from PDF and DOCX resumes"""
    
    def extract_text(self, filepath):
        """Extract text based on file extension"""
        file_extension = os.path.splitext(filepath)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(filepath)
        elif file_extension == '.docx':
            return self._extract_from_docx(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, pdf_path):
        """Extract text from PDF using PyMuPDF"""
        text = ""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
        
        return text.strip()
    
    def _extract_from_docx(self, docx_path):
        """Extract text from DOCX using python-docx"""
        text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error extracting DOCX: {str(e)}")
        
        return text.strip()
