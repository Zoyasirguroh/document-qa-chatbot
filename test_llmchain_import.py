import sys
sys.path.insert(0, r'C:\Users\FCI\Documents\document-qa-chatbot')

try:
    from src.llm_chain import LLMChain
    print("SUCCESS: LLMChain module imported!")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
