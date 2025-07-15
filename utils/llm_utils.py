import ollama
    # Replace this with your actual LLM API call
from ollama import chat  # or your existing model
def suggest_test_cases(filename, code_diff, language_hint):
    prompt = f"""
You are an expert test case generator. Your task is to generate unit test code for only the functions or components that are added or modified in the provided code diff.

Inputs:
- filename: {filename}
- code diff: {code_diff}
- language hint: {language_hint}

Instructions:
- If a language hint is provided (like '{language_hint}'), prioritize it over auto-detection.
- If the language is:
  - Python: generate `pytest` unit test code.
  - Java: generate `JUnit 5` test code.
  - JavaScript: generate `Jest` test code.
  - Vue.js: generate `Jest` or `Vitest` unit test code using `@vue/test-utils`.

Test Case Requirements:
- Generate tests only for changed/added logic.
- Each test must include:
  - At least one happy-path test.
  - At least one invalid or boundary test.

Format Rules:
- Output only valid test code.
- STRICTLY DO NOT INCLUDE any explanations, markdown, triple backticks, or comments.
- Vue test files must import the component and mount it using `shallowMount()` or `mount()` from `@vue/test-utils`.
- For Python: assume `from scr.<base_module> import <function>`.
- For Java: put tests in `<ClassName>Test.java`.
- For Vue: assume component is imported like `import Component from '@/components/<Component>.vue'`.

Output:
ONLY and ONLY GIVE ME the complete test code as a valid source file.
STRICTLY DO NOT INCLUDE any markdown formatting, explanations, or non-code content.
"""

    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {"role": "system", "content": "You are a helpful and expert test case generator."},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0,
                "top_p": 1,
                "repeat_penalty": 1
            }
        )

        output = response['message']['content'].strip()
        return output.replace('```python', '').replace('```java', '').replace('```javascript', '').replace('```vue', '').replace('```', '').strip()

    except Exception as e:
        return f"Error generating test: {e}"


def review_code(filename: str, diff: str, language_hint: str = "python") -> str:
  
    prompt = f"""You are a senior code reviewer.

Here is the diff of a file `{filename}` written in {language_hint}:

{diff}

Please provide a code review:-
- Identify potential bugs or issues.
- Suggest improvements or best practices.
- Ensure the code follows the language's conventions.
- If the language is Python, check for PEP 8 compliance.
- If the language is Java, check for Java best practices.
- If the language is Vue.js, ensure proper component structure and testing practices.
 

First the output should include 'bugs and issues', secondly it should include 'updated code', and finally it should include 'summary of review'.

"""



    response = chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']