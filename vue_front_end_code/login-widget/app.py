import streamlit as st
import os
import sys
from datetime import datetime
st.set_page_config(page_title="AI Test Automation Tool", layout="wide")

# Ensure 'scr/' is in the Python path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "scr")))

from utils.git_utils import get_changed_files, get_file_diff
from utils.llm_utils import suggest_test_changes
from utils.test_runner import run_tests

st.title("🤖 AI Test Automation Tool")

# 1. Git Repo Path
repo_path = st.text_input("Enter Git Repo Path", value="./")
st.info(f"📂 Current Repo Path: `{repo_path}`")

# 2. Detect Git Changes
if st.button("Detect Changes"):
    files = get_changed_files(repo_path)

    if not files:
        st.info("✅ No changes detected.")
    else:
        st.session_state["detected_files"] = files
        st.success(f"🔍 Found {len(files)} changed file(s)")

# Display detected files and handle suggestions
if "detected_files" in st.session_state:
    files = st.session_state["detected_files"]

    for f in files:
        st.write(f"📄 **Changed File:** `{f}`")

        # Show the diff
        diff = get_file_diff(repo_path, f)
        with st.expander(f"View diff for {f}"):
            st.code(diff, language="diff")

        # Suggest Test Button
        suggest_btn_key = f"suggest_{f}"

        if st.button(f"🔮 Generate Test Cases for {f}", key=suggest_btn_key):
            with st.spinner(f"Generating test suggestions for {f}..."):
                suggestions = suggest_test_changes(f, diff)
                st.session_state[f"suggestions_{f}"] = suggestions

        # If suggestion exists, show it and allow confirmation or regeneration
        if f"suggestions_{f}" in st.session_state:
            suggestions = st.session_state[f"suggestions_{f}"]

            st.subheader(f"💡 Suggested Test Cases for `{f}`:")
            st.code(suggestions, language="python")

            # Create three columns for buttons
            col1, col2, col3 = st.columns(3)

            with col1:
                confirm_btn_key = f"confirm_{f}"
                if st.button(f"✅ Accept & Save Test Cases", key=confirm_btn_key):
                    if "def test_" in suggestions and not suggestions.startswith("Error"):
                        base_name = os.path.splitext(f)[0]
                        base_name = base_name.replace("scr/", "").replace("\\", "_").replace("/", "_")
                        test_file_name = f"{base_name}_test_cases.py"

                        # Save test in tests directory
                        test_directory = os.path.join(repo_path, "tests")
                        os.makedirs(test_directory, exist_ok=True)
                        test_file_path = os.path.join(test_directory, test_file_name)

                        with open(test_file_path, "w", encoding="utf-8") as file:
                            file.write(suggestions)

                        st.success(f"✅ Test file created at: `{os.path.abspath(test_file_path)}`")
                        st.info(f"🧪 Running tests for {test_file_name}...")
                        test_results = run_tests(test_file_path)

                        with open("test_update_log.txt", "a", encoding="utf-8") as log_file:
                            log_file.write(f"\n{'='*60}\n")
                            log_file.write(f"Test Generation Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            log_file.write(f"{'='*60}\n")
                            log_file.write(f"Original File: {f}\n")
                            log_file.write(f"Test File Created: {test_file_name}\n")
                            log_file.write(f"Test File Path: {test_file_path}\n")
                            log_file.write(f"\nCode Diff:\n{'-'*30}\n{diff}\n")
                            log_file.write(f"\nGenerated Test Cases:\n{'-'*30}\n{suggestions}\n")
                            log_file.write(f"\nTest Execution Results:\n{'-'*30}\n{test_results}\n")
                            log_file.write(f"{'='*60}\n")

                        st.success(f"✅ Test file '{test_file_name}' created and executed!")
                        st.subheader("🧪 Test Execution Results:")
                        st.code(test_results)

                        del st.session_state[f"suggestions_{f}"]
                    else:
                        st.error("⚠️ Invalid test cases generated. Please try again.")

            with col2:
                reject_btn_key = f"reject_{f}"
                if st.button(f"❌ Reject Suggestions", key=reject_btn_key):
                    del st.session_state[f"suggestions_{f}"]
                    st.info("Suggestions rejected.")

            with col3:
                regen_btn_key = f"regen_{f}"
                if st.button("🔁 Regenerate", key=regen_btn_key):
                    with st.spinner(f"Regenerating test suggestions for {f}..."):
                        new_suggestions = suggest_test_changes(f, diff)
                        st.session_state[f"suggestions_{f}"] = new_suggestions
                        st.rerun()

        st.divider()

# 3. Run All Tests (Optional)
st.subheader("🧪 Test Execution")
col1, col2 = st.columns(2)

with col1:
    if st.button("Run All Tests"):
        test_path = os.path.join(repo_path, "tests")
        if os.path.exists(test_path):
            result = run_tests(test_path)
            st.subheader("📊 All Test Results:")
            st.code(result)
        else:
            st.warning("No tests directory found.")

with col2:
    if st.button("View Test Log"):
        if os.path.exists("test_update_log.txt"):
            with open("test_update_log.txt", "r", encoding="utf-8") as log_file:
                log_content = log_file.read()
            st.subheader("📋 Test Update Log:")
            st.text_area("Log Content", log_content, height=400)
        else:
            st.info("No log file found yet.")
