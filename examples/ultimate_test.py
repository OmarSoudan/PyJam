import numpy as np
from pyjam import (
    Piano, ElectricGuitar, Bass, Organ, SynthPad, AcousticGuitar,
    Strings, Flute, Bell, Trumpet, Retro8Bit, SubBass, Saxophone,
    Distortion, Delay, AudioEngine
)

def run_mega_test():
    # 1. Initialize Orchestra
    orchestra = {
        "Grand Piano": Piano(0.5),
        "Electric Guitar": ElectricGuitar(0.4).add_effect(Distortion(2.5)),
        "Folk Acoustic": AcousticGuitar(0.5),
        "Deep Bass": Bass(0.7),
        "Church Organ": Organ(0.4),
        "Ambient Pad": SynthPad(0.3).add_effect(Delay(time=0.4)),
        "String Ensemble": Strings(0.4),
        "Silver Flute": Flute(0.4),
        "Golden Bell": Bell(0.3),
        "Jazz Trumpet": Trumpet(0.3),
        "Retro NES": Retro8Bit(0.3),
        "Sub Power": SubBass(0.8),
        "Alto Sax": Saxophone(0.4)
    }

    full_audio = np.array([])
    bpm = 100
    beat = 60 / bpm

    print("--- Starting PyJam Mega Test ---")

    for name, inst in orchestra.items():
        print(f"Testing: {name}...")
        
        # Test 1: Standard Major Chord
        chord1 = inst.play_chord("C4maj", beat * 2)
        
        # Test 2: Sophisticated Minor 7th Chord
        chord2 = inst.play_chord("A3min7", beat * 2)
        
        # Test 3: Melodic Octave Jump (C4 -> G4 -> C5)
        m1 = inst.play("C4", beat)
        m2 = inst.play("G4", beat)
        m3 = inst.play("C5", beat)
        
        # Combine sections
        gap = np.zeros(int(AudioEngine.SAMPLE_RATE * 0.2)) # Tiny silence
        section = np.concatenate([chord1, chord2, gap, m1, m2, m3, gap])
        
        full_audio = np.concatenate([full_audio, section])

    # Final Master
    print("Mastering audio...")
    final = AudioEngine.normalize(full_audio)
    AudioEngine.save(final, "PyJam_Ultimate_Showcase")
    print("--- Test Complete! Check your folder for WAV and MP3 ---")

if __name__ == "__main__":
    run_mega_test()
