import os
import subprocess
from datetime import datetime
import re
import ctypes
import psutil
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import urllib.request
import urllib.parse
import json
import random
import socket
import time

def execute_command(text: str) -> str | None:
    """
    Checks if the transcribed text matches any system command.
    If so, executes it and returns a response string.
    If not, returns None, indicating the request should go to the LLM brain.
    """
    clean_text = text.strip().lower()

    is_open_request = "open" in clean_text or "launch" in clean_text or "start" in clean_text

    # Google Search Command
    query = None
    if clean_text.startswith("search for ") or clean_text.startswith("google for "):
        query = clean_text.split("for", 1)[1].strip()
    elif clean_text.startswith("search ") or clean_text.startswith("google "):
        parts = clean_text.split(" ", 1)
        if len(parts) > 1:
            query = parts[1].strip()
            
    if query:
        try:
            import urllib.parse
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            opened = False
            for path in chrome_paths:
                if os.path.exists(path):
                    subprocess.Popen([path, url])
                    opened = True
                    break
            if not opened:
                import webbrowser
                webbrowser.open(url)
            return f"Searching Google for {query}."
        except Exception as e:
            return f"Failed to search. Error: {e}"

    # 1. Open Chrome / Websites
    if is_open_request and ("chrome" in clean_text or "gmail" in clean_text or "youtube" in clean_text or "google" in clean_text or "github" in clean_text or "reddit" in clean_text or "stackoverflow" in clean_text):
        try:
            # Map keywords to URLs
            urls = {
                "gmail": "https://gmail.com",
                "youtube": "https://youtube.com",
                "google": "https://google.com",
                "github": "https://github.com",
                "reddit": "https://reddit.com",
                "stackoverflow": "https://stackoverflow.com"
            }
            
            target_url = None
            site_name = "Google Chrome"
            for site, url in urls.items():
                if site in clean_text:
                    target_url = url
                    site_name = site.capitalize()
                    break

            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            opened = False
            for path in chrome_paths:
                if os.path.exists(path):
                    if target_url:
                        subprocess.Popen([path, target_url])
                    else:
                        os.startfile(path)
                    opened = True
                    break
            
            if not opened:
                import webbrowser
                webbrowser.open(target_url if target_url else "https://www.google.com")
                
            return f"Opening {site_name}."
        except Exception as e:
            return f"Failed to open {site_name}. Error: {e}"

    # 2. Open VS Code
    if is_open_request and ("vs code" in clean_text or "vscode" in clean_text or "visual studio code" in clean_text):
        try:
            subprocess.Popen("code", shell=True)
            return "Opening Visual Studio Code."
        except Exception as e:
            return f"Failed to open VS Code. Error: {e}"

    # 3. Open Spotify
    if is_open_request and "spotify" in clean_text:
        try:
            # Using the Spotify protocol handler to start the app
            subprocess.Popen("start spotify:", shell=True)
            return "Opening Spotify."
        except Exception as e:
            return f"Failed to open Spotify. Error: {e}"

    # 4. Open Calculator
    if is_open_request and ("calculator" in clean_text or "calc" in clean_text):
        try:
            subprocess.Popen("calc")
            return "Opening Calculator."
        except Exception as e:
            return f"Failed to open Calculator. Error: {e}"

    # 5. Open Notepad
    if is_open_request and "notepad" in clean_text:
        try:
            subprocess.Popen("notepad")
            return "Opening Notepad."
        except Exception as e:
            return f"Failed to open Notepad. Error: {e}"

    # 6. Tell me the time
    if "tell me the time" in clean_text or "what time is it" in clean_text or "current time" in clean_text or "what is the time" in clean_text:
        return datetime.now().strftime("The current time is %I:%M %p.")

    # 7. Tell me the date
    if "tell me the date" in clean_text or "what's the date" in clean_text or "current date" in clean_text or "what is the date" in clean_text:
        return datetime.now().strftime("Today is %B %d, %Y.")

    # 8. Shutdown PC
    if "shutdown" in clean_text or "shut down my computer" in clean_text:
        # Schedule shutdown in 5 seconds
        os.system("shutdown /s /t 5")
        return "Shutting down the system in 5 seconds. Goodbye."

    # 9. Restart PC
    if "restart" in clean_text or "restart my computer" in clean_text:
        # Schedule restart in 5 seconds
        os.system("shutdown /r /t 5")
        return "Restarting the system in 5 seconds."

    # 10. Lock PC
    if "lock pc" in clean_text or "lock computer" in clean_text or "lock the pc" in clean_text:
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Locking the workstation."
        except Exception as e:
            return f"Failed to lock the workstation. Error: {e}"

    # 11. Open Docker Desktop
    if is_open_request and ("docker desktop" in clean_text or "docker" in clean_text):
        standard_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
        try:
            if os.path.exists(standard_path):
                subprocess.Popen([standard_path])
            else:
                # Fallback to run directly from PATH
                subprocess.Popen("Docker Desktop.exe", shell=True)
            return "Opening Docker Desktop."
        except Exception as e:
            return f"Failed to open Docker Desktop. Error: {e}"

    # 12. System Telemetry & Status Report
    if "status report" in clean_text or "system status" in clean_text or "telemetry" in clean_text:
        try:
            cpu_usage = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()
            mem_usage = memory_info.percent
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                charging = battery.power_plugged
                plugged_status = "and charging" if charging else "and discharging"
                battery_str = f", and your battery is at {percent} percent {plugged_status}"
            else:
                battery_str = ""
            return f"Sir, CPU load is at {cpu_usage} percent, memory utilization is at {mem_usage} percent{battery_str}."
        except Exception as e:
            return f"Failed to retrieve system status. Error: {e}"

    # 13. Instant Screenshot Capture
