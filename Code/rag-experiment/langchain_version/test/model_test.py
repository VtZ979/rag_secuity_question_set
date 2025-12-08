from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import shutil
import os
import pandas as pd
from langchain.docstore.document import Document

model_list = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
]

csv_file_path = "StackOverflow_security_sample_labelled_all.csv"
    
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


query = "php password"  # test question
all_results = []  # collection of result for all models

for model_name in model_list:
    print("=" * 60)
    print(f"Testing model: {model_name}")
    try:
        persist_dir = f"./chroma_db_{model_name.replace('/', '_')}"

        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)

        embedding = HuggingFaceEmbeddings(model_name=model_name)

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embedding,
            persist_directory=persist_dir
        )

        retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3})
        results = retriever.invoke(query)

        print(f"Top 3 results for model [{model_name}]:")
        for i, r in enumerate(results, 1):
            preview = r.page_content[:100].replace("\n", " ")
            print(f"{i}. {preview}...\n")
            all_results.append({
                "model": model_name,
                "query": query,
                "postid": r.metadata.get("postid", ""),
                "original_question": r.metadata.get("original_question", "")
            })

    except Exception as e:
        print(f" Error using model {model_name}: {e}")

df_results = pd.DataFrame(all_results)
df_results.to_csv("embedding_model_comparison.csv", index=False)
print("All model retrieval results have been saved to embedding_model_comparison.csv")

