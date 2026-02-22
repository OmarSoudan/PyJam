import numpy as np
from pyjam import (
    Piano, ElectricGuitar, Bass, Organ, SynthPad, AcousticGuitar,
    Strings, Flute, Bell, Trumpet, Retro8Bit, SubBass, Saxophone,
    Distortion, Delay, AudioEngine
)

# 1. Initialize the Orchestra
instr_list = {
    "Piano": Piano(volume=0.5),
    "Guitar": ElectricGuitar(volume=0.4).add_effect(Distortion(2.0)),
    "Bass": Bass(volume=0.7),
    "Organ": Organ(volume=0.4),
    "Pad": SynthPad(volume=0.3),
    "Acoustic": AcousticGuitar(volume=0.5),
    "Strings": Strings(volume=0.4),
    "Flute": Flute(volume=0.4),
    "Bell": Bell(volume=0.3),
    "Trumpet": Trumpet(volume=0.3),
    "8Bit": Retro8Bit(volume=0.3),
    "Sub": SubBass(volume=0.8),
    "Sax": Saxophone(volume=0.4)
}

full_demo = np.array([])
chord = "Am7"
dur = 2.0

print("Testing all instruments one by one...")

for name, obj in instr_list.items():
    print(f" -> Playing {name}")
    # Each instrument plays the chord differently
    if name in ["Bass", "Sub"]:
        # Low end just plays the root
        audio = obj.play(chord[0] + "2", dur)
    elif name in ["Guitar", "Acoustic"]:
        # Guitars arpeggiate
        audio = obj.arpeggiate(chord, dur, pattern=[0, 2, 1, 3])
    else:
        # Others play the full chord
        audio = obj.play_chord(chord, dur)
    
    # Add a tiny gap between tests
    gap = np.zeros(int(AudioEngine.SAMPLE_RATE * 0.5))
    full_demo = np.concatenate([full_demo, audio, gap])

# 3. Save the mega-test
final = AudioEngine.normalize(full_demo)
AudioEngine.save(final, "PyJam_Mega_Test")
