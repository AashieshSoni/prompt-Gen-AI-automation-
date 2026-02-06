'''RLAIF reward scoring
agents/metrics_collector.py'''
import ollama
from pathlib import Path

PROMPT = Path("prompts/reward_evaluation_prompt.md").read_text()

def evaluate_results(test_output: str):
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": test_output}
        ]
    )

    content = response["message"]["content"]
    reward = 1.0 if "STABLE" in content else -1.0
    return reward, content
