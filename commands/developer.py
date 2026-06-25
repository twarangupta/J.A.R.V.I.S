import os
import subprocess
import re
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

# Helper to query the local LLM (imported inline to avoid circular dependencies)
def ask_local_ai(prompt: str) -> str:
    try:
        from brain import ask_ai
        return ask_ai(prompt)
    except Exception as e:
        return f"Error querying local AI: {e}"

def execute_developer_command(clean_text: str) -> str | None:
    # 1. New: Log Analyzer / Debugger
    if "debug this crash" in clean_text or "debug crash" in clean_text or "analyze this stack trace" in clean_text or "analyze stack trace" in clean_text or "debug error" in clean_text or "analyze error" in clean_text:
        try:
            import pyperclip
            trace = pyperclip.paste().strip()
            if not trace:
                return "Your clipboard is empty, sir. Please copy the error stack trace first."
            
            prompt = (
                "You are an expert debugger. Analyze this error/stack trace and provide a concise summary of "
                "what went wrong and the exact code changes needed to fix it. Keep it under 200 words:\n\n"
                f"{trace}"
            )
            report = ask_local_ai(prompt)
            # Save the full report to a file
            with open("debug_report.md", "w", encoding="utf-8") as f:
                f.write(f"# Debug Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{report}\n")
            pyperclip.copy(report)
            return "I've analyzed the stack trace. The report has been saved to debug_report.md and copied to your clipboard, sir."
        except Exception as e:
            return f"Failed to analyze error. Error: {e}"

    # 2. New: Dependency Health Checker
    if "audit my dependencies" in clean_text or "check dependencies" in clean_text or "audit dependencies" in clean_text:
        try:
            reports = []
            if os.path.exists("requirements.txt"):
                res = subprocess.run(["pip", "list", "--outdated", "--format=json"], capture_output=True, text=True)
                if res.returncode == 0 and res.stdout.strip():
                    try:
                        pkgs = json.loads(res.stdout)
                        if pkgs:
                            reports.append(f"{len(pkgs)} outdated Python packages found.")
                    except:
                        reports.append("Python dependencies have outdated packages.")
            if os.path.exists("package.json"):
                res = subprocess.run(["npm", "outdated"], shell=True, capture_output=True, text=True)
                if res.stdout.strip():
                    reports.append("Outdated Node.js packages detected.")
            
            if not reports:
                return "All your project dependencies appear to be up to date, sir."
            return "Sir, " + " and ".join(reports)
        except Exception as e:
            return f"Failed to check dependencies. Error: {e}"

    # 3. New: API Sandbox
    if "send a get request to" in clean_text or "send a post request to" in clean_text or "send request to" in clean_text:
        try:
            import pyperclip
            # Extract URL
            method = "GET"
            if "post request" in clean_text:
                method = "POST"
            
            url_part = clean_text.split("to", 1)[1].strip()
            # Clean up speech artifacts
            url_part = url_part.replace("slash", "/").replace("colon", ":").replace(" ", "").rstrip(".?,!")
            if not url_part.startswith("http"):
                url_part = "http://" + url_part

            req = urllib.request.Request(url_part, method=method)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            if method == "POST":
                # Check if clipboard has data to post, otherwise send empty dict
                post_data = pyperclip.paste().strip()
                try:
                    json.loads(post_data)
                    data_bytes = post_data.encode('utf-8')
                    req.add_header('Content-Type', 'application/json')
                except:
                    data_bytes = b"{}"
                    req.add_header('Content-Type', 'application/json')
                req.data = data_bytes

            with urllib.request.urlopen(req, timeout=5) as response:
                body = response.read().decode('utf-8')
                headers = dict(response.headers)
            
            result_str = f"Status: {response.status}\nHeaders:\n{json.dumps(headers, indent=2)}\n\nBody:\n{body}"
            pyperclip.copy(result_str)
            return f"API response received with status code {response.status} and copied to clipboard, sir."
        except Exception as e:
            return f"API request failed. Error: {e}"

    # 4. New: Semantic Code Explainer
    if "explain code file" in clean_text or "explain file" in clean_text or "explain code" in clean_text:
        try:
            match = re.search(r"(?:file|code)\s+([\w\.-]+)", clean_text)
            if not match:
                return "Please specify the name of the file you want me to explain, sir."
            filename = match.group(1).rstrip(".?,!")
            if not os.path.exists(filename):
                return f"File {filename} does not exist in the current directory."
            
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                code_content = f.read()
            
            if len(code_content) > 4000:
                code_content = code_content[:4000] + "\n... [truncated]"
                
            prompt = (
                "Explain the primary architecture, design patterns, and logic of this code file concisely "
                "in a few sentences. Highlight the main components and how they interact:\n\n"
                f"File: {filename}\n{code_content}"
            )
            explanation = ask_local_ai(prompt)
            return f"According to my analysis of {filename}: {explanation}"
        except Exception as e:
            return f"Failed to analyze the code file. Error: {e}"

    # 5. New: Container Logs Monitor
    if "check container logs" in clean_text or "container logs" in clean_text:
        try:
            import pyperclip
            parts = clean_text.split("logs")
            container_name = ""
            if len(parts) > 1:
                container_name = parts[1].replace("for", "").strip().rstrip(".?,!")
            
            if not container_name:
                return "Which docker container name should I fetch the logs for, sir?"
            
            res = subprocess.run(["docker", "logs", "--tail", "20", container_name], capture_output=True, text=True)
            output = res.stdout + res.stderr
            if not output.strip():
                return f"No logs found or container {container_name} is offline, sir."
            
            pyperclip.copy(output)
            return f"I've fetched the last 20 log entries for container {container_name} and copied them to your clipboard."
        except Exception as e:
            return f"Failed to get container logs. Error: {e}"

    # Port & Process Manager
    if "kill port" in clean_text or "what is on port" in clean_text or "check port" in clean_text or "what's on port" in clean_text:
        try:
            match = re.search(r"port\s+(\d+)", clean_text)
            if match:
                port = match.group(1)
                res = subprocess.run(f"netstat -ano | findstr :{port}", shell=True, capture_output=True, text=True)
                lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
                if not lines:
                    return f"No process is running on port {port}, sir."
                    
                pid = lines[0].split()[-1]
                if "kill" in clean_text:
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, check=True)
                    return f"Successfully terminated process with P.I.D. {pid} on port {port}."
                else:
                    return f"Process with P.I.D. {pid} is listening on port {port}, sir."
        except Exception as e:
            return f"Failed to operate on port. Error: {e}"

    # Docker Container Status
    if "check docker" in clean_text or "docker status" in clean_text:
        try:
            res = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, check=True)
            containers = [c.strip() for c in res.stdout.strip().split("\n") if c.strip()]
            if not containers:
                return "No active docker containers are running, sir."
            return f"The running docker containers are: {', '.join(containers)}."
        except Exception as e:
            return "Failed to query Docker. Ensure Docker Desktop is running."

    # Clipboard JSON Formatter
    if "format json" in clean_text or "prettify json" in clean_text or "pretty print json" in clean_text:
        try:
            import pyperclip
            raw = pyperclip.paste().strip()
            parsed = json.loads(raw)
            pretty = json.dumps(parsed, indent=4)
            pyperclip.copy(pretty)
            return "JSON formatted and copied back to clipboard, sir."
        except Exception as e:
            return f"Failed to parse clipboard as JSON. Error: {e}"

    # Codebase Search
    if "search codebase for" in clean_text or "search code for" in clean_text:
        try:
            term = clean_text.split("for", 1)[1].strip()
            matches = []
            for root, dirs, files in os.walk("."):
                if "venv" in root or ".venv" in root or ".git" in root or "__pycache__" in root:
                     continue
                for file in files:
                    if file.endswith((".py", ".txt", ".json", ".md", ".sh", ".ps1")):
                        path = os.path.join(root, file)
                        try:
                            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                                for i, line in enumerate(f, 1):
                                     if term in line.lower():
                                         matches.append(f"{file} line {i}")
                                         if len(matches) >= 3:
                                             break
                        except:
                            pass
                if len(matches) >= 3:
                     break
            if not matches:
                return f"No matches found for {term} in your codebase."
            return f"Found matches in: {', '.join(matches[:3])}."
        except Exception as e:
            return f"Failed search. Error: {e}"

    # Boilerplate Creator
    if "create fastapi" in clean_text or "fastapi boilerplate" in clean_text:
        try:
            import pyperclip
            import pyautogui
            pyautogui.FAILSAFE = False
            code = """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
"""
            pyperclip.copy(code)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            return "Pasted the FastAPI boilerplate directly at your cursor, sir."
        except Exception as e:
            return f"Failed to paste FastAPI boilerplate. Error: {e}"

    if "create boilerplate for" in clean_text or "create a boilerplate for" in clean_text or "boilerplate for" in clean_text:
        try:
            import pyperclip
            import pyautogui
            pyautogui.FAILSAFE = False
            
            # Extract the technology/context
            tech = "code template"
            if "create a boilerplate for" in clean_text:
                tech = clean_text.split("create a boilerplate for", 1)[1].strip()
            elif "create boilerplate for" in clean_text:
                tech = clean_text.split("create boilerplate for", 1)[1].strip()
            elif "boilerplate for" in clean_text:
                tech = clean_text.split("boilerplate for", 1)[1].strip()
                
            tech = tech.rstrip(".?,!")
            
            prompt = (
                f"Write a standard, clean, minimal boilerplate template code snippet for: '{tech}'. "
                "Output ONLY raw code. Do NOT output markdown ticks (like ```), explanations, comments, or headers. "
                "Only output the raw code itself."
            )
            raw_code = ask_local_ai(prompt)
            # Remove any residual markdown backticks the LLM might have returned
            raw_code = raw_code.replace("```python", "").replace("```html", "").replace("```javascript", "").replace("```", "").strip()
            
            pyperclip.copy(raw_code)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            return f"Pasted the {tech} boilerplate directly at your cursor, sir."
        except Exception as e:
            return f"Failed to generate boilerplate. Error: {e}"

    # Local Code Reviewer
    if "review my code" in clean_text or "code review" in clean_text:
        try:
            res = subprocess.run(["git", "diff"], capture_output=True, text=True, check=True)
            diff = res.stdout.strip()
            if not diff:
                return "No changes detected in git, sir."
            if len(diff) > 4000:
                diff = diff[:4000] + "\n... [Diff truncated due to size]"
            prompt = (
                "You are a Senior Code Reviewer. Review the following git diff. "
                "Find potential bugs, style issues, and performance bottlenecks. "
                "Provide constructive feedback. Keep it brief.\n\n"
                f"Git Diff:\n{diff}"
            )
            review = ask_local_ai(prompt)
            with open("code_review.md", "w", encoding="utf-8") as f:
                f.write(f"# Code Review - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{review}\n")
            return "I've reviewed your git diff and written the report to code_review.md, sir."
        except Exception as e:
            return f"Failed to perform code review. Error: {e}"

    # Automated Unit Test Generator
    if "write a unit test" in clean_text or "write a test for" in clean_text or "generate test" in clean_text:
        try:
            match = re.search(r"for\s+([\w\.-]+)", clean_text)
            if not match:
                return "Please specify the file name to generate tests for, sir."
            filename = match.group(1).rstrip(".?,!")
            if not os.path.exists(filename):
                return f"File {filename} does not exist in the current directory."
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                code_content = f.read()
            if len(code_content) > 4000:
                code_content = code_content[:4000]
            prompt = (
                f"Write a comprehensive unit test suite using unittest or pytest for this Python code. "
                f"Only output valid Python code, no markdown formatting blocks.\n\n"
                f"Code:\n{code_content}"
            )
            test_code = ask_local_ai(prompt)
            test_code = test_code.replace("```python", "").replace("```", "").strip()
            test_filename = f"test_{filename}"
            with open(test_filename, "w", encoding="utf-8") as f:
                f.write(test_code)
            return f"Unit test suite generated and saved as {test_filename}, sir."
        except Exception as e:
            return f"Failed to generate tests. Error: {e}"

    # Project Workspace Launcher
    if "start project" in clean_text or "launch project" in clean_text:
        try:
            proj_name = "Jarvis"
            if "project" in clean_text:
                proj_name = clean_text.split("project", 1)[1].strip()
            subprocess.Popen("code .", shell=True)
            import webbrowser
            webbrowser.open("https://github.com")
            return f"Project workspace launched for {proj_name}, sir."
        except Exception as e:
            return f"Failed to launch workspace. Error: {e}"

    return None
