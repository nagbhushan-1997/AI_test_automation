# from ollama import Client

# # Initialize Ollama client (works locally)
# client = Client()

# def suggest_test_changes(filename, code_diff):
#     prompt = f"""You're an AI test expert. Given the following code diff from `{filename}`, generate or update the relevant Python test case accordingly.

# Diff:
# {code_diff}

# Output only the updated or new test case code:"""

#     response = client.chat(
#         model='llama3.2',  # Or use your specific version like 'llama3:instruct' if tagged that way
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response['message']['content']
import ollama

def suggest_test_changes(filename, code_diff):
    prompt = f"""
You are an expert test case generator. Your task is to generate unit test code for only the functions that are added or modified in the provided code diff.

Inputs:
- filename: {filename}
- code diff: {code_diff}

Instructions:
- Automatically detect the programming language (Python or Java) from the code diff.
- If the code is in Python, generate `pytest` unit test code.
- If the code is in Java, generate `JUnit 5` test code.
- Do not generate tests for unchanged functions.
- Generate tests for all functions that are added or modified in the code diff.
- Ensure the test code is valid and can be run directly.
- Output only the valid test code as a single source file.
- Do not include any markdown formatting (e.g., triple backticks), comments, explanations, or pseudocode.
- Each function must include:
  - At least one happy-path (valid input) test.
  - At least one invalid or boundary test case.
- For Python: assume the module can be imported using `from scr.<base_module> import <function>`.
- For Java: place tests in a class named `<ClassName>Test` derived from the filename if applicable.

Output:
ONLY and ONLY GIVE Me the complete test code for the changed functions, as valid code.
STRICTLY DO NOT INCLUDE any other Natural Language or markdown.
"""
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {"role": "system", "content": "You are a helpful and expert Python test case generator."},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0,        
                "top_p": 1,
                "repeat_penalty": 1
            }
        )
        
        output = response['message']['content'].strip()
        output = output.replace('```python', '').replace('```java', '').replace('```javascript', '').replace('```','').strip()
        return output if output else "No test code generated. Please check the input diff."

    except Exception as e:
        return f"Error generating test: {e}"