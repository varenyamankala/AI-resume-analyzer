"""
PDF Extractor Module

This module handles extraction of text from PDF resume files using PyPDF2.
It provides functionality to read and process PDF content for further analysis.
"""

import PyPDF2
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_bytes):
    """
    Extract text content from a PDF file bytes object.
    
    Args:
        pdf_bytes: Raw PDF file bytes
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        Exception: If PDF extraction fails
    """
    try:
        # Read the PDF file using PyPDF2
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        
        # Extract text from all pages
        extracted_text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                extracted_text += page.extract_text()
                extracted_text += "\n"  # Add newline between pages
            except Exception as e:
                logger.warning(f"Error extracting text from page {page_num}: {e}")
                continue
        
        if not extracted_text.strip():
            raise ValueError("No text could be extracted from the PDF")
        
        logger.info(f"Successfully extracted text from PDF. Length: {len(extracted_text)} characters")
        return extracted_text.strip()
    
    except Exception as e:
        logger.error(f"Error extracting PDF: {e}")
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def get_pdf_info(pdf_bytes, filename="resume.pdf"):
    """
    Get metadata about the PDF file (number of pages, etc).
    
    Args:
        pdf_bytes: Raw PDF file bytes
        filename: Name of the PDF file
        
    Returns:
        dict: Dictionary containing PDF metadata
    """
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        
        return {
            "num_pages": len(pdf_reader.pages),
            "file_name": filename,
            "file_size": len(pdf_bytes)
        }
    except Exception as e:
        logger.error(f"Error getting PDF info: {e}")
        return {}
