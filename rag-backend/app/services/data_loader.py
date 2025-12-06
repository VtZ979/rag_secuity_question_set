"""
Data loading service for Stack Overflow security questions
"""
import sys
from pathlib import Path
import pandas as pd
from langchain.docstore.document import Document

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.settings import CSV_DATA_PATH


def load_stackoverflow_docs(csv_path=None):
    """
    Load Stack Overflow security questions from CSV and convert to LangChain Documents.
    
    Args:
        csv_path: Optional path to CSV file. If None, uses default from settings.
        
    Returns:
        List of LangChain Document objects
    """
    if csv_path is None:
        csv_path = CSV_DATA_PATH
    
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Read CSV with UTF-8 encoding
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    # Convert DataFrame rows to Document objects
    docs = []
    for _, row in df.iterrows():
        # Get question and answer, handle None/NaN values
        question = row.get('original question', '')
        answer = row.get('answers', '')
        
        # Convert to string and handle None/NaN
        question = str(question) if pd.notna(question) else ''
        answer = str(answer) if pd.notna(answer) else ''
        
        # Skip documents with empty content
        if not question.strip() and not answer.strip():
            continue
        
        # Combine question and answer as document content
        content = f"Question: {question}\n\nAnswer: {answer}"
        
        # Ensure content is not empty
        if not content.strip():
            continue
        
        # Create metadata dictionary (handle None/NaN values)
        metadata = {
            "postid": str(row.get('postid', '')) if pd.notna(row.get('postid')) else '',
            "tags": str(row.get('tags', '')) if pd.notna(row.get('tags')) else '',
            "title": str(row.get('title', '')) if pd.notna(row.get('title')) else '',
            "words": str(row.get('words', '')) if pd.notna(row.get('words')) else '',
            "creation_date": str(row.get('creation_date', '')) if pd.notna(row.get('creation_date')) else '',
            "Related": str(row.get('Related', '')) if pd.notna(row.get('Related')) else '',
            "challenges": str(row.get('challenges', '')) if pd.notna(row.get('challenges')) else '',
            "skills": str(row.get('skills', '')) if pd.notna(row.get('skills')) else '',
            "accepted_answers": str(row.get('accepted answers', '')) if pd.notna(row.get('accepted answers')) else '',
            "Label1": str(row.get('Label1', '')) if pd.notna(row.get('Label1')) else '',
            "original_question": question,
            "topic_id": str(row.get('topic_id', '')) if pd.notna(row.get('topic_id')) else '',
            "category": str(row.get('category', '')) if pd.notna(row.get('category')) else '',
            "subcategory": str(row.get('subcategory', '')) if pd.notna(row.get('subcategory')) else ''
        }
        
        # Create Document object
        doc = Document(page_content=content, metadata=metadata)
        docs.append(doc)
    
    return docs

