import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os
import re

class AudioEngine:
    SAMPLE_RATE = 44100
    
    NOTES = {
        "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63,
        "F": 349.23, "F#": 369.99, "G": 392.00, "G#": 415.30, "A": 440.00,
        "A#": 466.16, "B": 493.88
    }

    @staticmethod
    def get_freq(note_str):
        """Converts 'C4', 'C5', 'A#2' to frequency. Defaults to octave 4."""
        note_str = note_str.upper().strip()
        
        # Use regex to split note name from octave number
        # Matches (Letters and #) followed by (Digits)
        match = re.match(r"([A-G]#?)(\d+)?", note_str)
        if not match:
            raise ValueError(f"Invalid note format: {note_str}")
            
        note_name = match.group(1)
        octave = int(match.group(2)) if match.group(2) else 4
            
        if note_name not in AudioEngine.NOTES:
            raise ValueError(f"Unknown note: {note_name}")
            
        base_freq = AudioEngine.NOTES[note_name]
        # Frequency calculation: freq = base * 2^(octave - 4)
        return base_freq * (2.0 ** (octave - 4))

    @staticmethod
    def trim_or_pad(signal, length):
        if len(signal) > length: return signal[:length]
        return np.pad(signal, (0, max(0, length - len(signal))))

    @staticmethod
    def normalize(signal, volume=0.8):
        if np.max(np.abs(signal)) > 0:
            signal = signal / np.max(np.abs(signal))
        return signal * volume

    @staticmethod
    def save(signal, filename):
        base_name = os.path.splitext(filename)[0]
        wav_path = f"{base_name}.wav"
        mp3_path = f"{base_name}.mp3"
        int_data = (signal * 32767).astype(np.int16)
        write(wav_path, AudioEngine.SAMPLE_RATE, int_data)
        try:
            AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3")
            print(f"Exported: {wav_path} and {mp3_path}")
        except:
            print(f"WAV saved. MP3 export failed.")
