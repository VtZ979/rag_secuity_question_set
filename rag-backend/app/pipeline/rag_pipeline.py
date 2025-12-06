"""
Main RAG Pipeline
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.services.data_loader import load_stackoverflow_docs
from app.services.retriever_service import RetrieverService
from app.services.llm_service import LLMService
from app.services.similarity_service import SimilarityService
from app.models.security_classifier import SecurityQuestionClassifier
from app.models.lda_classifier import initialize_lda_classifier
from app.models.sentiment_analyzer import VaderSentimentAnalyzer
from config.settings import (
    LDA_MODEL_PATH, LDA_DICT_PATH, LDA_MAPPING_PATH,
    CLASSIFIER_MODEL_PATH
)


class RAGPipeline:
    """
    Main RAG pipeline orchestrating all components.
    """
    
    def __init__(self):
        """Initialize the RAG pipeline."""
        self.retriever_service = None
        self.llm_service = None
        self.security_classifier = None
        self.lda_classifier = None
        self.sentiment_analyzer = None
        self.initialized = False
    
    def initialize(self):
        """
        Initialize all pipeline components.
        This should be called once at application startup.
        """
        print("Initializing RAG pipeline...")
        
        # Load documents
        print("Loading documents...")
        docs = load_stackoverflow_docs()
        print(f"Loaded {len(docs)} documents")
        
        # Build retriever
        print("Building retriever...")
        self.retriever_service = RetrieverService()
        self.retriever_service.build_retriever(docs)
        print("Retriever built")
        
        # Initialize LLM service
        print("Initializing LLM service...")
        self.llm_service = LLMService()
        print("LLM service initialized")
        
        # Initialize security classifier
        print("Loading security classifier...")
        self.security_classifier = SecurityQuestionClassifier(
            model_path=str(CLASSIFIER_MODEL_PATH)
        )
        print("Security classifier loaded")
        
        # Initialize LDA classifier
        print("Loading LDA classifier...")
        self.lda_classifier = initialize_lda_classifier(
            model_path=str(LDA_MODEL_PATH),
            dict_path=str(LDA_DICT_PATH),
            mapping_path=str(LDA_MAPPING_PATH)
        )
        print("LDA classifier loaded")
        
        # Initialize sentiment analyzer
        print("Initializing sentiment analyzer...")
        self.sentiment_analyzer = VaderSentimentAnalyzer()
        print("Sentiment analyzer initialized")
        
        self.initialized = True
        print("RAG pipeline initialization complete!")
    
    def get_response(self, question: str):
        """
        Get RAG response for a question.
        
        Args:
            question: User question string
            
        Returns:
            Dictionary with answer and related posts
        """
        if not self.initialized:
            raise RuntimeError("Pipeline not initialized. Call initialize() first.")
        
        # Retrieve relevant documents
        relevant_docs = self.retriever_service.get_relevant_documents(question)
        
        # Process documents and generate response
        response = self._process_documents(relevant_docs, question)
        
        return response
    
    def _process_documents(self, relevant_docs, question):
        """
        Process retrieved documents and generate response.
        
        Args:
            relevant_docs: List of retrieved documents
            question: User question
            
        Returns:
            Structured response dictionary
        """
        # Judge relevance
        judgement = self.llm_service.judge_relevance(question)
        
        # Classify question
        classifier_label = self.security_classifier.predict(question)
        lda_result = self.lda_classifier.classify(question)
        
        # Build category judgment
        if "relevant" in judgement.lower():
            category_j = (
                f"Your question is a {classifier_label} question. "
                f"The security topic of this question falls under the category: {lda_result['subcategory']}. "
                "This may be your knowledge blind spot, it is recommended that you learn more and "
                "pay attention to such security issues in the future."
            )
        else:
            category_j = (
                "The question does not appear to be related to cybersecurity, or lacks sufficient "
                "context to categorize. Please provide more technical details or context."
            )
        
        # Generate main answer
        main_answer = self.llm_service.generate_answer("", question)
        challenges = self.llm_service.generate_challenges(question)
        skills = self.llm_service.generate_skills(question)
        
        # Build response structure
        response = {
            "answer": {
                "user_question": question,
                "llm_answer": main_answer,
                "challenges": challenges,
                "skills": skills,
                "category": category_j
            },
            "related_post": []
        }
        
        # Process each relevant document
        for doc in relevant_docs:
            # Skip documents with empty or None page_content
            if not doc.page_content or not doc.page_content.strip():
                continue
            
            # Get similarity
            language = doc.metadata.get('skills', '')
            similarity = SimilarityService.classify_relevance(question, language)
            
            # Generate LLM solution for this document
            llm_solution = self.llm_service.generate_answer(
                doc.page_content, 
                question
            )
            
            # Calculate answer similarity
            accepted_answer = doc.metadata.get('accepted_answers', '')
            answer_similarity = SimilarityService.calculate_answer_similarity(
                accepted_answer, 
                llm_solution
            )
            
            # Analyze sentiment
            ori_q = doc.metadata.get('original_question', '')
            sentiment_result = self.sentiment_analyzer.invoke(ori_q)
            sentiment_label = sentiment_result.get("sentiment", "")
            
            # Build related post structure
            related_post = {
                "post_id": doc.metadata.get('postid', ''),
                "title": doc.metadata.get('title', ''),
                "ori_question": doc.metadata.get('original_question', ''),
                "accepted_answers": doc.metadata.get('accepted_answers', ''),
                "similarity": similarity,
                "llmSolution": llm_solution,
                "answer_similarity": answer_similarity,
                "challenges": doc.metadata.get('challenges', ''),
                "skills": doc.metadata.get('skills', ''),
                "sentimental": sentiment_label,
                "category": (
                    f"This question is a {doc.metadata.get('Label1', '')} question. "
                    f"The security topic of this question falls under the category: "
                    f"{doc.metadata.get('subcategory', '')}."
                )
            }
            
            response["related_post"].append(related_post)
        
        return response


# Global pipeline instance
pipeline = None


def initialize_rag():
    """Initialize the global RAG pipeline."""
    global pipeline
    pipeline = RAGPipeline()
    pipeline.initialize()


def get_rag_response(question: str):
    """
    Get RAG response for a question (convenience function).
    
    Args:
        question: User question string
        
    Returns:
        Response dictionary
    """
    if pipeline is None:
        raise RuntimeError("Pipeline not initialized. Call initialize_rag() first.")
    
    return pipeline.get_response(question)

