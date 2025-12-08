import pandas as pd
import json
from typing import List, Dict
from .retriever_builder import build_retriever
from .data_loader import load_stackoverflow_docs
import os

def check_similarity_accuracy():
    # initialize retriever
    print("Initializing retriever...")
    docs = load_stackoverflow_docs()
    retriever, _ = build_retriever(docs)
    
    # read rewritten questions
    print("Loading rewritten questions...")
    # get project root directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    csv_path = os.path.join(root_dir, "rag-experiment/langchain_version/data/rewritten_questions_final.csv")
    print(f"Looking for CSV file at: {csv_path}")  # add debug information
    df = pd.read_csv(csv_path)
    
    # store results
    results = {
        "total_questions": 0,
        "first_position": 0,  # the first related document in the first position
        "second_position": 0,  # the first related document in the second position
        "third_position": 0,  # the first related document in the third position
        "not_found": 0,  # the first related document not in the returned results
        "details": []  # store detailed information
    }
    
    current = 0
    timer0 = time.time()
    # iterate over each question
    for index, row in df.iterrows():
        current += 1
        original_question = row['original_question']
        rewritten_question = row['alternative_question']
        
        try:
            # directly use retriever to get similar documents
            relevant_docs = retriever.get_relevant_documents(rewritten_question)
            
            # get the list of postids of the related documents
            related_posts = [doc.metadata['postid'] for doc in relevant_docs]
            
            # check the position of the original question's postid in the returned results
            original_postid = row['postid']
            position = -1
            if original_postid in related_posts:
                position = related_posts.index(original_postid)
            
            # update statistics
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
            
            # record detailed information
            results["details"].append({
                "original_question": original_question,
                "rewritten_question": rewritten_question,
                "original_postid": original_postid,
                "related_posts": related_posts,
                "position": position
            })
            
        except Exception as e:
            print(f"Error processing question {index}: {str(e)}")
            continue
    
    # calculate accuracy
    total_found = results["first_position"] + results["second_position"] + results["third_position"]
    accuracy = {
        "first_position": results["first_position"] / results["total_questions"] * 100,
        "second_position": results["second_position"] / results["total_questions"] * 100,
        "third_position": results["third_position"] / results["total_questions"] * 100,
        "not_found": results["not_found"] / results["total_questions"] * 100,
        "total_found_rate": total_found / results["total_questions"] * 100
    }
    
    # save results
    result_path = os.path.join(root_dir, "similarity_check_results.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump({
            "statistics": results,
            "accuracy": accuracy
        }, f, ensure_ascii=False, indent=2)
    
        # print results
    print("\nSimilarity check results:")
    print(f"Total questions: {results['total_questions']}")
    print(f"First position: {results['first_position']} ({accuracy['first_position']:.2f}%)")
    print(f"Second position: {results['second_position']} ({accuracy['second_position']:.2f}%)")
    print(f"Third position: {results['third_position']} ({accuracy['third_position']:.2f}%)")
    print(f"Not found: {results['not_found']} ({accuracy['not_found']:.2f}%)")
    print(f"Total found rate: {accuracy['total_found_rate']:.2f}%")
    print(f"Time taken: {time.time() - timer0:.2f} seconds")
    return results, accuracy

if __name__ == "__main__":
    check_similarity_accuracy()
