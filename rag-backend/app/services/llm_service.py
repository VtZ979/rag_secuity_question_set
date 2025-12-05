"""
LLM service for answer generation
"""
import sys
from pathlib import Path
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.settings import LLM_MODEL, LLM_BASE_URL


class LLMService:
    """
    Service for interacting with LLM (Ollama).
    """
    
    def __init__(self, model=None, base_url=None):
        """
        Initialize the LLM service.
        
        Args:
            model: LLM model name
            base_url: Base URL for Ollama API
        """
        self.model = model or LLM_MODEL
        self.base_url = base_url or LLM_BASE_URL
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Ollama LLM instance."""
        self.llm = Ollama(model=self.model)
    
    def generate_answer(self, context: str, question: str) -> str:
        """
        Generate an answer using the LLM.
        
        Args:
            context: Context documents
            question: User question
            
        Returns:
            Generated answer text
        """
        template = """
        You are an expert in software development, specifically in the field of software security. 
        Based on the following context, provide an answer to the question.

        Your answer should follow this format:

        Summary : [Programming Language] → [Framework] → [API or Configuration]
        - Bullet point 1: key insight or step
        - Bullet point 2: key insight or step
        - Bullet point 3: ...

        Be concise and only include details that are directly relevant from the context. 
        The summary line should be under 20 words.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm
        return chain.invoke({"context": context, "question": question})
    
    def generate_challenges(self, question: str) -> str:
        """
        Generate challenges summary for a question.
        
        Args:
            question: User question
            
        Returns:
            Challenges summary
        """
        template = """
        Role: You are an expert Software Engineer. You will be provided with a question 
        regarding a challenge faced by another software developer posted in a developer 
        discussion forum. Your task is to identify the challenge mentioned post and 
        summarise the challenges in 100 words. Please do not provide any answer if you 
        do not have any. Please do not use any special symbols or characters in your answer.

        Question: {question}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm
        return chain.invoke({"question": question})
    
    def generate_skills(self, question: str) -> str:
        """
        Generate skills summary for a question.
        
        Args:
            question: User question
            
        Returns:
            Skills summary
        """
        template = """
        Role: You are an expert Software Engineer. You will be provided with a question 
        regarding a challenge faced by another software developer posted in a developer 
        discussion forum. Your task is to identify the technical skills, tools and 
        technologies required to learn by this software developer to deal with this kind 
        of challenges smoothly in future. Please provide your answer in 100 words. 
        Please do not provide any answer if you do not have any. Please do not use any 
        special symbols or characters in your answer.

        Question: {question}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm
        return chain.invoke({"question": question})
    
    def judge_relevance(self, question: str) -> str:
        """
        Judge if a question is relevant to software/cybersecurity.
        
        Args:
            question: User question
            
        Returns:
            "relevant" or "irrelevant"
        """
        template = """
        You are a security expert. Determine whether the following user question is 
        specific, technical, and related to software/cybersecurity.

        Question: {question}

        Answer with one word only. Reply with exactly one of the following, all lowercase 
        with no punctuation: relevant or irrelevant.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm
        return chain.invoke({"question": question}).strip().lower()

