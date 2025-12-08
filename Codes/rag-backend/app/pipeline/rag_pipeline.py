from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Import hub - try different methods for compatibility
hub = None
try:
    # Try old way (langchain < 0.1.0)
    from langchain import hub
except ImportError:
    try:
        # Try new way (langchain >= 0.1.0, uses langchainhub)
        from langchainhub import Client
        hub_client = Client()
        # Create a simple wrapper to maintain compatibility
        class HubWrapper:
            def pull(self, prompt_id):
                return hub_client.pull(prompt_id)
        hub = HubWrapper()
    except ImportError:
        print("[WARNING] langchainhub not available, will use local prompt")
        hub = None

from .data_loader import load_stackoverflow_docs
from .retriever_builder import build_retriever
from .relevent_classify import classify_relevance
from .generator_builder import process_relevant_docs
from .classifier import SecurityQuestionClassifier

embedding = None
retriever = None
chain = None
llm = None
prompt = None
clf = None

def initialize_rag():
    global embedding, retriever, chain, llm ,prompt, clf
    print("begining load docs...")
    docs = load_stackoverflow_docs()
    print("docs loaded...")
    retriever, embedding = build_retriever(docs, use_split=False)
    print("retriever and embedding built...")
    llm = Ollama(model="llama3")
    print("llm initialized...")
    # # Prompt
    # Try to pull from hub, fallback to local prompt if network fails
    try:
        if hub is None:
            raise ImportError("hub not available")
        prompt = hub.pull("rlm/rag-prompt")
        print("prompt pulled from hub...")
    except Exception as e:
        print(f"[WARNING] Failed to pull prompt from hub: {e}")
        print("[INFO] Using local prompt template instead...")
        # Fallback to local prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\n\nContext: {context}"),
            ("human", "{question}")
        ])
        print("local prompt template created...")
    clf = SecurityQuestionClassifier(model_path="app/pipeline/svm_classifier.joblib")
    print("clf initialized...")
    print("loader finish...")
  
def get_rag_response(question: str):
    # get relevant docs
    relevant_docs = retriever.get_relevant_documents(question)
    print(relevant_docs)
    # process relevant docs and generate responses
    response = process_relevant_docs(relevant_docs, question, prompt, llm, embedding, clf)
    
    return response
    
