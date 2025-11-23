"""
Document processor for handling PDF and TXT files
"""
import os
from typing import List
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process documents and split into chunks"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document processor
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def process_document(self, file_path: str) -> List[Document]:
        """
        Process a single document
        
        Args:
            file_path: Path to document file
            
        Returns:
            List of Document objects with text chunks
        """
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self._process_pdf(file_path)
        elif file_extension == '.txt':
            return self._process_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    def _process_pdf(self, file_path: str) -> List[Document]:
        """Process PDF file"""
        try:
            reader = PdfReader(file_path)
            
            documents = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                
                if text.strip():  # Only process non-empty pages
                    # Create document with metadata
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": os.path.basename(file_path),
                            "page": page_num + 1,
                            "total_pages": len(reader.pages)
                        }
                    )
                    documents.append(doc)
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            logger.info(f"Processed PDF: {file_path} - {len(chunks)} chunks created")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise
    
    def _process_txt(self, file_path: str) -> List[Document]:
        """Process TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Create document with metadata
            doc = Document(
                page_content=text,
                metadata={
                    "source": os.path.basename(file_path),
                    "type": "txt"
                }
            )
            
            # Split into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            logger.info(f"Processed TXT: {file_path} - {len(chunks)} chunks created")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing TXT {file_path}: {str(e)}")
            raise