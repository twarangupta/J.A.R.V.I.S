# J.A.R.V.I.S. - Premium Desktop AI Assistant

J.A.R.V.I.S. (Just A Rather Very Intelligent System) is a highly advanced, local, voice-controlled desktop assistant. Inspired by Iron Man's J.A.R.V.I.S., this project combines real-time **neural text-to-speech**, **speech-to-text voice recognition**, and **accurate wake word detection** with a local LLM brain (`Llama 3.2`) running entirely offline on your machine.

---

## 🌟 Key Features

* **🧠 Offline Cognitive Brain:** Powered by local Ollama (`llama3.2:3b`) with full conversational context memory.
* **🎙️ Local Wake Word Engine:** Stands by quietly in the background waiting for you to say *"Hey Jarvis"* (powered by OpenWakeWord).
* **🗣️ Premium Neural Speech (Piper TTS):** Realistic, low-latency vocal responses using local `.onnx` voice models.
* **🔇 Smart Interruption System:** 
  * **By Voice:** Say *"Hey Jarvis"* during speech to instantly cut him off and speak.
  * **By Keyboard:** Press **any key** (e.g. `Space` or `Enter`) in the terminal to immediately halt his speech.
* **🛠️ 40+ Core Commands:** Built-in voice macros for app launching, media control, system diagnostics, and developer helpers.
* **👋 Safe Exit:** Press `Ctrl + C` to shut down, and Jarvis will verbally say goodbye before going offline.

---

## 📋 Table of Voice Commands

### 🔍 Search & Browsing
* *"Search for [query]"* / *"Google [query]"* $\rightarrow$ Performs a Google search in Chrome.
* *"Open [gmail / youtube / github / reddit / stackoverflow]"* $\rightarrow$ Launches browser straight to the page.
* *"Open Chrome"* $\rightarrow$ Opens a fresh web browser.

### 🐙 Git & Local Environments
* *"Git status"* $\rightarrow$ Tells you the number of modified/untracked files.
* *"Commit my changes [with message 'msg' / saying 'msg']"* $\rightarrow$ Stages and commits changes using your custom message (falls back to timestamp if none provided).
* *"Git push"* $\rightarrow$ Pushes commits to the remote branch on origin.
* *"Git pull"* $\rightarrow$ Pulls updates from remote repository.
* *"Git stash"* / *"Git stash pop"* $\rightarrow$ Save modifications or restore stashed changes.
* *"Check conflicts"* / *"Merge conflicts"* $\rightarrow$ Checks for unmerged git conflict markers in files.
* *"Git log"* / *"Show commits"* $\rightarrow$ Reads out the last 5 commits.
* *"Switch branch to [name]"* $\rightarrow$ Checkouts the specified branch.
* *"Create branch [name]"* $\rightarrow$ Creates and switches to a new local branch.
* *"List branches"* $\rightarrow$ Lists local branches and highlights active one.
* *"Check port [number]"* / *"What is on port [number]"* $\rightarrow$ Finds the Process ID (PID) listening on that port.
* *"Kill port [number]"* $\rightarrow$ Kills the process blocking that port.
* *"Check Docker"* / *"Docker status"* $\rightarrow$ Lists running container names.
* *"Check container logs for [name]"* $\rightarrow$ Fetches the last 20 lines of docker logs to your clipboard.

### 🧠 Developer Utilities
* *"Jarvis, review my code"* $\rightarrow$ Analyzes `git diff` and writes a detailed review to `code_review.md`.
* *"Write a unit test for [filename]"* $\rightarrow$ Generates `pytest` test suites.
* *"Search codebase for [term]"* $\rightarrow$ Finds files containing your query.
* *"Create FastAPI boilerplate"* $\rightarrow$ Writes a ready FastAPI server script to `main.py`.
* *"Format JSON"* $\rightarrow$ Prettifies minified JSON on your clipboard.
* *"Debug this crash"* / *"Analyze stack trace"* $\rightarrow$ Reads traceback from clipboard, diagnoses the error using local AI, and writes `debug_report.md`.
* *"Audit my dependencies"* $\rightarrow$ Scans `requirements.txt` or `package.json` for outdated packages.
* *"Send a [GET/POST] request to [url]"* $\rightarrow$ Runs API requests and copies response/headers to clipboard.
* *"Explain code file [filename]"* $\rightarrow$ Feeds the code file to local Ollama and explains its architecture and classes.

### 📂 File & Windows OS Operations
* *"Open [vscode / spotify / calculator / notepad / docker]"* $\rightarrow$ Launches desktop applications.
* *"Open [downloads folder / documents / desktop / pictures]"* $\rightarrow$ Opens the corresponding folder in Windows Explorer.
* *"Take a screenshot"* $\rightarrow$ Captures screen and saves it on your Desktop.
* *"Organize my downloads"* $\rightarrow$ Sorts your Downloads folder by file extension categories.
* *"Close this window"* / *"Minimize window"* $\rightarrow$ Close/Minimize active windows.
* *"Empty Recycle Bin"* $\rightarrow$ Clears the Windows trash silently.

### 🔊 Audio, Volume & Media Controls
* *"Play music"* / *"Pause"* $\rightarrow$ Toggle Spotify/YouTube playback.
* *"Next song"* / *"Previous track"* $\rightarrow$ Skip/go back in music tracks.
* *"Mute"* / *"Unmute"* $\rightarrow$ Mute master Windows audio.
* *"Set volume to [0-100]%"* $\rightarrow$ Precise volume control (e.g. *"Set volume to 50%"*).
* *"Increase volume"* / *"Lower volume"* $\rightarrow$ Raises/lowers master volume.

### 📊 System Diagnostics
* *"Jarvis, status report"* / *"System status"* $\rightarrow$ Verbally reports CPU load, memory utilization, and battery.
* *"Check storage"* / *"Disk space"* $\rightarrow$ Reports free storage on your C: drive.
* *"What time is it"* / *"Tell me the date"* $\rightarrow$ Current clock time or date.
* *"What is my IP address"* $\rightarrow$ Reports local and public IP addresses.

### 📅 Notes, Timers & Reminders
* *"Write a note: [content]"* $\rightarrow$ Appends a timestamped note to `notes.md`.
* *"Read my notes"* $\rightarrow$ Reads aloud your 3 most recently saved notes.
* *"Set a timer for [X] [seconds/minutes]"* $\rightarrow$ Counts down in background and alerts you.
* *"Remind me in [X] [seconds/minutes] to [task]"* $\rightarrow$ Async background timer task alert.

### 🌐 Information & Entertainment
* *"What's the weather"* $\rightarrow$ Geo-IP lookup weather report.
* *"Read today's headlines"* $\rightarrow$ Reads top World News headlines.
* *"Wikipedia for [topic]"* $\rightarrow$ Reads a Wikipedia page summary.
* *"Spell [word]"* $\rightarrow$ Spells the word using the NATO phonetic alphabet.
* *"Calculate [expression]"* $\rightarrow$ Solves vocal math equations (e.g. *"Calculate 145 times 3"*).
* *"Tell me a joke"* $\rightarrow$ Returns a funny developer joke.
* *"Flip a coin"* / *"Roll a dice"* $\rightarrow$ Heads/Tails coin toss or dice roll.
* *"Read my screen"* / *"Scan screen text"* $\rightarrow$ Performs OCR screenshot analysis and copies text to clipboard.
* *"Draft [an email / reply / message]"* $\rightarrow$ Uses local AI to generate professional text draft to clipboard.
* *"Log [X] dollars for [category]"* $\rightarrow$ Logs transaction to `finances.csv` and reads budget summaries.
* *"What is my schedule today"* / *"My schedule"* $\rightarrow$ Parses local calendar `calendar.ics` and lists upcoming events.
* *"Run a speed test"* $\rightarrow$ Measures local download speeds and ping latency.
* *"Translate [text] to [language]"* $\rightarrow$ Submits translation tasks to local Ollama.
* *"Type [text]"* / *"Write [text]"* $\rightarrow$ Paste-types spoken text directly at cursor silently.

### 🤫 Focus, Audio Themes & Greetings
* *"Meeting mode"* / *"Focus mode"* $\rightarrow$ Mutes the PC and minimizes all open windows.
* *"Start project [name]"* $\rightarrow$ Launches VS Code in the workspace and opens GitHub.
* **Premium Audio Effects**: Procedural synthesis of Iron Man power-up sound effects upon startup, and sweep power-down tones upon running standby "go to sleep".
* **Dynamic Greetings**: Randomly speaks either location weather (IP-derived), laptop battery telemetry, or Avengers-themed diagnostic quotes on boot.

---

## 🚀 Installation & Setup

### 1. Prerequisites
* **Python 3.10** (Recommended)
* **Ollama** installed on your system. [Download Ollama here](https://ollama.com/).

### 2. Download LLM Brain
Open your terminal and run:
```bash
ollama pull llama3.2:3b
```

### 3. Setup Virtual Environment & Install Dependencies
Clone this repository, navigate to the folder, and run:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 4. Download J.A.R.V.I.S. Voice Model
Run the setup download script to fetch the high-quality neural voice model (~114 MB):
```powershell
python download_jarvis_voice.py
```
This saves the model files to `models/jarvis-high.onnx` and `models/jarvis-high.onnx.json`.

---

## 🏃 Running Jarvis

1. Make sure your local **Ollama** service is running (`ollama serve`).
2. Run the main runner file:
```powershell
.\venv\Scripts\python.exe jarvis.py
```
3. Wait for the startup text: `All systems active. Jarvis is online.`
4. Say **"Hey Jarvis"** to wake him up!

---

## 🛠️ Troubleshooting & Error Handling

### 1. PortAudio Conflicts (`OSError: Stream not open`)
* **Cause:** Happens when multiple libraries (`sounddevice` and `pyaudio`) compete for audio channels.
* **Fix:** Jarvis has been refactored to use `pyaudio` for both recording AND speech playback, preventing PortAudio resource crashes.

### 2. Windows Terminal Freezing (QuickEdit Mode)
* **Cause:** In Windows PowerShell/CMD, clicking inside the console window suspends the running Python script to let you highlight text.
* **Fix:** Press **Enter** or **Right-Click** inside the terminal window to unfreeze it.

### 3. Immediate Interruption / Loop Feedback
* **Cause:** The wake-up trigger registers in the wake word detector's buffer, triggering an immediate "interrupted by user" stop when speech starts.
* **Fix:** Jarvis now ignores the first **0.5 seconds** of audio stream during speech and runs `.reset()` on the detector buffer to clear the wakeup event history.

### 4. Acoustic Feedback (Can't interrupt with voice)
* **Cause:** Speakers are playing Jarvis's voice too loud, causing the microphone to get flooded with speaker output, which drops wake word detector confidence.
* **Fix:** Speak loudly or use headphones. Alternatively, press **any keyboard key** (e.g. `Spacebar`) in the active terminal console to halt speech instantly.
