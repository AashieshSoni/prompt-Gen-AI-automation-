'''FastAPI endpoint triggering one iteration
api/app.py
'''
from fastapi import FastAPI
from agents.self_improver import run_self_improvement_iteration

app = FastAPI()

@app.post("/rlaif/run")
def run_iteration(api_spec: str):
    return run_self_improvement_iteration(api_spec)
