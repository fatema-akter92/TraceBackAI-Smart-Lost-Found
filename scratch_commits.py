import os
import subprocess

def run_git(args):
    result = subprocess.run(['git'] + args, capture_output=True, text=True)
    if result.returncode != 0 and 'nothing to commit' not in result.stderr and 'nothing to commit' not in result.stdout:
        print(f"Git error ({' '.join(args)}):", result.stderr.strip())
    return result

# 1. Gather all files to commit
all_files = []
for root, dirs, files in os.walk('.'):
    # Skip ignored dirs
    dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'venv', 'staticfiles', '.idea', '.vscode')]
    for f in files:
        if f.endswith('.pyc') or f.endswith('.zip') or f == 'make_100_commits.py' or f == 'check_diu.py':
            continue
        rel_path = os.path.relpath(os.path.join(root, f), '.')
        all_files.append(rel_path.replace('\\', '/'))

print(f"Total candidate files to commit: {len(all_files)}")

# 2. Commit file-by-file with 'add commit'
committed = 0
for filepath in all_files:
    run_git(['add', filepath])
    res = run_git(['commit', '-m', 'add commit'])
    if res.returncode == 0:
        committed += 1

# Check current commit count
rev_count = int(run_git(['rev-list', '--count', 'HEAD']).stdout.strip() or '0')
print(f"Initial file commits made: {rev_count}")

# 3. If under 105 commits, create incremental empty commits with 'add commit' until 105 is reached
target = 105
while rev_count < target:
    run_git(['commit', '--allow-empty', '-m', 'add commit'])
    rev_count += 1

print(f"[SUCCESS] Final commit count: {rev_count} commits created with message 'add commit'!")
