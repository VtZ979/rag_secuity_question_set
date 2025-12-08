import pandas as pd
import json
import time
from typing import List, Dict
from .retriever_builder import build_retriever
from .data_loader import load_stackoverflow_docs
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# define the model list
MODEL_LIST = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
]

def check_similarity_accuracy(model_name: str = "sentence-transformers/all-MiniLM-L6-v2", search_type: str = "mmr"):
    # initialize retriever
    print(f"\nTesting model: {model_name} with search_type: {search_type}")
    print("Initializing retriever...")
    docs = load_stackoverflow_docs()
    
    # create a independent vector store directory for each model
    persist_dir = f"./chroma_db_{model_name.replace('/', '_')}"
    retriever, _ = build_retriever(docs, persist_directory=persist_dir, search_type=search_type)
    
    # read rewritten questions
    print("Loading rewritten questions...")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    csv_path = os.path.join(root_dir, "rag-experiment/langchain_version/data/rewritten_questions_final.csv")
    print(f"Looking for CSV file at: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # store results
    results = {
        "model": model_name,
        "search_type": search_type,
        "total_questions": 0,
        "first_position": 0,
        "second_position": 0,
        "third_position": 0,
        "not_found": 0,
        "details": [],
        "total_time": 0
    }
    
    current = 0
    timer0 = time.time()
    
    # iterate over each question
    for index, row in df.iterrows():
        current += 1
        original_question = row['original_question']
        rewritten_question = row['alternative_question']
        
        try:
            # measure time for each query
            query_start = time.time()
            relevant_docs = retriever.get_relevant_documents(rewritten_question)
            query_time = time.time() - query_start
            
            related_posts = [doc.metadata['postid'] for doc in relevant_docs]
            original_postid = row['postid']
            position = -1
            if original_postid in related_posts:
                position = related_posts.index(original_postid)
            
            results["total_questions"] += 1
            if position == 0:
                results["first_position"] += 1
            elif position == 1:
                results["second_position"] += 1
            elif position == 2:
                results["third_position"] += 1
            else:
                results["not_found"] += 1
            
            print(f"Processing question {current}/{len(df)}")
            
            results["details"].append({
                "original_question": original_question,
                "rewritten_question": rewritten_question,
                "original_postid": original_postid,
                "related_posts": related_posts,
                "position": position,
                "query_time": query_time
            })
            
        except Exception as e:
            print(f"Error processing question {index}: {str(e)}")
            continue
    
    results["total_time"] = time.time() - timer0
    
    # calculate accuracy
    total_found = results["first_position"] + results["second_position"] + results["third_position"]
    accuracy = {
        "first_position": results["first_position"] / results["total_questions"] * 100,
        "second_position": results["second_position"] / results["total_questions"] * 100,
        "third_position": results["third_position"] / results["total_questions"] * 100,
        "not_found": results["not_found"] / results["total_questions"] * 100,
        "total_found_rate": total_found / results["total_questions"] * 100,
        "avg_query_time": results["total_time"] / results["total_questions"]
    }
    
    # print results
    print(f"\nResults for {model_name} with {search_type}:")
    print(f"Total questions: {results['total_questions']}")
    print(f"First position: {results['first_position']} ({accuracy['first_position']:.2f}%)")
    print(f"Second position: {results['second_position']} ({accuracy['second_position']:.2f}%)")
    print(f"Third position: {results['third_position']} ({accuracy['third_position']:.2f}%)")
    print(f"Not found: {results['not_found']} ({accuracy['not_found']:.2f}%)")
    print(f"Total found rate: {accuracy['total_found_rate']:.2f}%")
    print(f"Total time: {results['total_time']:.2f} seconds")
    print(f"Average query time: {accuracy['avg_query_time']:.2f} seconds")
    
    return results, accuracy

def run_all_models_comparison():
    all_results = []
    search_types = ["similarity", "mmr", "similarity_score_threshold"]
    
    for model_name in MODEL_LIST:
        for search_type in search_types:
            try:
                results, accuracy = check_similarity_accuracy(model_name, search_type)
                all_results.append({
                    "model": model_name,
                    "search_type": search_type,
                    "accuracy": accuracy,
                    "total_time": results["total_time"]
                })
            except Exception as e:
                print(f"Error testing {model_name} with {search_type}: {str(e)}")
                continue
    
    # Save comparison results
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    result_path = os.path.join(root_dir, "model_comparison_results.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    # Print comparison summary
    print("\nModel Comparison Summary:")
    print("=" * 80)
    for result in all_results:
        print(f"\nModel: {result['model']}")
        print(f"Search Type: {result['search_type']}")
        print(f"Total Found Rate: {result['accuracy']['total_found_rate']:.2f}%")
        print(f"Total Time: {result['total_time']:.2f} seconds")
        print(f"Average Query Time: {result['accuracy']['avg_query_time']:.2f} seconds")
        print("-" * 40)

if __name__ == "__main__":
    run_all_models_comparison()
