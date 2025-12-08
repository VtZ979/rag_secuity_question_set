import pandas as pd
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import os
from typing import List
import time

def clean_response(response: str) -> str:
    """
    clean the response of LLM, remove the sentence that starts with "Here's a" or "Here is a"
    """
    cleaned_response = response.strip()
    
    # check if the response starts with "Here's a" or "Here is a"
    if cleaned_response.startswith("Here's a") or cleaned_response.startswith("Here is a"):
        # find the position of the first newline
        newline_pos = cleaned_response.find('\n')
        if newline_pos != -1:
            # delete to the newline, and keep the rest of the content
            cleaned_response = cleaned_response[newline_pos:].strip()
    
    return cleaned_response

def generate_alternative_questions(input_csv_path: str, output_csv_path: str, api_key: str = None) -> None:
    """
    Reads a CSV file containing StackOverflow questions, generates alternative formulations
    for each question using an LLM, and saves the results to a new CSV file.
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_csv_path (str): Path to save the output CSV file
        api_key (str, optional): OpenAI API key. If None, will try to get from environment variable
    """
    # Read the CSV file
    df = pd.read_csv(input_csv_path)
    
    # Initialize LLM
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    llm = Ollama(
        model="llama3",
        temperature=0.7
    )
    
    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=["question"],
        template="""Please rewrite the following question in a different way while maintaining the same meaning and intent. 
        The new version should be clear and natural, but use different wording and structure:
        
        Original question: {question}
        
        Rewritten question:"""
    )
    
    # Process each question
    results = []
    current = 0
    for idx, row in df.iterrows():
        try:
            # Get the original question
            original_question = row['original question']
            if pd.isna(original_question):
                continue
                
            # Generate alternative question
            prompt = prompt_template.format(question=original_question)
            alternative_question = llm(prompt)
            
            # Add to results
            results.append({
                'postid': row['postid'],
                'original_question': original_question,
                'alternative_question': alternative_question.strip()
            })
            
            print(current)
            current+=1
        except Exception as e:
            print(f"Error processing row {idx}: {str(e)}")
            continue
    
    # Create DataFrame from results
    output_df = pd.DataFrame(results)
    
    # Save to CSV
    output_df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")

def clean_generated_file(input_csv_path: str, output_csv_path: str) -> None:
    """
    clean the generated file, remove the prefix of the answer
    
    Args:
        input_csv_path (str): the path of the input CSV file
        output_csv_path (str): the path of the output CSV file
    """
    # read the CSV file
    df = pd.read_csv(input_csv_path)
    
    # clean each answer
    for idx, row in df.iterrows():
        if pd.isna(row['alternative_question']):
            continue
            
        # clean the answer
        cleaned_question = clean_response(row['alternative_question'])
        df.at[idx, 'alternative_question'] = cleaned_question
    
    # save the cleaned file
    df.to_csv(output_csv_path, index=False)
    print(f"Cleaned file saved to {output_csv_path}")

if __name__ == "__main__":
    print("Starting the script...")
    from langchain_community.llms import Ollama
    import os
    import sys
    
    print("Importing modules...")
    
    # add the project root to the Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    sys.path.append(project_root)
    print(f"Project root: {project_root}")
    
    # initialize Ollama
    print("Initializing Ollama...")
    llm = Ollama(
        model="llama3",  # use the llama3 model
        temperature=0.7
    )
    print("Ollama initialized successfully")
    
    # file path
    input_csv = os.path.join(project_root, "rag-experiment/langchain_version/data/StackOverflow_security_sample_labelled_all.csv")
    output_csv = os.path.join(project_root, "rag-experiment/langchain_version/data/rewritten_questions.csv")
    print(f"Input CSV: {input_csv}")
    print(f"Output CSV: {output_csv}")
    
    # check if the file exists
    if not os.path.exists(input_csv):
        print(f"Error: Input file does not exist at {input_csv}")
        sys.exit(1)
    
    # run the function
    print("Starting to process questions...")
    #generate_alternative_questions(input_csv, output_csv, llm)
    print("Processing completed!")

    # file path
    input_csv = "../rag-experiment/langchain_version/data/rewritten_questions.csv"
    output_csv = "../rag-experiment/langchain_version/data/rewritten_questions_final.csv"
    
    # run the clean function
    clean_generated_file(input_csv, output_csv)

