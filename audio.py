import pyaudio
import numpy as np
import time
from config import SAMPLE_RATE, CHUNK_SIZE

class AudioHandler:
    """
    Manages microphone input streams.
    Provides methods to stream raw chunks for wake word detection,
    and to record complete phrases with basic silence detection for Whisper.
    """
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self):
        """Starts the microphone input stream."""
        if self.stream is not None:
            self.stop_stream()
            
        try:
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE
            )
        except Exception as e:
            print(f"[Audio Error] Failed to open microphone stream: {e}")
            raise e

    def stop_stream(self):
        """Stops and closes the microphone stream."""
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                print(f"[Audio Error] Error closing stream: {e}")
            self.stream = None

    def read_chunk(self) -> np.ndarray:
        """
        Reads a single chunk of audio from the stream.
        Returns a numpy array of int16 samples.
        """
        try:
            if self.stream is None or not self.stream.is_active():
                self.start_stream()
        except OSError:
            self.stream = None
            self.start_stream()
            
        try:
            data = self.stream.read(CHUNK_SIZE, exception_on_overflow=False)
            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            # Underflow/Overflow or hardware issues
            return np.zeros(CHUNK_SIZE, dtype=np.int16)

    def record_phrase(self, silence_threshold=500, silence_timeout_seconds=2.0, max_seconds=10.0) -> np.ndarray:
        """
        Records the microphone stream until silence is detected or max duration is reached.
        Returns a normalized float32 numpy array, ready for Whisper.
        """
        print("[Listening for speech...]")
        self.start_stream()
        
        recorded_frames = []
        silent_chunks = 0
        
        # Calculate how many chunks represent the silence timeout
        # Each chunk is 1280 samples at 16000Hz = 80ms (0.08 seconds)
        chunk_duration = CHUNK_SIZE / SAMPLE_RATE
        max_silent_chunks = int(silence_timeout_seconds / chunk_duration)
        max_total_chunks = int(max_seconds / chunk_duration)
        
        started_speaking = False
        
        for _ in range(max_total_chunks):
            chunk = self.read_chunk()
            recorded_frames.append(chunk)
            
            # Simple volume threshold check (using Root Mean Square or max amplitude)
            amplitude = np.max(np.abs(chunk))
            
            if amplitude > silence_threshold:
                if not started_speaking:
                    # Voice activity detected
