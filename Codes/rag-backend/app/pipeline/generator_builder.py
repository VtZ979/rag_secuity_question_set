from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from .vader_analyzer import VaderSentimentAnalyzer
import numpy as np
from .classifier import SecurityQuestionClassifier
from .LDA_classify import classify_question

sentiment_analyzer = VaderSentimentAnalyzer()

"""
  Compute the cosine similarity between two vectors.
"""
def cosine_similarity(vec1, vec2):

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


"""
    Process relevant documents and generate RAG response structures.

    :param relevant_docs: Documents retrieved based on the user question.
    :param question: The input question from the user.
    :param prompt: ChatPromptTemplate used to guide the LLM's response format.
    :param llm: The LLM instance (llma3).
    :param embedding: The embedding model used to compute similarity (e.g., HuggingFaceEmbeddings).
    :return: A list of structured response dictionaries.
"""
def process_relevant_docs(relevant_docs, question, prompt, llm, embedding, clf):
    """
    Optimized version: Only 1 Ollama call for main answer.
    All other information is extracted from document metadata or computed using embeddings.
    """
    # Prompt for main answer - combine all relevant documents as context
    template = """
      You are an expert in software development, specifically in the field of software security. 
      Based on the following context from relevant Stack Overflow posts, provide a comprehensive answer to the question.

      Your answer should follow this format:

      Summary : [Programming Language] → [Framework] → [API or Configuration]
      - Bullet point 1: key insight or step
      - Bullet point 2: key insight or step
      - Bullet point 3: ...

      Be concise and only include details that are directly relevant from the context. The summary line should be under 20 words.

      Context:
      {context}

      Question:
      {question}

      Answer:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Combine all relevant documents into a single context
    combined_context = "\n\n".join([
        f"Post {idx + 1}:\nTitle: {doc.metadata.get('title', 'N/A')}\n"
        f"Question: {doc.metadata.get('original_question', doc.page_content[:200])}\n"
        f"Answer: {doc.metadata.get('accepted_answers', 'N/A')}\n"
        for idx, doc in enumerate(relevant_docs[:3])  # Limit to top 3 documents
    ])
    
    # Get category information from classifier (no Ollama needed)
    classifier_label = clf.predict(question)
    LDA_result = classify_question(question)
    
    # Simple relevance check using keywords (no Ollama needed)
    security_keywords = ['security', 'authentication', 'authorization', 'encryption', 'vulnerability', 
                         'attack', 'secure', 'password', 'token', 'session', 'cookie', 'csrf', 'xss', 'sql injection']
    is_relevant = any(keyword in question.lower() for keyword in security_keywords)
    
    if is_relevant:
        category_j = (
            f"Your question is a {classifier_label} question. The security topic of this question falls under the category: {LDA_result['subcategory']}."
            "This may be your knowledge blind spot, it is recommended that you learn more and pay attention to such security issues in the future."
        )
    else:
        category_j = "The question does not appear to be related to cybersecurity, or lacks sufficient context to categorize. Please provide more technical details or context."

    # ONLY ONE Ollama call for the main answer
    print("[INFO] Generating main answer from combined context...")
    try:
        llm_answer = (prompt | llm).invoke({"context": combined_context, "question": question})
    except Exception as e:
        print(f"[WARNING] Main answer generation failed: {e}")
        llm_answer = "Unable to generate answer due to service error."
    
    # Extract challenges and skills from document metadata (no Ollama needed)
    # Use the first document's metadata, or combine if available
    challenges = relevant_docs[0].metadata.get('challenges', 'Challenges information not available.') if relevant_docs else "No challenges information available."
    skills = relevant_docs[0].metadata.get('skills', 'Skills information not available.') if relevant_docs else "No skills information available."
    
    response = {
        "answer": {
            "user_question": question,
            "llm_answer": llm_answer,
            "challenges": challenges,
            "skills": skills,
            "category": category_j
        },
        "related_post": []
    }

    # Process related posts - NO Ollama calls, only use metadata and embeddings
    for idx, relevant_doc in enumerate(relevant_docs):
        print(f"[INFO] Processing document {idx + 1}/{len(relevant_docs)} (using metadata only)...")
        
        # Calculate similarity using embeddings (no Ollama needed)
        question_embedding = embedding.embed_query(question)
        doc_embedding = embedding.embed_query(relevant_doc.page_content)
        similarity_score = cosine_similarity(question_embedding, doc_embedding)
        
        # Convert similarity score to text label
        if similarity_score > 0.8:
            similarity = "High Similarity – The document is highly relevant to your question."
        elif similarity_score > 0.6:
            similarity = "Partial Overlap – The document partially addresses your question."
        elif similarity_score > 0.4:
            similarity = "Low Similarity – The document has some connection to your question."
        else:
            similarity = "No Overlap – The document is not directly related to your question."
        
        # Calculate answer similarity using embeddings (no Ollama needed)
        accepted_answer = relevant_doc.metadata.get('accepted_answers', '')
        if accepted_answer:
            answer_embedding = embedding.embed_query(accepted_answer)
            answer_similarity_score = cosine_similarity(question_embedding, answer_embedding)
            
            if answer_similarity_score > 0.7:
                answer_similarity = "High Similarity – The accepted answer closely matches your question."
            elif answer_similarity_score > 0.5:
                answer_similarity = "Partial Match – The accepted answer partially addresses your question."
            else:
                answer_similarity = "Low Similarity – The accepted answer has limited relevance."
        else:
            answer_similarity = "No accepted answer available for comparison."
        
        # Get sentiment (no Ollama needed, uses VADER)
        ori_q = relevant_doc.metadata.get('original_question', '')
        sentiment_result = sentiment_analyzer.invoke(ori_q)
        sentiment_label = sentiment_result.get("sentiment", "")
        
        # Construct the related post structure
        related_post = {
            "post_id": relevant_doc.metadata.get('postid', ''),
            "title": relevant_doc.metadata.get('title', ''),
            "ori_question": relevant_doc.metadata.get('original_question', ''),
            "accepted_answers": relevant_doc.metadata.get('accepted_answers', ''),
            "similarity": similarity,
            "llmSolution": "The LLM-generated answer is shown in the main response above, which combines insights from all relevant documents.",  # No separate LLM call per document
            "answer_similarity": answer_similarity,
            "challenges": relevant_doc.metadata.get('challenges', ''),
            "skills": relevant_doc.metadata.get('skills', ''),
            "sentimental": sentiment_label,
            "category": f"This question is a {relevant_doc.metadata.get('Label1', '')} question. The security topic of this question falls under the category: {relevant_doc.metadata.get('subcategory', '')}."
        }    
        response["related_post"].append(related_post)

    return response

