import os
import re
import json
import time
import random
import urllib.request
from datetime import datetime

# Helper to query the local LLM
def ask_local_ai(prompt: str) -> str:
    try:
        from brain import ask_ai
        return ask_ai(prompt)
    except Exception as e:
        return f"Error querying local AI: {e}"

def execute_general_command(clean_text: str, raw_text: str = "") -> str | None:
    # 0. New: Dictation / Typing Helper
    if clean_text.startswith("type ") or clean_text.startswith("write ") or clean_text.startswith("insert "):
        if not clean_text.startswith("write a note") and not clean_text.startswith("write note"):
            try:
                import pyperclip
                import pyautogui
                pyautogui.FAILSAFE = False
                text_to_type = ""
                if clean_text.startswith("type "):
                    text_to_type = raw_text.strip()[5:]
                elif clean_text.startswith("write "):
                    text_to_type = raw_text.strip()[6:]
                elif clean_text.startswith("insert "):
                    text_to_type = raw_text.strip()[7:]
                
                if text_to_type:
                    # Remove trailing Whisper punctuation if it's a single period
                    if text_to_type.endswith(".") and not text_to_type.endswith("..."):
                        text_to_type = text_to_type[:-1]
                    pyperclip.copy(text_to_type)
                    time.sleep(0.1)
                    pyautogui.hotkey('ctrl', 'v')
                    return ""  # Silent success
            except Exception as e:
                return f"Failed to type text. Error: {e}"

    # 1. New: Screen OCR / Visual Reader
    if "read my screen" in clean_text or "scan screen text" in clean_text or "read screen" in clean_text or "ocr screen" in clean_text:
        try:
            import pyautogui
            import pyperclip
            # Graceful import check for pytesseract
            try:
                import pytesseract
            except ImportError:
                return "Sir, the pytesseract library is missing. Please run pip install pytesseract and ensure Tesseract OCR is installed on your system."
            
            temp_path = "temp_ocr_capture.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(temp_path)
            
            # Run OCR (catch executable errors gracefully)
            try:
                text = pytesseract.image_to_string(temp_path).strip()
            except Exception as tess_err:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return "Tesseract executable was not found. Please ensure Tesseract is in your Windows PATH variable."

            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            if not text:
                return "I completed the scan, but could not detect any readable text on the screen, sir."
            
            pyperclip.copy(text)
            return "I have scanned the text on your screen and copied it to your clipboard, sir."
        except Exception as e:
            return f"Failed to perform screen OCR. Error: {e}"

    # 2. New: Intelligent Draft Writer
    if "draft an email" in clean_text or "draft email" in clean_text or "draft a reply" in clean_text or "draft reply" in clean_text or "draft message" in clean_text:
        try:
            import pyperclip
            prompt = (
                "Write a professional, concise email draft or message reply based on this instruction. "
                "Do not include any headers or metadata, just the plain message body text:\n\n"
                f"{clean_text}"
            )
            draft = ask_local_ai(prompt)
            pyperclip.copy(draft)
            return "I've drafted the message and copied it to your clipboard, sir."
        except Exception as e:
            return f"Failed to draft message. Error: {e}"

    # 3. New: Voice Expense Tracker
    if "log expense" in clean_text or "log " in clean_text and ("dollars" in clean_text or "rupees" in clean_text or "spent" in clean_text):
        try:
            # Parse amount and category
            # E.g. "log twenty dollars for dinner" or "log 50 spent on lunch"
            match = re.search(r"log\s+(\d+|[a-zA-Z]+)\s*(?:dollars|rupees|spent)?\s*(?:on|for)\s+(.*)", clean_text)
            
            # Words to digit mapping fallback
            word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "twenty": 20, "fifty": 50, "hundred": 100}
            
            amount = 0
            category = "General"
            if match:
                amt_str = match.group(1).strip().lower()
                category = match.group(2).strip().capitalize().rstrip(".?,!")
                if amt_str.isdigit():
                    amount = int(amt_str)
                else:
                    amount = word_to_num.get(amt_str, 0)
            
            if amount == 0:
                # Try a broader search for a number
                num_match = re.search(r"(\d+)", clean_text)
                if num_match:
                    amount = int(num_match.group(1))
            
            if amount == 0:
                return "I couldn't identify the expense amount. Please specify the number, sir."
                
            csv_path = "finances.csv"
            exists = os.path.exists(csv_path)
            with open(csv_path, "a", encoding="utf-8") as f:
                if not exists:
                    f.write("Date,Amount,Category\n")
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{date_str},{amount},{category}\n")
            return f"Logged {amount} spent on {category}, sir."
        except Exception as e:
            return f"Failed to log expense. Error: {e}"

    if "how much did i spend" in clean_text or "spending summary" in clean_text or "check budget" in clean_text:
        try:
            csv_path = "finances.csv"
            if not os.path.exists(csv_path):
                return "No expenses have been logged yet, sir."
            
            total = 0
            count = 0
            with open(csv_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[1:]: # Skip header
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        try:
                            total += float(parts[1])
                            count += 1
                        except:
                            pass
            return f"Sir, you have spent a total of {total} across {count} logged items."
        except Exception as e:
            return f"Failed to check budget. Error: {e}"

    # 4. New: Smart Calendar Companion
    if "what is my schedule" in clean_text or "show calendar" in clean_text or "my schedule" in clean_text:
        try:
            ics_path = "calendar.ics"
            if not os.path.exists(ics_path):
                return "Calendar file calendar.ics was not found in your directory, sir."
            
            with open(ics_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Basic ICS parse for SUMMARY fields
            events = re.findall(r"SUMMARY:(.*)", content)
            if not events:
                return "Your calendar is empty, sir."
            
            today_events = [e.strip() for e in events[:3]] # Read top 3
            return "Here are your next events: " + " ... ".join(today_events)
        except Exception as e:
            return f"Failed to read calendar. Error: {e}"

    # 5. New: Wi-Fi / Internet Diagnostics
    if "run a speed test" in clean_text or "check my internet speed" in clean_text or "internet speed test" in clean_text or "speed test" in clean_text:
        try:
            # Check latency first via lightweight request
            t0 = time.time()
            try:
                urllib.request.urlopen("https://www.google.com", timeout=3)
                latency = int((time.time() - t0) * 1000)
            except:
                return "Sir, internet connectivity checks failed. You appear to be offline."

            # Check if speedtest library exists
            try:
                import speedtest
                s = speedtest.Speedtest()
                s.get_best_server()
                download = s.download() / 1e6
                upload = s.upload() / 1e6
                return f"Speed test complete. Latency is {latency} milliseconds, download speed is {download:.1f} Megabits per second, and upload is {upload:.1f} Megabits per second, sir."
            except:
                # Fallback benchmark: time download of a small resource
                test_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
                try:
                    t_start = time.time()
                    with urllib.request.urlopen(test_url, timeout=5) as r:
                        data = r.read()
                    elapsed = time.time() - t_start
                    size_kb = len(data) / 1024
                    speed_kbps = size_kb / elapsed
                    speed_mbps = (speed_kbps * 8) / 1000
                    return f"Internet connection is active, sir. Latency is {latency} milliseconds. Estimated basic download speed is {speed_mbps:.1f} Megabits per second."
                except:
                    return f"Connection is active with a latency of {latency} milliseconds, but speed tests are currently blocked."
        except Exception as e:
            return f"Failed to test internet speed. Error: {e}"

    # 6. New: Voice Translator
    if "translate" in clean_text:
        try:
            # E.g. "translate hello to spanish"
            match = re.search(r"translate\s+(.*)\s+to\s+([a-zA-Z\s]+)", clean_text, re.IGNORECASE)
            if match:
                text_to_translate = match.group(1).strip()
                lang = match.group(2).strip().capitalize()
                prompt = (
                    f"Translate the following text to {lang}. Output only the translated result "
                    f"without any explanation, brackets or quotes:\n\n{text_to_translate}"
                )
                translation = ask_local_ai(prompt)
                return f"The translation to {lang} is: {translation}"
            else:
                return "Please tell me what text to translate and what target language to use, sir."
        except Exception as e:
            return f"Failed translation. Error: {e}"

    # Tell me the time
    if "tell me the time" in clean_text or "what time is it" in clean_text or "current time" in clean_text or "what is the time" in clean_text:
        return datetime.now().strftime("The current time is %I:%M %p.")

    # Tell me the date
    if "tell me the date" in clean_text or "what's the date" in clean_text or "current date" in clean_text or "what is the date" in clean_text:
        return datetime.now().strftime("Today is %B %d, %Y.")

    # Voice Scratchpad / Notes
    if "write a note" in clean_text or "save a note" in clean_text:
        try:
            note_text = ""
            if "note" in clean_text:
                note_text = clean_text.split("note", 1)[1].strip()
            
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

    # Timer
    if "timer for" in clean_text or "set a timer" in clean_text:
        try:
            match = re.search(r"(\d+)\s*(second|minute|hour)s?", clean_text)
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

    # NATO Spelling Aid
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

    # Dice Roller / Coin Flipper
    if "flip a coin" in clean_text or "toss a coin" in clean_text:
        return f"It is {random.choice(['Heads', 'Tails'])}, sir."
    if "roll a dice" in clean_text or "roll a die" in clean_text:
        return f"It is a {random.randint(1, 6)}, sir."

    # Math Solver
    if "calculate" in clean_text or "what is" in clean_text:
        try:
            expr = clean_text.replace("times", "*").replace("divided by", "/").replace("plus", "+").replace("minus", "-")
            match = re.search(r"([\d\s\+\-\*\/\(\)\.]+)", expr)
            if match:
                math_expr = match.group(1).strip()
                if re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", math_expr):
                    res = eval(math_expr)
                    return f"The answer is {res}."
        except:
            pass

    # IP Address Lookup
    if "my ip address" in clean_text or "what's my ip" in clean_text or "ip configuration" in clean_text:
        try:
            import socket
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

    # News Reader
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

    # Wikipedia Summary
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

    # Joke Teller
    if "tell me a joke" in clean_text or "joke" in clean_text:
        jokes = [
            "Why do programmers wear glasses? Because they can't C sharp.",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "A SQL query goes into a bar, walks up to two tables and asks: Can I join you?",
            "Why did the programmer quit his job? Because he didn't get arrays."
        ]
        return random.choice(jokes)

    # Reminders
    if "remind me in" in clean_text or "set a reminder" in clean_text:
        try:
            match = re.search(r"remind me in (\d+)\s*(second|minute|hour)s?\s+to\s+(.*)", clean_text)
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

    # Weather Reports
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
        except:
            return "I am currently unable to fetch the weather telemetry, sir."

    return None
