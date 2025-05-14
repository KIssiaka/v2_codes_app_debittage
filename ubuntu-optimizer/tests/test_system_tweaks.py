import unittest
from src.features.system_tweaks import SystemTweaks

class TestSystemTweaks(unittest.TestCase):

    def setUp(self):
        self.system_tweaks = SystemTweaks()

    def test_apply_tweaks(self):
        result = self.system_tweaks.apply_tweaks()
        self.assertTrue(result)

    def test_reset_tweaks(self):
        self.system_tweaks.apply_tweaks()  # Apply tweaks first
        result = self.system_tweaks.reset_tweaks()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()