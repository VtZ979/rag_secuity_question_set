from typing import Literal
# Compatible import for pydantic - try langchain_core.pydantic_v1 first, fallback to pydantic
try:
    from langchain_core.pydantic_v1 import BaseModel, Field
except ImportError:
    # Fallback to standard pydantic if pydantic_v1 is not available
    from pydantic import BaseModel, Field
from ollama import chat
import time

class RelevanceResult(BaseModel):
    relevance: Literal[
        "Exact Match",
        "No Overlap",
        "Partial Overlap",
        "Subset",
        "Superset",
        "Upstream/Downstream Relation",
        "Conceptual Intersection",
        "Alternative Technology Context"
    ] = Field(
        ...,
        description="The relationship between the question and the given programming technique"
    )
    explanation: str = Field(
        ...,
        description="A brief explanation of the relationship"
    )

# Manually defined simplified schema for Ollama format parameter
# This avoids issues with Pydantic's schema() method which may include
# extra fields (definitions, $defs) that Ollama doesn't support
RELEVANCE_SCHEMA = {
    "type": "object",
    "properties": {
        "relevance": {
            "type": "string",
            "enum": [
                "Exact Match",
                "No Overlap",
                "Partial Overlap",
                "Subset",
                "Superset",
                "Upstream/Downstream Relation",
                "Conceptual Intersection",
                "Alternative Technology Context"
            ]
        },
        "explanation": {
            "type": "string"
        }
    },
    "required": ["relevance", "explanation"]
}

def classify_relevance(question: str, Language: str) -> str:
    """
    use llm to check whether the question is related to the given programming technique, return the relationship type and explanation.
    """
    # define the relationship types and their explanations
    relationship_types = {
        "Exact Match": "The user's question fully aligns with the given technique.",
        "No Overlap": "The user's question is unrelated to the given technique.",
        "Partial Overlap": "The user's question partially involves the given technique.",
        "Subset": "The user's question is entirely within a smaller scope of the given technique.",
        "Superset": "The user's question covers multiple techniques, including the given one.",
        "Upstream/Downstream Relation": "The user's question uses a technology that builds on or underlies the given one.",
        "Conceptual Intersection": "The user's question touches on a broader concept that the given technique is part of.",
        "Alternative Technology Context": "The user's question uses a different language/tech that serves a similar purpose."
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
                            "You are a smart assistant. Analyze the user's question and determine the relationship between the question's relevant programming techniques "
                            "and the given programming technique: " + Language + ".\n"
                            "You must respond in JSON format with two fields:\n"
                            "- 'relevance': one of the following labels:\n"
                            "  1. 'Exact Match'\n"
                            "  2. 'No Overlap'\n"
                            "  3. 'Partial Overlap'\n"
                            "  4. 'Subset'\n"
                            "  5. 'Superset'\n"
                            "  6. 'Upstream/Downstream Relation'\n"
                            "  7. 'Conceptual Intersection'\n"
                            "  8. 'Alternative Technology Context'\n"
                            "- 'explanation': a brief explanation of the relationship\n\n"
                            "Example response:\n"
                            "{\n"
                            "  'relevance': 'Exact Match',\n"
                            "  'explanation': 'The user's question fully aligns with the given technique.'\n"
                            "}"
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                model="llama3",
                format=RELEVANCE_SCHEMA,
            )

            result = RelevanceResult.parse_raw(response['message']['content'])
            print(f"question : {question}; relationship type:=={result.relevance}; explanation:=={result.explanation}")
            
            # return the full prompt text
            return f"{result.relevance} – {relationship_types[result.relevance]}"
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
                return "Partial Overlap – The user's question partially involves the given technique."