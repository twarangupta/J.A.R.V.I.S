import numpy as np
import pyaudio
import time

def play_startup_sound():
    """
    Synthesizes a premium, modern Iron Man repulsor boot-up sequence.
    Uses FM (Frequency Modulation) synthesis and detuned oscillators
    to create a thick, metallic plasma charge and stabilizer lock sound.
    """
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=44100,
                        output=True)
        
        sample_rate = 44100
        
        # --- PHASE 1: Micro-thruster igniter spark (0.0 to 0.2s) ---
        duration_igniter = 0.2
        t_igniter = np.linspace(0, duration_igniter, int(sample_rate * duration_igniter), False)
        # Buzzy white-noise spark modulated by a high frequency sine wave
        noise = np.random.uniform(-1.0, 1.0, len(t_igniter))
        spark = noise * np.sin(2 * np.pi * 3000 * t_igniter) * 0.05
        # Quick decay envelope
        spark *= np.exp(-15 * t_igniter)
        
        # --- PHASE 2: Repulsor FM Plasma Charge Sweep (0.0 to 1.3s) ---
        duration_sweep = 1.3
        t_sweep = np.linspace(0, duration_sweep, int(sample_rate * duration_sweep), False)
        
        # Carrier sweeps from 100Hz to 750Hz (logarithmic)
        fc = 100 * (7.5 ** t_sweep)
        # Modulating frequency (gives the plasma "buzz" texture)
        fm = 180
        # Modulation index rises over time (plasma density increases)
        beta = 4.0 * t_sweep
        
        # FM Synthesis: y = sin(2*pi*fc*t + beta*sin(2*pi*fm*t))
        # We detune two voices slightly to create a thick chorus effect
        voice1 = np.sin(2 * np.pi * fc * t_sweep + beta * np.sin(2 * np.pi * fm * t_sweep))
        voice2 = np.sin(2 * np.pi * (fc + 5) * t_sweep + beta * np.sin(2 * np.pi * (fm + 2) * t_sweep))
        sweep_data = (voice1 * 0.5 + voice2 * 0.5).astype(np.float32)
        
        # Fade in and pulse sweep (tremolo to simulate power stabilizing)
        pulse = 0.8 + 0.2 * np.sin(2 * np.pi * 12 * t_sweep)
        env_sweep = np.linspace(0, 1, len(t_sweep)) ** 2  # Exponential growth
        sweep_data *= env_sweep * pulse * 0.22
        
        # --- PHASE 3: Stabilizer Lock chime (0.0 to 0.8s) ---
        duration_chime = 0.8
        t_chime = np.linspace(0, duration_chime, int(sample_rate * duration_chime), False)
        
        # Metallic chords (combine resonant frequencies of Iron Man HUD chimes)
        freqs = [659.25, 987.77, 1318.51, 1975.53] # E5, B5, E6, B6
        chime_data = np.zeros_like(t_chime)
        for i, f in enumerate(freqs):
            chime_data += np.sin(2 * np.pi * f * t_chime) * (0.4 / (i + 1))
            
        # Add ring modulation (creates high-tech metallic tint)
        chime_data *= np.sin(2 * np.pi * 500 * t_chime) * 0.3 + 0.7
        # Long exponential decay
        env_chime = np.exp(-4 * t_chime)
        chime_data = (chime_data * env_chime * 0.25).astype(np.float32)
        
        # --- COMBINE ALL PHASES ---
        # Overlap igniter spark with the start of the sweep
        sweep_data[:len(spark)] += spark
        full_sound = np.concatenate([sweep_data, chime_data])
        
        # Play audio
        stream.write(full_sound.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        print(f"[Audio Boot warning] Failed to play startup tone: {e}")

def play_sleep_sound():
    """
    Synthesizes a futuristic repulsor power-down and standby tone
    using FM synthesis. Bypasses silently on any driver error.
    """
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=44100,
                        output=True)
        
        sample_rate = 44100
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Power-down frequency sweep (600Hz -> 60Hz)
        fc = 600 * (0.1 ** t)
        # FM modulation frequency and index (for buzzy power drain texture)
        fm = 120
        beta = 3.0 * (1.0 - t)
        
        voice1 = np.sin(2 * np.pi * fc * t + beta * np.sin(2 * np.pi * fm * t))
        voice2 = np.sin(2 * np.pi * (fc - 3) * t + beta * np.sin(2 * np.pi * (fm - 1) * t))
        sound_data = (voice1 * 0.5 + voice2 * 0.5).astype(np.float32)
        
        # Exponential volume decay (system going cold)
        env = np.exp(-3 * t)
        sound_data *= env * 0.22
        
        stream.write(sound_data.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        print(f"[Audio Sleep warning] Failed to play sleep tone: {e}")

if __name__ == "__main__":
    print("Testing upgraded Iron Man startup and sleep tones...")
    play_startup_sound()
    time.sleep(1)
    play_sleep_sound()
