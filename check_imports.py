#!/usr/bin/env python
"""Check available imports in langchain"""

# Try different import paths
attempts = [
    "from langchain.chains.retrieval_qa.base import RetrievalQA",
    "from langchain.chains import RetrievalQA",
    "from langchain_community.chains.retrieval_qa.base import RetrievalQA",
]

for attempt in attempts:
    try:
        exec(attempt)
        print(f"SUCCESS: {attempt}")
        break
    except ImportError as e:
        print(f"FAILED: {attempt}")
        print(f"  Error: {e}\n")
