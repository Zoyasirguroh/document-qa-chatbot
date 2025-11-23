"""
Vector store manager using ChromaDB
"""
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manage vector store operations"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize vector store manager
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create vector store from documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            Chroma vector store
        """
        try:
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            logger.info(f"Created vector store with {len(documents)} documents")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def load_vector_store(self) -> Chroma:
        """
        Load existing vector store
        
        Returns:
            Chroma vector store
        """
        try:
            vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            
            logger.info("Loaded existing vector store")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise