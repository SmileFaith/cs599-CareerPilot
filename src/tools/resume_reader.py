import logging
from pathlib import Path
from typing import Optional
import pdfplumber
import docx

logger = logging.getLogger(__name__)

class ResumeReaderTool:
    """Tool for reading text from PDF and DOCX resume files."""

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Read text from a PDF or DOCX file.
        
        Args:
            file_path: Path to the resume file.
            
        Returns:
            Extracted text from the file.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is unsupported.
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            if path.suffix.lower() == '.pdf':
                return ResumeReaderTool._read_pdf(path)
            elif path.suffix.lower() in ['.docx', '.doc']:
                return ResumeReaderTool._read_docx(path)
            else:
                logger.error(f"Unsupported file format: {path.suffix}")
                raise ValueError(f"Unsupported file format: {path.suffix}")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

    @staticmethod
    def _read_pdf(path: Path) -> str:
        text = []
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text.append(extracted)
            return "\n".join(text)
        except Exception as e:
            logger.error(f"Error in _read_pdf: {e}")
            raise

    @staticmethod
    def _read_docx(path: Path) -> str:
        try:
            doc = docx.Document(path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            logger.error(f"Error in _read_docx: {e}")
            raise
