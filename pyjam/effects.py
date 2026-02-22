import numpy as np

class Effect:
    def apply(self, signal): return signal

class Distortion(Effect):
    def __init__(self, drive=4.0): self.drive = drive
    def apply(self, signal): return np.tanh(signal * self.drive)

class Wah(Effect):
    """Simulates a wah-wah pedal with a sweeping resonant bandpass filter."""
    def __init__(self, sweep_rate=2.0, resonance=0.1):
        self.sweep_rate = sweep_rate
        self.resonance = resonance

    def apply(self, signal):
        from .engine import AudioEngine
        num_samples = len(signal)
        out = np.zeros(num_samples)
        
        # State variables for the filter
        low = 0
        band = 0
        
        for i in range(num_samples):
            # The LFO (Low Frequency Oscillator) that 'moves' the pedal
            f = 0.1 + 0.1 * np.sin(2 * np.pi * self.sweep_rate * i / AudioEngine.SAMPLE_RATE)
            
            # State-variable filter math
            low = low + f * band
            high = signal[i] - low - self.resonance * band
            band = f * high + band
            
            out[i] = band # Bandpass output gives the 'wah'
            
        return out

class Delay(Effect):
    def __init__(self, feedback=0.3, time=0.2):
        self.feedback, self.time = feedback, time
    def apply(self, signal):
        from .engine import AudioEngine
        ds = int(self.time * AudioEngine.SAMPLE_RATE)
        out = np.zeros(len(signal) + ds)
        out[:len(signal)] += signal
        out[ds:] += signal * self.feedback
        return out[:len(signal)]

class Tremolo(Effect):
    """Volume modulation for a 'shimmering' effect."""
    def __init__(self, rate=5.0, depth=0.5):
        self.rate, self.depth = rate, depth
    def apply(self, signal):
        from .engine import AudioEngine
        t = np.linspace(0, len(signal)/AudioEngine.SAMPLE_RATE, len(signal))
        mod = (1 - self.depth) + self.depth * np.sin(2 * np.pi * self.rate * t)
        return signal * mod

class Chorus(Effect):
    """Simulates multiple instruments playing together by slight delay modulation."""
    def __init__(self, rate=1.5, depth=0.002):
        self.rate, self.depth = rate, depth
    def apply(self, signal):
        from .engine import AudioEngine
        t = np.linspace(0, len(signal)/AudioEngine.SAMPLE_RATE, len(signal))
        delay_mod = (self.depth * AudioEngine.SAMPLE_RATE * np.sin(2 * np.pi * self.rate * t)).astype(int)
        out = np.copy(signal)
        for i in range(len(signal)):
            idx = i - abs(delay_mod[i])
            if idx >= 0:
                out[i] = (signal[i] + signal[idx]) * 0.5
        return out
