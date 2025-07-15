# import subprocess
# import sys

# def run_tests(path):
#     result = subprocess.run([sys.executable, "-m", "pytest", path], capture_output=True, text=True)
#     return result.stdout + "\n" + result.stderr

import subprocess

def run_tests(path):
    result = subprocess.run(
        ["pytest", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Decode manually using utf-8 and replace undecodable characters
    stdout_decoded = result.stdout.decode("utf-8", errors="replace")
    stderr_decoded = result.stderr.decode("utf-8", errors="replace")
    
    return stdout_decoded + "\n" + stderr_decoded
