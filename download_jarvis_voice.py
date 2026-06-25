import urllib.request
import os

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        # Use headers to avoid generic User-Agent blocking
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print("Success!")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    
    onnx_url = "https://huggingface.co/jgkawell/jarvis/resolve/main/en/en_GB/jarvis/high/jarvis-high.onnx"
    json_url = "https://huggingface.co/jgkawell/jarvis/resolve/main/en/en_GB/jarvis/high/jarvis-high.onnx.json"
    
    download_file(onnx_url, os.path.join(model_dir, "jarvis-high.onnx"))
