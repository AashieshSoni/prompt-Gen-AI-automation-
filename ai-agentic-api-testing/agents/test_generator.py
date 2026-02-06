'''Uses Ollama to generate REST + GraphQL tests
test_generator.py'''
import ollama
from pathlib import Path

PROMPT = Path("prompts/test_generation_prompt.md").read_text()

def generate_tests(api_spec: str):
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": api_spec}
        ]
    )

    tests = response["message"]["content"].split("\n")
    return [t for t in tests if t.strip()]
