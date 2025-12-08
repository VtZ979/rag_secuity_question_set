import pandas as pd
# Compatible import for Document - try new location first, fallback to old
try:
    from langchain_core.documents import Document
except ImportError:
    # Fallback for older langchain versions
    from langchain.docstore.document import Document
import os

def load_stackoverflow_docs():
    # use correct relative path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    csv_file_path = os.path.join(project_root, "data", "StackOverflow_security_sample_labelled_all.csv")
    
    # use pandas to read CSV file, specify encoding as UTF-8
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    
    # convert DataFrame to Document object list
    docs = []
    for _, row in df.iterrows():
        # combine question and answer as document content
        content = f"Question: {row['original question']}\n\nAnswer: {row['answers']}"
        
        # create metadata dictionary
        metadata = {
            "postid": row['postid'],
            "tags": row['tags'],
            "title": row['title'],
            "words": row['words'],
            "creation_date": row['creation_date'],
            "Related": row['Related'],
            "challenges": row['challenges'],
            "skills": row['skills'],
            "accepted_answers": row['accepted answers'],
            "Label1": row['Label1'],
            "original_question": row['original question'],
            "topic_id": row['topic_id'],
            "category": row['category'],
            "subcategory": row['subcategory']
        }
        
        # create Document object
        doc = Document(page_content=content, metadata=metadata)
        docs.append(doc)
    
    return docs
