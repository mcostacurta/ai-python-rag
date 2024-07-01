import os
from query_data import query_rag
from langchain_community.llms.ollama import Ollama

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

MODEL = os.getenv('MODEL', 'mistral')

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test_nba_2020_winner():
    assert query_and_validate(
        question="Who is the nba winner of 2020?",
        expected_response="Los Angeles Lakers",
    )

def test_nfl_teams():
    assert query_and_validate(
        question="How many teams are in NFL? (Answer with one number)",
        expected_response="32",
    )

def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model=MODEL)
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
