'''Executes tests (Robot / API runner abstraction)
executor_client.py
'''
import subprocess
import tempfile

def execute_tests(tests: list[str]) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".robot") as f:
        f.write("*** Test Cases ***\n")
        for t in tests:
            f.write(f"{t}\n    Log    Executing\n")

        f.flush()
        result = subprocess.run(
            ["robot", f.name],
            capture_output=True,
            text=True
        )

    return result.stdout + result.stderr
