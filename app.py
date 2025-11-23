import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Import our custom modules
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager
from src.llm_chain import LLMChain
from src.utils import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

# Page configuration
st.set_page_config(
    page_title="Document Q&A Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False

def main():
    initialize_session_state()
    
    # Title and description
    st.title("📚 Document Q&A Chatbot")
    st.markdown("Ask questions about your documents using AI-powered RAG")
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📄 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Choose PDF or TXT files",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload one or more documents to ask questions about"
        )
        
        if uploaded_files:
            if st.button("Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    try:
                        # Initialize components
                        doc_processor = DocumentProcessor()
                        vector_manager = VectorStoreManager()
                        
                        # Process documents
                        all_chunks = []
                        for uploaded_file in uploaded_files:
                            # Save temporarily
                            temp_path = f"temp_{uploaded_file.name}"
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Process document
                            chunks = doc_processor.process_document(temp_path)
                            all_chunks.extend(chunks)
                            
                            # Clean up
                            os.remove(temp_path)
                        
                        # Create vector store
                        st.session_state.vector_store = vector_manager.create_vector_store(all_chunks)
                        st.session_state.documents_loaded = True
                        
                        st.success(f"✅ Processed {len(uploaded_files)} documents with {len(all_chunks)} chunks!")
                        logger.info(f"Successfully processed {len(uploaded_files)} documents")
                        
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")
                        logger.error(f"Error processing documents: {str(e)}")
        
        # Display status
        st.divider()
        if st.session_state.documents_loaded:
            st.success("✅ Documents loaded and ready!")
        else:
            st.info("👆 Upload documents to get started")
        
        # Info section
        st.divider()
        st.markdown("""
        ### How to use:
        1. Upload PDF or TXT files
        2. Click "Process Documents"
        3. Ask questions in the chat
        4. Get AI-powered answers!
        
        ### Features:
        - 🔍 Semantic search
        - 🤖 GPT-4 powered
        - 📚 Multi-document support
        - ⚡ Fast responses
        """)
    
    # Main chat interface
    if not st.session_state.documents_loaded:
        st.info("👈 Please upload and process documents in the sidebar to begin")
        
        # Show example questions
        st.markdown("### Example Questions You Can Ask:")
        st.markdown("""
        - "What are the main topics covered in these documents?"
        - "Summarize the key findings"
        - "What does the document say about [specific topic]?"
        - "Can you explain [concept] from the documents?"
        """)
    else:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message:
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}:**")
                            st.text(source[:200] + "...")
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Initialize LLM chain
                        llm_chain = LLMChain(st.session_state.vector_store)
                        
                        # Get answer
                        response = llm_chain.ask_question(prompt)
                        
                        # Display answer
                        st.markdown(response["answer"])
                        
                        # Show sources
                        with st.expander("📚 View Sources"):
                            for i, doc in enumerate(response["source_documents"], 1):
                                st.markdown(f"**Source {i}:** {doc.metadata.get('source', 'Unknown')}")
                                st.text(doc.page_content[:200] + "...")
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["answer"],
                            "sources": [doc.page_content for doc in response["source_documents"]]
                        })
                        
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                        logger.error(f"Error in LLM chain: {str(e)}")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ Please set OPENAI_API_KEY in your .env file")
        st.stop()
    
    main()