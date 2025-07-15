import streamlit as st
import os
import sys
import pandas as pd
import re
from datetime import datetime
import subprocess
import hashlib
from pathlib import Path
from utils.git_utils import get_changed_files, get_file_diff
from utils.llm_utils import suggest_test_cases, review_code
from utils.test_runner import run_tests

# Set up the Streamlit page
st.set_page_config(page_title="AI Test Automation Tool", layout="wide")

# Utility: generate a hash-based safe key
def make_safe_key(prefix: str, path: str):
    return f"{prefix}_{hashlib.md5(path.encode()).hexdigest()}"

# Function to run Vue tests
def run_vue_tests(vue_project_path):
    try:
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
        if not os.path.exists(os.path.join(vue_project_path, "package.json")):
            return f"❌ Cannot find package.json in {vue_project_path}"

        result = subprocess.run(
            [npm_cmd, "run", "test:unit"],
            cwd=vue_project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60,
            encoding="utf-8",
        )
        return result.stdout
    except Exception as e:
        return f"❌ Error running Vue tests: {e}"

# Add 'scr/' to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "scr")))

# Title
st.title("🤖 AI Test Automation Tool")

# 1. Git Repo Path
repo_path = st.text_input("Enter Git Repo Path", value="./")
st.info(f"📂 Current Repo Path: `{repo_path}`")

# 2. Detect Git Changes
if st.button("Detect Changes"):
    files = get_changed_files(repo_path)
    for i in files:
        st.write(f"📄 **Detected File:** `{i}`")
        
    if not files:
        st.info("✅ No changes detected.")
    else:
        st.session_state["detected_files"] = files
        st.success(f"🔍 Found {len(files)} changed file(s)")

# 3. Handle each changed file
if "detected_files" in st.session_state:
    files = st.session_state["detected_files"]

    for f in files:
        st.write(f"📄 **Changed File:** `{f}`")

        diff = get_file_diff(repo_path, f)
        with st.expander(f"View diff for {f}"):
            st.code(diff, language="diff")

        # Keys
        suggest_btn_key = make_safe_key("suggest_btn", f)
        suggestion_state_key = make_safe_key("suggestion", f)

        review_btn_key = make_safe_key("review_btn", f)
        review_state_key = make_safe_key("review", f)

        confirm_btn_key = make_safe_key("confirm", f)
        reject_btn_key = make_safe_key("reject", f)
        regen_btn_key = make_safe_key("regen", f)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔮 Generate Test Cases", key=suggest_btn_key):
                with st.spinner(f"Generating test suggestions for {f}..."):
                    language = "vue" if f.endswith(".vue") else "python"
                    suggestions = suggest_test_cases(f, diff, language_hint=language)
                    st.session_state[suggestion_state_key] = suggestions

        with col2:
            if st.button("🔍 Code Review", key=review_btn_key):
                with st.spinner(f"Reviewing code changes for {f}..."):
                    language = "vue" if f.endswith(".vue") else "python"
                    review_feedback = review_code(f, diff, language_hint=language)
                    st.session_state[review_state_key] = review_feedback

        # Show Code Review if available
        if review_state_key in st.session_state:
            st.subheader(f"📝 Code Review for `{f}`:")
            st.text_area("Review Feedback", st.session_state[review_state_key], height=300, key=f"review_output_{review_state_key}")

            # Save to Excel
            if st.button("💾 Save Code Review to Excel", key=f"save_excel_{review_state_key}"):
                review_text = st.session_state[review_state_key]

                match_bugs = re.search(r"\*{0,2}\s*Bugs and Issues\s*:?\s*\*{0,2}([\s\S]*?)\*{0,2}\s*Updated Code\s*:?\s*\*{0,2}",review_text, re.IGNORECASE)
                match_code = re.search(r"\*{0,2}\s*Updated Code\s*:?\s*\*{0,2}([\s\S]*?)\*{0,2}\s*Summary of Review\s*:?\s*\*{0,2}",review_text, re.IGNORECASE)
                match_summary = re.search(r"\*{0,2}\s*Summary of Review\s*:?\s*\*{0,2}\s*([\s\S]*)",review_text, re.IGNORECASE)

                if match_bugs and match_code and match_summary:
                    bugs = match_bugs.group(1).strip()
                    code = match_code.group(1).strip()
                    summary = match_summary.group(1).strip()

                    excel_dir = os.path.join(repo_path, "vue_front_end_code", "login-widget", "saved_logs", Path(f).stem)
                    os.makedirs(excel_dir, exist_ok=True)
                    

                    bugs_path = os.path.join(excel_dir, f"bugs_and_issues.txt")
                    with open(bugs_path, "w", encoding="utf-8") as file:
                        file.write(f"\n{'='*60}\n")
                        file.write(f"Original File: {f}\n")
                        file.write(f"Bugs and Issues file created at: {os.path.abspath(bugs_path)}\n")
                        file.write(f"Bugs and Issues Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        file.write(f"{'='*60}\n")
                        file.write(f"Bugs and Issues:\n{'-'*30}\n{bugs}\n")
                        file.write(f"\nSummary of Review:\n{'-'*30}\n{summary}\n")

                    # Save updated code
                    language = "vue" if f.endswith(".vue") else "python"
                    ext = {"vue": ".vue", "python": ".py", "java": ".java"}.get(language, "")
                    code_path = os.path.join(excel_dir, f"updated_code{ext}")
                    with open(code_path, "w", encoding="utf-8") as file:
                        file.write(code)

                    # Save to Excel
                    excel_path = os.path.join(excel_dir, "code_reviews.xlsx")
                    if os.path.exists(excel_path):
                        df = pd.read_excel(excel_path)
                    else:
                        df = pd.DataFrame(columns=["Sl No", "Bugs or Issues", "Updated Code", "Summary of Review"])

                    df = pd.concat([
                        df,
                        pd.DataFrame([{
                            "Sl No": len(df) + 1,
                            "Bugs or Issues": bugs,
                            "Updated Code": code,
                            "Summary of Review": summary
                        }])
                    ], ignore_index=True)

                    df.to_excel(excel_path, index=False)
                    st.success(f"✅ Code review saved to `{excel_path}`")
                else:
                    st.error("❌ Could not parse the review. Ensure it includes '**Bugs and Issues**', '**Updated Code**', '**Summary of Review**'.")

            if st.button("🔁 Regenerate Review", key=f"regen_review_{review_state_key}"):
                with st.spinner(f"Regenerating code review for {f}..."):
                    language = "vue" if f.endswith(".vue") else "python"
                    new_review = review_code(f, diff, language_hint=language)
                    st.session_state[review_state_key] = new_review
                    st.rerun()

        # Show Test Case Suggestions if available
        if suggestion_state_key in st.session_state:
            suggestions = st.session_state[suggestion_state_key]
            st.subheader(f"Suggested Test Cases for `{f}`:")
            st.code(suggestions, language="javascript" if f.endswith(".vue") else "python")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"✅ Save the Test Cases", key=confirm_btn_key):
                    is_vue = f.endswith(".vue")
                    component_name = os.path.splitext(os.path.basename(f))[0]
                    test_file_name = f"{component_name}.spec.js" if is_vue else f"{component_name}_test_cases.py"

                    test_dir = (
                        os.path.join(repo_path, "vue_front_end_code", "login-widget", "tests", "unit", "components")
                        if is_vue else
                        os.path.join(repo_path, "tests")
                    )
                    os.makedirs(test_dir, exist_ok=True)
                    test_path = os.path.join(test_dir, test_file_name)

                    with open(test_path, "w", encoding="utf-8") as file:
                        file.write(suggestions)

                    st.success(f"✅ Test file created at: `{os.path.abspath(test_path)}`")

                    # Log it
                    log_path = os.path.join(repo_path, "test_update_log.txt")
                    with open(log_path, "a", encoding="utf-8") as log_file:
                        log_file.write(f"\n{'='*60}\n")
                        log_file.write(f"Test Generation Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        log_file.write(f"{'='*60}\n")
                        log_file.write(f"Original File: {f}\n")
                        log_file.write(f"Test File Created: {test_file_name}\n")
                        log_file.write(f"Test File Path: {test_path}\n")
                        log_file.write(f"\nCode Diff:\n{'-'*30}\n{diff}\n")
                        log_file.write(f"\nGenerated Test Cases:\n{'-'*30}\n{suggestions}\n")

                    del st.session_state[suggestion_state_key]

            with col2:
                if st.button("❌ Reject Suggestions", key=reject_btn_key):
                    del st.session_state[suggestion_state_key]
                    st.info("Suggestions rejected.")

            with col3:
                if st.button("🔁 Regenerate", key=regen_btn_key):
                    with st.spinner(f"Regenerating test suggestions for {f}..."):
                        language = "vue" if f.endswith(".vue") else "python"
                        new_suggestions = suggest_test_cases(f, diff, language_hint=language)
                        st.session_state[suggestion_state_key] = new_suggestions
                        st.rerun()

# 6. Exit App
st.divider()
if st.button("Exit App"):
    st.success("🎉 Thank you for using the AI Test Automation Tool! Have a great day!")
    st.stop()
