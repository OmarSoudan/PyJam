# PyJam 🎸🎹

PyJam is a lightweight, object-oriented Digital Audio Workstation (DAW) for Python. It provides a compact API for generating musical arrangements, synthesizing instruments, and building virtual pedalboards—aimed at developers, sound designers, and musicians who want programmatic control over audio production.

Key design goals:
- Easy-to-use, Pythonic API for instruments and effects
- Modular pedalboard architecture for chaining audio effects
- High-fidelity WAV export with optional MP3 support
- Extensible: add new instruments or effects by subclassing base classes

---

## 🚀 Features

- 10+ built-in instruments (physical-modeling, FM, subtractive)
- Modular pedalboard with distortion, delay, chorus, wah, tremolo, etc.
- Music-theory utilities for chord parsing and octave mapping (e.g. `Am7`, `C#maj7`, `C4`)
- Export to WAV (high quality) and MP3 (requires `ffmpeg`)
- Designed for programmatic composition and quick prototyping

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/OmarSoudan/PyJam.git
cd PyJam
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Note: To export MP3 files, ensure `ffmpeg` is installed on your system.

---

## 🎸 Quick Start

Example usage demonstrating instrument creation, pedalboard chaining, and saving audio:

```python
from pyjam import ElectricGuitar, Distortion, Delay, AudioEngine

# Initialize an instrument
guitar = ElectricGuitar(volume=0.5)

# Build a pedalboard
guitar.add_effect(Distortion(drive=4.0)).add_effect(Delay(time=0.2))

# Create a riff or chord progression
riff = guitar.arpeggiate("Am7", duration=2.0, pattern=[0, 2, 1, 3])

# Export the audio
AudioEngine.save(riff, "my_first_riff.wav")
```

---

## 🎻 Available Instruments

- Acoustic: Piano, AcousticGuitar, Flute, Strings (physical modeling / additive)
- Electric: ElectricGuitar, Bass, Organ (harmonic summation)
- Brass: Trumpet, Saxophone (resonant wave models)
- Digital: SynthPad, SubBass, Retro8Bit, Bell (FM / subtractive / PWM)

If you add a new instrument, inherit from the `Instrument` base class and implement `play_raw`.

---

## 🎛️ Effects (Pedalboard)

Common effects you can chain using `.add_effect()`:

- Distortion(drive): soft-clipping saturation
- Delay(feedback, time): tempo-aligned echo
- Wah(sweep_rate): resonant auto-wah filter
- Chorus(rate, depth): ensemble modulation
- Tremolo(rate, depth): amplitude modulation

---

## 🛠 Development

To add a custom instrument, subclass the `Instrument` base class and implement the audio generation logic:

```python
class MyCustomSynth(Instrument):
    def play_raw(self, freq, duration, sr=44100):
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        return np.sin(2 * np.pi * freq * t)
```

Please include tests and a short benchmark or example when contributing new instruments or effects.

---

## Contributing

Contributions are welcome. Open issues for bugs or feature requests and submit PRs for additions. Follow the existing code style and include documentation and examples for new features.

---

## License & Author

PyJam is distributed under the MIT License. See `LICENSE` for details.

Created by [OmarSoudan](https://github.com/OmarSoudan)
