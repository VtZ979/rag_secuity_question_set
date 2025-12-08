from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import warnings
import logging

# Ignore warnings and set offline mode for HuggingFace
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

# Set offline mode to disable network checks (model should already be cached locally)
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

def build_retriever(docs, persist_directory: str = "./chroma_db", use_split: bool = False):


    import shutil
    shutil.rmtree(persist_directory, ignore_errors=True)



    # make sure the persistent directory exists
    os.makedirs(persist_directory, exist_ok=True)
  
    text_splitter = RecursiveCharacterTextSplitter()
    splits = text_splitter.split_documents(docs)

    # # Embed
    # Ensure offline mode is set before initializing embedding
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HUB_DISABLE_OFFLINE_WARNING'] = '1'
    
    try:
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    except Exception as e:
        print(f"[WARNING] Embedding initialization warning (may be network check): {e}")
        # Try again - model should be in cache
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embedding,
        persist_directory=persist_directory
    )

    retriever = vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": 3})

    return retriever, embedding