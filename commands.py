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
