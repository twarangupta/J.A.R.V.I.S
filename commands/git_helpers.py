import subprocess
from datetime import datetime

def execute_git_command(clean_text: str) -> str | None:
    # Git status
    if "git status" in clean_text or "get status" in clean_text:
        try:
            res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
            lines = res.stdout.strip().split("\n")
            modified = len([l for l in lines if l])
            if modified == 0:
                return "Your git branch is clean, sir."
            return f"You have {modified} untracked or modified files in your branch, sir."
        except Exception as e:
            return f"Failed to run git status. Error: {e}"

    # Git commit
    if "git commit" in clean_text or "get commit" in clean_text or "commit my changes" in clean_text or "git check in" in clean_text or "get check in" in clean_text:
        try:
            # Check for a custom commit message in the command text
            msg = None
            for marker in ["-m ", "--message ", "with message ", "message ", "saying "]:
                if marker in clean_text:
                    parts = clean_text.split(marker, 1)
                    extracted = parts[1].strip().strip('"\'')
                    if extracted:
                        msg = extracted
                        break
            if not msg:
                msg = f"Automated commit via Jarvis on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", msg], check=True)
            return f"Staged all files and committed with message: {msg}."
        except Exception as e:
            return f"Failed to commit. Error: {e}"

    # Git push
    if "git push" in clean_text or "get push" in clean_text or "push changes" in clean_text or "push my changes" in clean_text:
        try:
            res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
            branch = res.stdout.strip()
            if not branch:
                return "I couldn't identify the current active branch, sir."
            subprocess.run(["git", "push", "origin", branch], check=True)
            return f"Successfully pushed changes on branch {branch} to origin, sir."
        except Exception as e:
            return f"Failed to push changes. Error: {e}"

    # Git pull
    if "git pull" in clean_text or "get pull" in clean_text or "pull changes" in clean_text or "pull from remote" in clean_text:
        try:
            res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
            branch = res.stdout.strip()
            if not branch:
                return "I couldn't identify the current active branch, sir."
            subprocess.run(["git", "pull", "origin", branch], check=True)
            return f"Successfully pulled latest changes on branch {branch} from remote repository, sir."
        except Exception as e:
            return f"Failed to pull changes. Error: {e}"

    # Git stash pop
    if "git stash pop" in clean_text or "get stash pop" in clean_text or "pop stash" in clean_text or "apply stash" in clean_text:
        try:
            subprocess.run(["git", "stash", "pop"], check=True)
            return "Successfully popped the top stash from the stack, sir."
        except Exception as e:
            return f"Failed to pop stash. Error: {e}"

    # Git stash
    if "git stash" in clean_text or "get stash" in clean_text or "stash changes" in clean_text or "stash my changes" in clean_text:
        try:
            subprocess.run(["git", "stash"], check=True)
            return "Successfully stashed local modifications, sir."
        except Exception as e:
            return f"Failed to stash changes. Error: {e}"

    # Git conflicts
    if "git conflict" in clean_text or "get conflict" in clean_text or "merge conflict" in clean_text or "any conflict" in clean_text or "check conflict" in clean_text:
        try:
            res = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"], capture_output=True, text=True, check=True)
            files = [f.strip() for f in res.stdout.strip().split("\n") if f.strip()]
            if not files:
                return "No active merge conflicts detected in your repository, sir."
            return f"Sir, I detected merge conflicts in the following files: {', '.join(files)}."
        except Exception as e:
            return f"Failed to check for merge conflicts. Error: {e}"

    # Git log
    if "git log" in clean_text or "get log" in clean_text or "show commits" in clean_text or "git history" in clean_text:
        try:
            res = subprocess.run(["git", "log", "-n", "5", "--oneline"], capture_output=True, text=True, check=True)
            lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
            if not lines:
                return "No commit history found, sir."
            history = " ... ".join(lines)
            return f"Here are the last 5 commits, sir: {history}"
        except Exception as e:
            return f"Failed to retrieve git log. Error: {e}"

    # Create new branch
    if "create branch" in clean_text or "create a branch" in clean_text or "make branch" in clean_text or "new branch" in clean_text:
        try:
            target_branch = None
            if "create branch" in clean_text:
                target_branch = clean_text.split("create branch", 1)[1].strip()
            elif "create a branch" in clean_text:
                target_branch = clean_text.split("create a branch", 1)[1].strip()
            elif "make branch" in clean_text:
                target_branch = clean_text.split("make branch", 1)[1].strip()
            elif "new branch" in clean_text:
                target_branch = clean_text.split("new branch", 1)[1].strip()
                
            if target_branch:
                target_branch = target_branch.rstrip(".?,!").replace(" ", "-")
                subprocess.run(["git", "checkout", "-b", target_branch], check=True)
                return f"Successfully created and switched to new branch {target_branch}, sir."
            else:
                return "Please specify the name of the new branch to create, sir."
        except Exception as e:
            return f"Failed to create branch. Error: {e}"

    # Switch/checkout branch
    if "switch branch to" in clean_text or "checkout branch" in clean_text or "switch branch" in clean_text:
        try:
            target_branch = None
            if "switch branch to" in clean_text:
                target_branch = clean_text.split("switch branch to", 1)[1].strip()
            elif "checkout branch" in clean_text:
                target_branch = clean_text.split("checkout branch", 1)[1].strip()
            elif "switch branch" in clean_text:
                target_branch = clean_text.split("switch branch", 1)[1].strip()
                
            if target_branch:
                target_branch = target_branch.rstrip(".?,!")
                subprocess.run(["git", "checkout", target_branch], check=True)
                return f"Successfully switched to branch {target_branch}, sir."
            else:
                return "Please specify which branch you want to switch to, sir."
        except Exception as e:
            return f"Failed to switch branch. Error: {e}"

    # List local branches
    if "git branch" in clean_text or "get branch" in clean_text or "show branches" in clean_text or "list branches" in clean_text:
        try:
            res = subprocess.run(["git", "branch"], capture_output=True, text=True, check=True)
            branches = [b.strip() for b in res.stdout.strip().split("\n") if b.strip()]
            if not branches:
                return "No branches found, sir."
            current = [b.replace("*", "").strip() for b in branches if b.startswith("*")]
            other_branches = [b.strip() for b in branches if not b.startswith("*")]
            current_str = f"You are currently on branch {current[0]}." if current else ""
            if other_branches:
                other_str = f" Other branches are: {', '.join(other_branches)}."
            else:
                other_str = " There are no other local branches."
            return f"{current_str}{other_str}"
        except Exception as e:
            return f"Failed to retrieve branches. Error: {e}"

    return None
