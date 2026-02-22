import unittest
from pyjam import Piano, AudioEngine

class TestPyJam(unittest.TestCase):
    def test_freq_calc(self):
        # A4 should always be 440Hz
        self.assertEqual(AudioEngine.get_freq("A4"), 440.0)

    def test_audio_length(self):
        piano = Piano()
        clip = piano.play("C4", 1.0)
        # Length should match sample rate
        self.assertEqual(len(clip), 44100)

if __name__ == '__main__':
    unittest.main()
