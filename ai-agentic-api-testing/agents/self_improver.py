'''Runs one full RLAIF iteration
self_improver.py'''

from agents.test_generator import generate_tests
from agents.executor_client import execute_tests
from agents.metrics_collector import evaluate_results
from agents.vectorstore_client import store_learning

def run_self_improvement_iteration(api_spec: str):
    """
    1. Generate tests from spec
    2. Execute tests
    3. Evaluate via RLAIF
    4. Store learning in ChromaDB
    """
    tests = generate_tests(api_spec)
    results = execute_tests(tests)
    reward, insights = evaluate_results(results)
    store_learning(api_spec, results, reward, insights)

    return {
        "reward": reward,
        "insights": insights,
        "executed_tests": len(tests)
    }
