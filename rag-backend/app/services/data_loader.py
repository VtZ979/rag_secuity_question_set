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
        # Combine question and answer as document content
        content = f"Question: {row['original question']}\n\nAnswer: {row['answers']}"
        
        # Create metadata dictionary
        metadata = {
            "postid": row.get('postid', ''),
            "tags": row.get('tags', ''),
            "title": row.get('title', ''),
            "words": row.get('words', ''),
            "creation_date": row.get('creation_date', ''),
            "Related": row.get('Related', ''),
            "challenges": row.get('challenges', ''),
            "skills": row.get('skills', ''),
            "accepted_answers": row.get('accepted answers', ''),
            "Label1": row.get('Label1', ''),
            "original_question": row.get('original question', ''),
            "topic_id": row.get('topic_id', ''),
            "category": row.get('category', ''),
            "subcategory": row.get('subcategory', '')
        }
        
        # Create Document object
        doc = Document(page_content=content, metadata=metadata)
        docs.append(doc)
    
    return docs

