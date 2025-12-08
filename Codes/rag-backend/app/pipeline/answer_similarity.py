from typing import Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from ollama import chat
import time

class AnswerSimilarityResult(BaseModel):
    similarity: Literal[
        "Exact Match",
        "High Similarity",
        "Partial Match",
        "Low Similarity",
        "No Match"
    ] = Field(
        ...,
        description="The similarity between the accepted answer and LLM solution"
    )
    explanation: str = Field(
        ...,
        description="A brief explanation of the similarity"
    )

# Manually defined simplified schema for Ollama format parameter
# This avoids issues with Pydantic's schema() method which may include
# extra fields (definitions, $defs) that Ollama doesn't support
ANSWER_SIMILARITY_SCHEMA = {
    "type": "object",
    "properties": {
        "similarity": {
            "type": "string",
            "enum": [
                "Exact Match",
                "High Similarity",
                "Partial Match",
                "Low Similarity",
                "No Match"
            ]
        },
        "explanation": {
            "type": "string"
        }
    },
    "required": ["similarity", "explanation"]
}

def calculate_answer_similarity(accepted_answer: str, llm_solution: str) -> str:
    """
    Calculate the similarity between the accepted answer and LLM solution.
    """
    # define the similarity types and their explanations
    similarity_types = {
        "Exact Match": "The LLM solution is almost identical to the accepted answer.",
        "High Similarity": "The LLM solution closely matches the key points of the accepted answer.",
        "Partial Match": "The LLM solution shares some common elements with the accepted answer.",
        "Low Similarity": "The LLM solution has minimal overlap with the accepted answer.",
        "No Match": "The LLM solution is completely different from the accepted answer."
    }

    # Add retry logic for Ollama calls
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = chat(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a smart assistant. Analyze the similarity between the accepted answer and LLM solution.if accepted answer is empty, return 'No Match'.\n"
                            "You must respond in JSON format with two fields:\n"
                            "- 'similarity': one of the following labels:\n"
                            "  1. 'Exact Match'\n"
                            "  2. 'High Similarity'\n"
                            "  3. 'Partial Match'\n"
                            "  4. 'Low Similarity'\n"
                            "  5. 'No Match'\n"
                            "- 'explanation': a brief explanation of the similarity\n\n"
                            "Example response:\n"
                            "{\n"
                            "  'similarity': 'High Similarity',\n"
                            "  'explanation': 'The LLM solution closely matches the key points of the accepted answer.'\n"
                            "}"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Accepted Answer:\n{accepted_answer}\n\nLLM Solution:\n{llm_solution}"
                    }
                ],
                model="llama3",
                format=ANSWER_SIMILARITY_SCHEMA,
            )

            result = AnswerSimilarityResult.parse_raw(response['message']['content'])
            print(f"Accepted Answer: {accepted_answer[:100]}...; LLM Solution: {llm_solution[:100]}...; similarity:=={result.similarity}; explanation:=={result.explanation}")
            
            # return the full prompt text
            return f"{result.similarity} – {similarity_types[result.similarity]}"
        except Exception as e:
            error_str = str(e)
            # Check if it's a crash/502 error
            is_crash_error = "502" in error_str or "500" in error_str or "exit status" in error_str or "terminated" in error_str
            
            if attempt < max_retries - 1:
                # If it's a crash error, wait longer for Ollama to recover
                wait_time = 10 if is_crash_error else 2
                print(f"Ollama call failed, retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries}): {e}")
                if is_crash_error:
                    print("[WARNING] Ollama process may have crashed. Waiting longer for recovery...")
                time.sleep(wait_time)
            else:
                print(f"Ollama call failed after {max_retries} attempts: {e}")
                if is_crash_error:
                    print("[ERROR] Ollama process crashed. Returning default value.")
                # Return a default value instead of crashing
                return "Partial Match – The LLM solution shares some common elements with the accepted answer." 