import win32com.client

s = win32com.client.Dispatch("SAPI.SpVoice")
text = '<pitch absmiddle="-5">Hello Sir, I am Jarvis. System online.</pitch>'
s.Speak(text)
