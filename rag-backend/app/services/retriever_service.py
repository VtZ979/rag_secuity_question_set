"""
Vector store and retriever service
"""
import sys
from pathlib import Path
import shutil
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.settings import VECTOR_DB_DIR, EMBEDDING_MODEL, RETRIEVAL_SEARCH_TYPE, RETRIEVAL_K


class RetrieverService:
    """
    Service for building and managing document retrievers.
    """
    
    def __init__(self, embedding_model=None, vector_db_dir=None):
        """
        Initialize the retriever service.
        
        Args:
            embedding_model: Name of the embedding model to use
            vector_db_dir: Directory for vector database persistence
        """
        self.embedding_model = embedding_model or EMBEDDING_MODEL
        self.vector_db_dir = vector_db_dir or VECTOR_DB_DIR
        self.embedding = None
        self.retriever = None
        self.vectorstore = None
    
    def build_retriever(self, docs, use_split=False, search_type=None, k=None):
        """
        Build a retriever from documents.
        
        Args:
            docs: List of LangChain Document objects
            use_split: Whether to split documents (currently not used)
            search_type: Search type ("similarity", "mmr", "similarity_score_threshold")
            k: Number of documents to retrieve
            
        Returns:
            Tuple of (retriever, embedding)
        """
        # Clean existing vector database
        if Path(self.vector_db_dir).exists():
            shutil.rmtree(self.vector_db_dir, ignore_errors=True)
        
        # Ensure directory exists
        Path(self.vector_db_dir).mkdir(parents=True, exist_ok=True)
        
        # Split documents if needed
        if use_split:
            text_splitter = RecursiveCharacterTextSplitter()
            docs = text_splitter.split_documents(docs)
        
        # Initialize embedding model
        self.embedding = HuggingFaceEmbeddings(model_name=self.embedding_model)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding,
            persist_directory=self.vector_db_dir
        )
        
        # Create retriever
        search_type = search_type or RETRIEVAL_SEARCH_TYPE
        k = k or RETRIEVAL_K
        
        search_kwargs = {"k": k}
        if search_type == "similarity_score_threshold":
            search_kwargs["score_threshold"] = 0.7
        
        self.retriever = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
        
        return self.retriever, self.embedding
    
    def get_relevant_documents(self, query: str):
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query string
            
        Returns:
            List of relevant documents
        """
        if self.retriever is None:
            raise ValueError("Retriever not initialized. Call build_retriever() first.")
        
        return self.retriever.get_relevant_documents(query)

