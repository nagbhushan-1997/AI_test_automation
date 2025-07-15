# from git import Repo
# import os

# def get_changed_files(repo_path):
#     repo = Repo(repo_path)
#     return [item.a_path for item in repo.index.diff(None)] + repo.untracked_files

# def get_file_diff(repo_path, filename):
#     repo = Repo(repo_path)
#     # Check if file is untracked
#     if filename in repo.untracked_files:
#         with open(os.path.join(repo_path, filename), 'r', encoding='utf-8') as f:
#             content = f.read()
#         return f"# Untracked file - showing full content\n{content}"
#     else:
#         # Safe way to pass filename
#         return repo.git.diff('--', filename)

from git import Repo
import os

def get_changed_files(repo_path):
    repo = Repo(repo_path)
    
    # Get both staged and untracked files
    changed_files = [item.a_path for item in repo.index.diff(None)] + repo.untracked_files

    # Filter: Only .py files directly inside the tests/ folder, starting with test_
    filtered_files = [
        f for f in changed_files
        if f.startswith("vue_front_end_code/login-widget/src/")
        and f.count("/") == 1  # Ensures it's directly under tests/, not nested like tests/unit/test_abc.py
        
        and f.endswith(".vue")
    ]

    return filtered_files

def get_file_diff(repo_path, filename):
    repo = Repo(repo_path)
    
    if filename in repo.untracked_files:
        with open(os.path.join(repo_path, filename), 'r', encoding='utf-8') as f:
            content = f.read()
        return f"# Untracked file - showing full content\n{content}"
    else:
        return repo.git.diff('--', filename)
