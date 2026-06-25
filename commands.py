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
    if "take a screenshot" in clean_text or "capture screen" in clean_text or "screenshot" in clean_text:
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            filename = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
            filepath = os.path.join(desktop, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            os.startfile(filepath)
            return "Screenshot captured and saved to your Desktop, sir."
        except Exception as e:
            return f"Failed to take screenshot. Error: {e}"

    # 14. Voice Scratchpad / Notes
    if "write a note" in clean_text or "save a note" in clean_text:
        try:
            note_text = ""
            if "note" in clean_text:
                note_text = clean_text.split("note", 1)[1].strip()
            
            # Clean up leading prefix words
            if note_text.startswith("to "):
                note_text = note_text[3:]
            elif note_text.startswith("that "):
                note_text = note_text[5:]
                
            if not note_text:
                return "What note would you like me to write, sir?"
                
            notes_path = "notes.md"
            with open(notes_path, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                f.write(f"- [{timestamp}] {note_text.capitalize()}\n")
            return f"I've saved that to your notes, sir."
        except Exception as e:
            return f"Failed to save note. Error: {e}"

    if "read my notes" in clean_text or "read notes" in clean_text:
        try:
            notes_path = "notes.md"
            if os.path.exists(notes_path):
                with open(notes_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                if not lines:
                    return "Your notepad is currently empty, sir."
                last_notes = [line.strip().replace("- ", "") for line in lines[-3:]]
                notes_str = " Here are your last notes: " + " ... ".join(last_notes)
                return f"You have {len(lines)} notes saved.{notes_str}"
            else:
                return "You don't have any notes saved yet, sir."
        except Exception as e:
            return f"Failed to read notes. Error: {e}"

    # 15. Media Playback Controls
    # Virtual Key Codes
    VK_MEDIA_PLAY_PAUSE = 0xB3
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_MEDIA_STOP = 0xB2
    
    def press_media_key(vk_code):
        ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0) # Key Up

    if "play music" in clean_text or "resume music" in clean_text or "pause music" in clean_text or "pause" in clean_text:
        press_media_key(VK_MEDIA_PLAY_PAUSE)
        return "Media playback toggled, sir."
    if "next song" in clean_text or "next track" in clean_text or "skip song" in clean_text:
        press_media_key(VK_MEDIA_NEXT_TRACK)
        return "Playing next track."
    if "previous song" in clean_text or "previous track" in clean_text or "go back a song" in clean_text:
        press_media_key(VK_MEDIA_PREV_TRACK)
        return "Playing previous track."
    if "stop music" in clean_text or "stop playback" in clean_text:
        press_media_key(VK_MEDIA_STOP)
        return "Playback stopped, sir."

    # 16. System Volume Control
    if "volume" in clean_text or "mute" in clean_text or "unmute" in clean_text:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            
            if "unmute" in clean_text:
                volume.SetMute(0, None)
                return "Audio unmuted, sir."
            elif "mute" in clean_text:
                volume.SetMute(1, None)
                return "Audio muted, sir."
                
            # Check for specific percentage
            match = re.search(r"(\d+)\s*%", clean_text)
            if not match:
                match = re.search(r"volume\s*(?:to\s*)?(\d+)", clean_text)
                
            if match:
                val = int(match.group(1))
                val = max(0, min(100, val))
                volume.SetMasterVolumeLevelScalar(val / 100.0, None)
                return f"Volume set to {val} percent, sir."
                
            if "increase" in clean_text or "raise" in clean_text or "up" in clean_text:
                current_val = volume.GetMasterVolumeLevelScalar()
                new_val = min(1.0, current_val + 0.1)
                volume.SetMasterVolumeLevelScalar(new_val, None)
                return f"Volume increased to {int(new_val * 100)} percent, sir."
                
            if "decrease" in clean_text or "lower" in clean_text or "down" in clean_text:
                current_val = volume.GetMasterVolumeLevelScalar()
                new_val = max(0.0, current_val - 0.1)
                volume.SetMasterVolumeLevelScalar(new_val, None)
                return f"Volume decreased to {int(new_val * 100)} percent, sir."
        except Exception as e:
            return f"Failed to adjust volume. Error: {e}"

    # 17. Empty Recycle Bin
    if "empty recycle bin" in clean_text or "clean the trash" in clean_text or "empty trash" in clean_text:
        try:
            SHERB_NOCONFIRMATION = 0x00000001
            SHERB_NOPROGRESSUI = 0x00000002
            SHERB_NOSOUND = 0x00000004
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, SHERB_NOCONFIRMATION | SHERB_NOSOUND)
            return "Recycle bin emptied, sir."
        except Exception as e:
            return f"Failed to empty recycle bin. Error: {e}"

    # 18. Geo-Weather Reports
    if "weather" in clean_text:
        try:
            req = urllib.request.Request(
                "http://ip-api.com/json",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response:
                loc_data = json.loads(response.read().decode())
                lat = loc_data.get("lat", 0)
                lon = loc_data.get("lon", 0)
                city = loc_data.get("city", "your location")
                
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            with urllib.request.urlopen(weather_url) as w_response:
                w_data = json.loads(w_response.read().decode())
                temp = w_data["current_weather"]["temperature"]
                return f"In {city}, it is currently {temp} degrees Celsius."
        except Exception as e:
            return "I am currently unable to fetch the weather telemetry, sir."

    # 19. Active Window Controls
    if "close this window" in clean_text or "close window" in clean_text:
        try:
            VK_MENU = 0x12  # Alt
            VK_F4 = 0x73    # F4
            ctypes.windll.user32.keybd_event(VK_MENU, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_F4, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_F4, 0, 2, 0)
            ctypes.windll.user32.keybd_event(VK_MENU, 0, 2, 0)
            return "Closing active window."
        except Exception as e:
            return f"Failed to close window. Error: {e}"

    if "minimize window" in clean_text or "minimize this window" in clean_text:
        try:
            VK_LWIN = 0x5B  # Left Win key
            VK_DOWN = 0x28  # Down arrow
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_DOWN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_DOWN, 0, 2, 0)
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
            return "Minimizing active window."
        except Exception as e:
            return f"Failed to minimize window. Error: {e}"

    # 20. Power Estimator
    if "battery" in clean_text or "power percentage" in clean_text:
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                secs = battery.secsleft
                plugged = battery.power_plugged
                
                if plugged:
                   return f"Sir, the battery is at {percent} percent and charging."
                elif secs == psutil.POWER_TIME_UNLIMITED:
                   return f"Sir, the battery is at {percent} percent and plugged in."
                elif secs == psutil.POWER_TIME_UNKNOWN:
                   return f"Sir, the battery is at {percent} percent, time remaining is calculating."
                else:
                   hours = secs // 3600
                   mins = (secs % 3600) // 60
                   return f"Sir, the battery is at {percent} percent with {hours} hours and {mins} minutes remaining."
            else:
                return "No battery detected, sir. Ensure you are on a laptop."
        except Exception as e:
            return f"Failed to check battery. Error: {e}"

    # 21. Disk Space Analyzer
    if "check storage" in clean_text or "disk space" in clean_text or "hard drive space" in clean_text:
        try:
            obj = psutil.disk_usage('C:\\')
            free_gb = obj.free / (1024**3)
            total_gb = obj.total / (1024**3)
            return f"C: drive has {free_gb:.1f} gigabytes free out of {total_gb:.1f} gigabytes total, sir."
        except Exception as e:
            return f"Failed to check disk usage. Error: {e}"

    # 22. Clipboard Reader
    if "read my clipboard" in clean_text or "read clipboard" in clean_text:
        try:
            import pyperclip
            text_clip = pyperclip.paste().strip()
            if text_clip:
                if len(text_clip) > 150:
                    text_clip = text_clip[:150] + " ... and so on."
                return f"Your clipboard contains: {text_clip}"
            return "Your clipboard is currently empty, sir."
        except Exception as e:
            return f"Failed to read clipboard. Error: {e}"

    # 23. Voice Alarm / Timer
    if "timer for" in clean_text or "set a timer" in clean_text:
        try:
            match = re.search(r"(\d+)\s*(second|minute|hour)", clean_text)
            if match:
                duration = int(match.group(1))
                unit = match.group(2)
                secs = duration
                if "minute" in unit:
                    secs *= 60
                elif "hour" in unit:
                    secs *= 3600
                
                import threading
                from speaker import speak
                def run_timer(s, d, u):
                    import time
                    time.sleep(s)
                    speak(f"Alert! Your timer for {d} {u}s has expired, sir.")
                    
                threading.Thread(target=run_timer, args=(secs, duration, unit)).start()
                return f"Starting a timer for {duration} {unit}s."
        except Exception as e:
            return f"Failed to start timer. Error: {e}"

    # 24. NATO Spelling Aid
    if "spell" in clean_text:
        try:
            match = re.search(r"spell\s+(\w+)", clean_text)
            if match:
                word = match.group(1).upper()
                nato = {
                    'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
                    'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
                    'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
                    'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
                    'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee', 'Z': 'Zulu'
                }
                spelling = [nato.get(char, char) for char in word]
                return f"{word} is spelled: " + ", ".join(spelling)
        except Exception as e:
            return f"Failed spelling operation. Error: {e}"

    # 25. Dice Roller / Coin Flipper
    if "flip a coin" in clean_text or "toss a coin" in clean_text:
        return f"It is {random.choice(['Heads', 'Tails'])}, sir."
    if "roll a dice" in clean_text or "roll a die" in clean_text:
        return f"It is a {random.randint(1, 6)}, sir."

    # 26. Math Solver
    if "calculate" in clean_text or "what is" in clean_text:
        try:
            expr = clean_text.replace("times", "*").replace("divided by", "/").replace("plus", "+").replace("minus", "-")
            match = re.search(r"([\d\s\+\-\*\/\(\)\.]+)", expr)
            if match:
                math_expr = match.group(1).strip()
                if re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", math_expr):
                    res = eval(math_expr)
                    return f"The answer is {res}."
        except Exception as e:
            pass

    # 27. IP Address Lookup
    if "my ip address" in clean_text or "what's my ip" in clean_text or "ip configuration" in clean_text:
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            try:
                req_ip = urllib.request.Request("https://api.ipify.org", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_ip) as r:
                    public_ip = r.read().decode().strip()
            except:
                public_ip = "unknown"
            return f"Your local IP is {local_ip}, and your public IP is {public_ip}."
        except Exception as e:
            return f"Failed to retrieve network config. Error: {e}"

    # 28. News Reader
    if "read today's headlines" in clean_text or "news headlines" in clean_text or "current news" in clean_text:
        try:
            req_news = urllib.request.Request("https://feeds.bbci.co.uk/news/world/rss.xml", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_news) as r:
                xml = r.read().decode('utf-8')
            titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", xml)
            if not titles:
                titles = re.findall(r"<title>(.*?)</title>", xml)
            headlines = [t for t in titles[1:4]]
            return "Here are the top world headlines: " + ". ... ".join(headlines)
        except Exception as e:
            return "I am currently unable to fetch the news telemetry, sir."

    # 29. Wikipedia Summary
    if "wikipedia" in clean_text:
        try:
            match = re.search(r"wikipedia\s+(?:for\s+)?(.*)", clean_text)
            if match:
                topic = match.group(1).strip()
                wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(topic)}"
                req_wiki = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_wiki) as r:
                    w_data = json.loads(r.read().decode())
                summary = w_data.get("extract", "No summary found.")
                if len(summary) > 250:
                    summary = summary[:250] + "..."
                return f"According to Wikipedia: {summary}"
        except Exception as e:
            return "I couldn't fetch details from Wikipedia at this time, sir."

    # 30. Joke Teller
    if "tell me a joke" in clean_text or "joke" in clean_text:
        jokes = [
            "Why do programmers wear glasses? Because they can't C sharp.",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "A SQL query goes into a bar, walks up to two tables and asks: Can I join you?",
            "Why did the programmer quit his job? Because he didn't get arrays."
        ]
        return random.choice(jokes)

    # 31. Reminders Core
    if "remind me in" in clean_text or "set a reminder" in clean_text:
        try:
            match = re.search(r"remind me in (\d+)\s*(second|minute|hour)\s+to\s+(.*)", clean_text)
            if match:
                dur = int(match.group(1))
                unit = match.group(2)
                task = match.group(3)
                secs = dur
                if "minute" in unit:
                    secs *= 60
                elif "hour" in unit:
                    secs *= 3600
                
                import threading
                from speaker import speak
                def run_reminder(s, t):
                    import time
                    time.sleep(s)
                    speak(f"Sir, this is your reminder to {t}.")
                    
                threading.Thread(target=run_reminder, args=(secs, task)).start()
                return f"I will remind you to {task} in {dur} {unit}s, sir."
        except Exception as e:
            return f"Failed to set reminder. Error: {e}"

    # 32. Git Helpers
    if "git status" in clean_text:
        try:
            res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
            lines = res.stdout.strip().split("\n")
            modified = len([l for l in lines if l])
            if modified == 0:
                return "Your git branch is clean, sir."
            return f"You have {modified} untracked or modified files in your branch, sir."
        except Exception as e:
            return f"Failed to run git status. Error: {e}"

    if "git commit" in clean_text or "commit my changes" in clean_text or "git check in" in clean_text:
        try:
            subprocess.run(["git", "add", "."], check=True)
            msg = f"Automated commit via Jarvis on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", msg], check=True)
            return f"Staged all files and committed with message: {msg}."
        except Exception as e:
            return f"Failed to commit. Error: {e}"

    # 33. Port & Process Manager
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

    # 34. Docker Container Status
    if "check docker" in clean_text or "docker status" in clean_text:
        try:
            res = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, check=True)
            containers = [c.strip() for c in res.stdout.strip().split("\n") if c.strip()]
            if not containers:
                return "No active docker containers are running, sir."
            return f"The running docker containers are: {', '.join(containers)}."
        except Exception as e:
            return "Failed to query Docker. Ensure Docker Desktop is running."

    # 35. Clipboard Developer Tools
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

    # 36. Codebase Search
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

    # 37. Boilerplate Creator
    if "create fastapi" in clean_text or "fastapi boilerplate" in clean_text:
        try:
            code = """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
"""
            with open("main.py", "w", encoding="utf-8") as f:
                f.write(code)
            return "FastAPI boilerplate created in main.py, sir."
        except Exception as e:
            return f"Failed to write file. Error: {e}"

    # 38. Local Code Reviewer
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
            from brain import ask_ai
            review = ask_ai(prompt)
            with open("code_review.md", "w", encoding="utf-8") as f:
                f.write(f"# Code Review - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{review}\n")
            return "I've reviewed your git diff and written the report to code_review.md, sir."
        except Exception as e:
            return f"Failed to perform code review. Error: {e}"

    # 39. Automated Unit Test Generator
    if "write a unit test" in clean_text or "write a test for" in clean_text or "generate test" in clean_text:
        try:
            match = re.search(r"for\s+([\w\.-]+)", clean_text)
            if not match:
                return "Please specify the file name to generate tests for, sir."
            filename = match.group(1)
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
            from brain import ask_ai
            test_code = ask_ai(prompt)
            test_code = test_code.replace("```python", "").replace("```", "").strip()
            test_filename = f"test_{filename}"
            with open(test_filename, "w", encoding="utf-8") as f:
                f.write(test_code)
            return f"Unit test suite generated and saved as {test_filename}, sir."
        except Exception as e:
            return f"Failed to generate tests. Error: {e}"

    # 40. Downloads Folder Organizer
    if "organize my downloads" in clean_text or "organize downloads" in clean_text:
        try:
            downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads):
                return "Downloads directory not found, sir."
            categories = {
                "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".txt", ".csv", ".pptx", ".ppt"],
                "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".ico"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "Installers": [".exe", ".msi"],
                "Audio": [".mp3", ".wav", ".flac", ".m4a"],
                "Video": [".mp4", ".mkv", ".avi", ".mov"]
            }
            moved_count = 0
            for item in os.listdir(downloads):
                item_path = os.path.join(downloads, item)
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    dest_dir = "Others"
                    for category, extensions in categories.items():
                        if ext in extensions:
                            dest_dir = category
                            break
                    target_folder = os.path.join(downloads, dest_dir)
                    os.makedirs(target_folder, exist_ok=True)
                    os.rename(item_path, os.path.join(target_folder, item))
                    moved_count += 1
            return f"I've successfully organized {moved_count} files in your downloads folder, sir."
        except Exception as e:
            return f"Failed to organize downloads. Error: {e}"

    # 41. Development Time Tracker
    if "start tracking" in clean_text:
        try:
            task = "Coding Session"
            if "tracking" in clean_text:
                parts = clean_text.split("tracking", 1)
                if len(parts) > 1 and parts[1].strip():
                    task = parts[1].replace(":", "").strip()
            with open("time_tracker.json", "w", encoding="utf-8") as f:
                json.dump({"task": task, "start_time": time.time()}, f)
            return f"I've started tracking time for {task}, sir."
        except Exception as e:
            return f"Failed to start time tracker. Error: {e}"

    if "stop tracking" in clean_text:
        try:
            tracker_path = "time_tracker.json"
            if os.path.exists(tracker_path):
                with open(tracker_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                task = data.get("task", "Coding Session")
                start_time = data.get("start_time", time.time())
                elapsed = time.time() - start_time
                os.remove(tracker_path)
                hours = int(elapsed // 3600)
                mins = int((elapsed % 3600) // 60)
                with open("timesheet.csv", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{task},{hours}h {mins}m\n")
                return f"Tracking stopped for {task}. Total time elapsed: {hours} hours and {mins} minutes."
            else:
                return "No active time tracking session found, sir."
        except Exception as e:
            return f"Failed to stop tracker. Error: {e}"

    # 42. Focus / Meeting Mode
    if "meeting mode" in clean_text or "focus mode" in clean_text:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            VK_LWIN = 0x5B
            VK_M = 0x4D
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_M, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_M, 0, 2, 0)
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
            return "Meeting mode activated. Master audio muted and windows minimized, sir."
        except Exception as e:
            return f"Failed to activate meeting mode. Error: {e}"

