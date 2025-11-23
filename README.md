# 📚 Document Q&A Chatbot with RAG

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.0.8-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)

Ask questions about your documents using Large Language Models and Retrieval Augmented Generation (RAG).

## 🎯 Overview

This chatbot allows you to upload PDF or TXT documents and ask natural language questions about their content. It uses:
- **RAG (Retrieval Augmented Generation)** to provide context-aware answers
- **Vector embeddings** for semantic search
- **GPT-4** for generating human-like responses
- **Streamlit** for a clean, interactive UI

## ✨ Features

- 📄 Upload multiple PDF/TXT documents
- 🔍 Semantic search using vector embeddings
- 🤖 Context-aware responses with GPT-4
- 💾 Persistent vector storage with ChromaDB
- 🎨 Clean, intuitive Streamlit interface
- ⚡ Fast query responses
- 🔒 Secure API key handling

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Zoyasirguroh/document-qa-chatbot.git
cd document-qa-chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 How to Use

1. **Upload Documents**
   - Click "Upload Documents" in the sidebar
   - Select one or more PDF or TXT files
   - Click "Process Documents" and wait for completion

2. **Ask Questions**
   - Type your question in the chat input
   - Get AI-generated answers based on your documents

3. **View Sources**
   - Each answer includes source document references

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| LLM | OpenAI GPT-4 | Generate answers |
| Orchestration | LangChain 1.0.8 | RAG orchestration |
| Embeddings | OpenAI text-embedding-ada-002 | Vector embeddings |
| Vector DB | ChromaDB | Vector storage & search |
| Frontend | Streamlit | User interface |
| Language | Python 3.11+ | Core development |

## 📂 Project Structure

```
document-qa-chatbot/
├── README.md                 # Documentation
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
├── .gitignore                # Git ignore rules
├── app.py                    # Main Streamlit app
└── src/
    ├── __init__.py
    ├── document_processor.py  # PDF/TXT processing
    ├── vector_store.py        # ChromaDB management
    ├── llm_chain.py           # LangChain RAG setup
    └── utils.py               # Helper functions
```

## 📊 How It Works

1. **Document Processing** - Load and split PDF/TXT files into chunks
2. **Embedding Generation** - Convert chunks to vector embeddings  
3. **Vector Storage** - Store embeddings in ChromaDB
4. **Query Processing** - Retrieve relevant chunks based on user query
5. **Answer Generation** - Generate answers using GPT-4 with context

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

## 🔮 Future Improvements

- [ ] Support for more file types (Word, Excel, PowerPoint)
- [ ] Multiple vector store options (Pinecone, Weaviate)
- [ ] Conversation memory (multi-turn chat)
- [ ] User authentication
- [ ] Cloud deployment

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - RAG orchestration framework
- [OpenAI](https://openai.com/) - GPT-4 and embeddings
- [Streamlit](https://streamlit.io/) - Web app framework
- [ChromaDB](https://www.trychroma.com/) - Vector database

## 👤 Author

**Zoya Sirguroh**
- [GitHub](https://github.com/Zoyasirguroh)

---

**Built with ❤️ by [Zoya Sirguroh](https://github.com/Zoyasirguroh)**
