import numpy as np
import random
import re
from .engine import AudioEngine

class Instrument:
    """The Parent DAW Class. All instruments inherit these methods."""
    
    CHORDS = {
        "maj": [0, 4, 7], "min": [0, 3, 7], "dim": [0, 3, 6], "aug": [0, 4, 8],
        "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10],
        "sus2": [0, 2, 7], "sus4": [0, 5, 7]
    }
    
    SUFFIX_MAP = {
        "": "maj", "maj": "maj", "min": "min", "m": "min", "dim": "dim", 
        "7": "7", "maj7": "maj7", "M7": "maj7", "min7": "min7", "m7": "min7",
        "sus2": "sus2", "sus4": "sus4"
    }

    def __init__(self, volume=0.6):
        self.volume = volume
        self.effects = []

    def add_effect(self, effect_obj):
        """Add a pedal to the chain."""
        self.effects.append(effect_obj)
        return self

    def _apply_chain(self, signal):
        """Processes the signal through all added effects."""
        for fx in self.effects:
            signal = fx.apply(signal)
        return signal

    def parse_chord(self, chord_str):
        """Intelligently splits 'C#5min7' into Root, Octave, and Type."""
        match = re.match(r"([A-G]#?)(\d+)?(.*)", chord_str)
        if not match:
            raise ValueError(f"Could not parse chord: {chord_str}")
        
        root = match.group(1)
        octave = match.group(2) if match.group(2) else "4"
        suffix = match.group(3)
        
        ctype = self.SUFFIX_MAP.get(suffix.lower(), "maj")
        return root + octave, ctype

    def play(self, note_str, duration):
        """Plays a single note: instrument.play('C4', 1.0)"""
        freq = AudioEngine.get_freq(note_str)
        wave = self.play_raw(freq, duration)
        return self._apply_chain(wave) * self.volume

    def play_chord(self, chord_str, duration):
        """Plays a full chord: instrument.play_chord('Am7', 2.0)"""
        root_note, ctype = self.parse_chord(chord_str)
        root_freq = AudioEngine.get_freq(root_note)
        target_len = int(AudioEngine.SAMPLE_RATE * duration)
        chord_signal = np.zeros(target_len)
        
        for interval in self.CHORDS[ctype]:
            freq = root_freq * (2 ** (interval / 12))
            note_wave = self.play_raw(freq, duration)
            chord_signal += AudioEngine.trim_or_pad(note_wave, target_len)
            
        return self._apply_chain(chord_signal / 3) * self.volume

    def arpeggiate(self, chord_str, duration, pattern=None):
        """Plays a sequence of notes: instrument.arpeggiate('C', 2.0, [0,1,2,1])"""
        if pattern is None:
            pattern = [0, 1, 2, 1]
        
        root_note, ctype = self.parse_chord(chord_str)
        root_freq = AudioEngine.get_freq(root_note)
        step_dur = duration / len(pattern)
        
        arp_parts = []
        for n in pattern:
            interval = self.CHORDS[ctype][n % len(self.CHORDS[ctype])]
            freq = root_freq * (2 ** (interval / 12))
            arp_parts.append(self.play_raw(freq, step_dur))
            
        combined = np.concatenate(arp_parts)
        return self._apply_chain(combined) * self.volume

    def play_raw(self, freq, duration):
        """This is overwritten by specific instruments."""
        raise NotImplementedError("Subclasses must implement play_raw")

# =============================
# SPECIFIC INSTRUMENT "DNA"
# =============================

class Piano(Instrument):
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        return (np.sin(2*np.pi*freq*t) + 0.3*np.sin(4*np.pi*freq*t)) * np.exp(-2.5 * t)

class ElectricGuitar(Instrument):
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        return (np.sin(2*np.pi*freq*t) + 0.5*np.sin(2*np.pi*freq*2*t)) * np.exp(-3.5 * t)

class Bass(Instrument):
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        return (np.sin(2*np.pi*freq*0.5*t) + 0.1*np.sin(2*np.pi*freq*t)) * np.exp(-1.5 * t)

class Organ(Instrument):
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        wave = np.sin(2*np.pi*freq*t) + 0.5*np.sin(4*np.pi*freq*t) + 0.2*np.sin(6*np.pi*freq*t)
        envelope = (1 - np.exp(-50*t)) * np.exp(-1*t)
        return wave * envelope

class SynthPad(Instrument):
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        wave = np.sin(2*np.pi*freq*t) + np.sin(2*np.pi*(freq * 1.005)*t)
        envelope = (1 - np.exp(-5*t)) * np.exp(-0.5*t)
        return wave * envelope

class AcousticGuitar(Instrument):
    def play_raw(self, freq, duration):
        num_samples = int(AudioEngine.SAMPLE_RATE * duration)
        delay_line_len = int(AudioEngine.SAMPLE_RATE / freq)
        ring_buffer = np.random.uniform(-1, 1, delay_line_len)
        out = np.zeros(num_samples)
        for i in range(num_samples):
            out[i] = ring_buffer[i % delay_line_len]
            avg = 0.996 * 0.5 * (ring_buffer[i % delay_line_len] + ring_buffer[(i + 1) % delay_line_len])
            ring_buffer[i % delay_line_len] = avg
        return out

class Strings(Instrument):
    """Ensemble strings using 3 detuned sawtooth waves and a warm low-pass filter."""
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        def saw(f, detune):
            return 2 * (t * (f + detune) - np.floor(0.5 + t * (f + detune)))
        
        # Layered detuned sawtooths for that 'thick' string section feel
        wave = saw(freq, 0) + 0.5 * saw(freq, 0.5) + 0.5 * saw(freq, -0.5)
        # Slow attack and vibrato simulation
        vibrato = 1 + 0.005 * np.sin(2 * np.pi * 5 * t)
        wave = wave * vibrato
        envelope = (1 - np.exp(-4 * t)) * np.exp(-0.5 * t)
        return wave * envelope

class Flute(Instrument):
    """Triangular wave base with turbulence (filtered noise) and 'chiff' attack."""
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        # Triangular wave is closer to flute physics than a sine
        wave = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
        # Add 'breath' noise
        noise = np.random.normal(0, 0.1, len(t)) * np.exp(-10 * t) # Chiff at start
        turbulence = np.random.normal(0, 0.03, len(t)) # Constant breath
        # Add vibrato
        vibrato = np.sin(2 * np.pi * 6 * t) * 0.02
        wave = (wave + noise + turbulence) * (1 + vibrato)
        envelope = (1 - np.exp(-20 * t)) * np.exp(-1.5 * t)
        return wave * envelope

class Bell(Instrument):
    """Inharmonic FM Synthesis: Bell tones have non-integer partials."""
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        # Non-integer ratios create the 'metal' dissonance of a bell
        partial1 = np.sin(2 * np.pi * freq * 2.0 * t) * np.exp(-2 * t)
        partial2 = np.sin(2 * np.pi * freq * 3.41 * t) * 0.5 * np.exp(-3 * t)
        partial3 = np.sin(2 * np.pi * freq * 5.7 * t) * 0.3 * np.exp(-4 * t)
        wave = (np.sin(2 * np.pi * freq * t) + partial1 + partial2 + partial3)
        return wave * np.exp(-2 * t)

class Trumpet(Instrument):
    """Sawtooth wave with resonant harmonics and a bright 'brass' attack."""
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        # Summing odd/even harmonics for brassy buzz
        wave = np.sin(2*np.pi*freq*t)
        for i in range(2, 6):
            wave += (1.0/i) * np.sin(2*np.pi*freq*i*t)
        # Trumpet 'lip' tension envelope (bright start)
        brightness = np.exp(-5 * t)
        wave = wave * (0.5 + brightness)
        envelope = (1 - np.exp(-40 * t)) * np.exp(-2 * t)
        return wave * envelope

class Retro8Bit(Instrument):
    """Strict pulse-width modulation (PWM) square wave for NES/Gameboy sound."""
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        # 25% duty cycle square wave
        wave = np.where(np.mod(t * freq, 1) < 0.25, 1, -1)
        return wave * np.exp(-4 * t)

class SubBass(Instrument):
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        return np.sin(2 * np.pi * (freq/2) * t) * np.exp(-1 * t)

class Saxophone(Instrument):
    """Asymmetric sawtooth with 'growl' modulation (reedy distortion)."""
    def play_raw(self, freq, duration):
        t = np.linspace(0, duration, int(AudioEngine.SAMPLE_RATE * duration), False)
        # Sawtooth with a tanh curve creates reed-like pressure
        wave = np.tanh(2 * np.sin(2 * np.pi * freq * t) + np.sin(2 * np.pi * freq * 2 * t))
        # Add 'growl' (low frequency flutter)
        growl = 1 + 0.1 * np.sin(2 * np.pi * 30 * t)
        envelope = (1 - np.exp(-15 * t)) * np.exp(-1 * t)
        return wave * growl * envelope
