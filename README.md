
# PyJam 🎸🎹

**PyJam** is a lightweight, Object-Oriented Digital Audio Workstation (DAW) for Python. It allows developers and musicians to generate complex musical arrangements, synthesis, and pedalboard effects entirely through code.

Whether you want to build a procedural backing track for a game, experiment with physical modeling synthesis, or create a virtual pedalboard for your guitar, PyJam provides the tools to do it.

## 🚀 Features

* **10+ Built-in Instruments:** From Physical Modeling (Acoustic Guitar, Flute) to FM Synthesis (Bells) and Subtractive Synthesis (Synths, Strings).
* **Virtual Pedalboard:** Chain effects like Distortion, Delay, Wah, and Chorus using a modular API.
* **Music Theory Engine:** Intelligent chord parsing (e.g., `Am7`, `C#maj7`, `Gsus4`) and automatic frequency calculation across octaves (e.g., `C4`, `A5`).
* **Format Agnostic:** High-fidelity WAV export and web-friendly MP3 support out of the box.

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/OmarSoudan/PyJam.git
cd PyJam

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


*Note: To export MP3 files, ensure you have `ffmpeg` installed on your system.*

## 🎸 Quick Start

```python
from pyjam import ElectricGuitar, Distortion, Delay, AudioEngine

# 1. Initialize your instrument
guitar = ElectricGuitar(volume=0.5)

# 2. Build your pedalboard
guitar.add_effect(Distortion(drive=4.0)).add_effect(Delay(time=0.2))

# 3. Play a riff or a chord
riff = guitar.arpeggiate("Am7", duration=2.0, pattern=[0, 2, 1, 3])

# 4. Save your jam
AudioEngine.save(riff, "my_first_riff")

```

## 🎻 Instruments Available

| Category | Instruments | Synthesis Method |
| --- | --- | --- |
| **Acoustic** | Piano, AcousticGuitar, Flute, Strings | Physical Modeling / Additive |
| **Electric** | ElectricGuitar, Bass, Organ | Harmonic Summation |
| **Brass** | Trumpet, Saxophone | Resonant Waves |
| **Digital** | SynthPad, SubBass, Retro8Bit, Bell | FM / Subtractive / PWM |

## 🎛️ Effects (Pedalboard)

Chain these to any instrument using `.add_effect()`:

* `Distortion(drive)`: Soft-clipping saturation.
* `Delay(feedback, time)`: Tempo-synced echo.
* `Wah(sweep_rate)`: Resonant auto-wah filter.
* `Chorus(rate, depth)`: Thick ensemble modulation.
* `Tremolo(rate, depth)`: Classic volume pulsing.

## 🛠️ Development & Contribution

PyJam is built using **Object-Oriented Programming (OOP)**. To add a new instrument, simply inherit from the `Instrument` base class and define your `play_raw` logic:

```python
class MyCustomSynth(Instrument):
    def play_raw(self, freq, duration):
        # Your custom math here
        return np.sin(2 * np.pi * freq * t)

```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Created by** [OmarSoudan](https://github.com/OmarSoudan)   🚀

---


