import os
import subprocess
import re
import ctypes
import psutil
import pyautogui
from datetime import datetime
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Virtual Key Codes for media controls
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2

def press_media_key(vk_code):
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0) # Key Up

def execute_system_command(clean_text: str) -> str | None:
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

    # Open Chrome / Websites
    if is_open_request and ("chrome" in clean_text or "gmail" in clean_text or "youtube" in clean_text or "google" in clean_text or "github" in clean_text or "reddit" in clean_text or "stackoverflow" in clean_text):
        try:
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

    # Open VS Code
    if is_open_request and ("vs code" in clean_text or "vscode" in clean_text or "visual studio code" in clean_text):
        try:
            subprocess.Popen("code", shell=True)
            return "Opening Visual Studio Code."
        except Exception as e:
            return f"Failed to open VS Code. Error: {e}"

    # Open Spotify
    if is_open_request and "spotify" in clean_text:
        try:
            subprocess.Popen("start spotify:", shell=True)
            return "Opening Spotify."
        except Exception as e:
            return f"Failed to open Spotify. Error: {e}"

    # Open Calculator
    if is_open_request and ("calculator" in clean_text or "calc" in clean_text):
        try:
            subprocess.Popen("calc")
            return "Opening Calculator."
        except Exception as e:
            return f"Failed to open Calculator. Error: {e}"

    # Open Notepad
    if is_open_request and "notepad" in clean_text:
        try:
            subprocess.Popen("notepad")
            return "Opening Notepad."
        except Exception as e:
            return f"Failed to open Notepad. Error: {e}"

    # Open System Folders (Downloads, Documents, Desktop, Pictures)
    if "download" in clean_text or "document" in clean_text or "desktop" in clean_text or "picture" in clean_text:
        if any(verb in clean_text for verb in ["open", "show", "go to", "reveal", "folder", "directory"]):
            try:
                folder_name = "Downloads"
                if "document" in clean_text:
                    folder_name = "Documents"
                elif "desktop" in clean_text:
                    folder_name = "Desktop"
                elif "picture" in clean_text:
                    folder_name = "Pictures"
                
                folder_path = os.path.join(os.path.expanduser("~"), folder_name)
                if os.path.exists(folder_path):
                    subprocess.Popen(["explorer", os.path.normpath(folder_path)])
                    return f"Opening your {folder_name} folder, sir."
                else:
                    return f"I couldn't locate your {folder_name} folder, sir."
            except Exception as e:
                return f"Failed to open folder. Error: {e}"

    # Shutdown PC
    if "shutdown" in clean_text or "shut down my computer" in clean_text:
        os.system("shutdown /s /t 5")
        return "Shutting down the system in 5 seconds. Goodbye."

    # Restart PC
    if "restart" in clean_text or "restart my computer" in clean_text:
        os.system("shutdown /r /t 5")
        return "Restarting the system in 5 seconds."

    # Lock PC
    if "lock pc" in clean_text or "lock computer" in clean_text or "lock the pc" in clean_text:
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Locking the workstation."
        except Exception as e:
            return f"Failed to lock the workstation. Error: {e}"

    # Open Docker Desktop
    if is_open_request and ("docker desktop" in clean_text or "docker" in clean_text):
        standard_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
        try:
            if os.path.exists(standard_path):
                subprocess.Popen([standard_path])
            else:
                subprocess.Popen("Docker Desktop.exe", shell=True)
            return "Opening Docker Desktop."
        except Exception as e:
            return f"Failed to open Docker Desktop. Error: {e}"

    # System Status / Telemetry
    if "status report" in clean_text or "system status" in clean_text or "telemetry" in clean_text:
        try:
            cpu_usage = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()
            mem_usage = memory_info.percent
            battery = psutil.sensors_battery()
            battery_str = ""
            if battery:
                percent = battery.percent
                charging = battery.power_plugged
                plugged_status = "and charging" if charging else "and discharging"
                battery_str = f", and your battery is at {percent} percent {plugged_status}"
            return f"Sir, CPU load is at {cpu_usage} percent, memory utilization is at {mem_usage} percent{battery_str}."
        except Exception as e:
            return f"Failed to retrieve system status. Error: {e}"

    # Screenshot
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

    # Media Playback Controls
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

    # Volume Control
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

    # Empty Recycle Bin
    if "empty recycle bin" in clean_text or "clean the trash" in clean_text or "empty trash" in clean_text:
        try:
            SHERB_NOCONFIRMATION = 0x00000001
            SHERB_NOSOUND = 0x00000004
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, SHERB_NOCONFIRMATION | SHERB_NOSOUND)
            return "Recycle bin emptied, sir."
        except Exception as e:
            return f"Failed to empty recycle bin. Error: {e}"

    # Active Window Controls
    if "close this window" in clean_text or "close window" in clean_text:
        try:
            VK_MENU = 0x12
            VK_F4 = 0x73
            ctypes.windll.user32.keybd_event(VK_MENU, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_F4, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_F4, 0, 2, 0)
            ctypes.windll.user32.keybd_event(VK_MENU, 0, 2, 0)
            return "Closing active window."
        except Exception as e:
            return f"Failed to close window. Error: {e}"

    if "minimize window" in clean_text or "minimize this window" in clean_text:
        try:
            VK_LWIN = 0x5B
            VK_DOWN = 0x28
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_DOWN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_DOWN, 0, 2, 0)
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
            return "Minimizing active window."
        except Exception as e:
            return f"Failed to minimize window. Error: {e}"

    # Meeting / Focus Mode
    if "meeting mode" in clean_text or "focus mode" in clean_text:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            
            # Minimize all windows Win+M
            VK_LWIN = 0x5B
            VK_M = 0x4D
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_M, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_M, 0, 2, 0)
            ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
            return "Meeting mode activated. Master audio muted and windows minimized, sir."
        except Exception as e:
            return f"Failed to activate meeting mode. Error: {e}"

    # Battery
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
                return "No battery detected, sir."
        except Exception as e:
            return f"Failed to check battery. Error: {e}"

    # Disk Space C:
    if "check storage" in clean_text or "disk space" in clean_text or "hard drive space" in clean_text:
        try:
            obj = psutil.disk_usage('C:\\')
            free_gb = obj.free / (1024**3)
            total_gb = obj.total / (1024**3)
            return f"C: drive has {free_gb:.1f} gigabytes free out of {total_gb:.1f} gigabytes total, sir."
        except Exception as e:
            return f"Failed to check disk usage. Error: {e}"

    # Organize Downloads
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

    return None
