"""
LLM chain setup using LangChain RetrievalQA
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import logging

logger = logging.getLogger(__name__)

class LLMChain:
    """Setup and manage LLM chain"""

    def __init__(self, vector_store, model_name: str = "gpt-4o-mini", temperature: float = 0.1):

        self.vector_store = vector_store

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature
        )

        # Create prompt
        prompt_template = """
Use the following pieces of context to answer the question.
If you don't know the answer, say you don't know. Do not make up an answer.
Always cite the document/source.

Context:
{context}

Question:
{question}

Answer:
"""

        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # Create retriever
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})

        # Use RetrievalQA for LangChain with langchain_classic
        from langchain_classic.chains import RetrievalQA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def ask_question(self, question: str) -> dict:
        """Ask a question and get an answer with sources."""

        try:
            response = self.qa_chain({"query": question})

            logger.info(f"Question answered: {question[:50]}...")

            return {
                "answer": response["result"],
                "source_documents": response.get("source_documents", [])
            }

        except Exception as e:
            logger.error(f"Error in QA chain: {str(e)}")
            raise
