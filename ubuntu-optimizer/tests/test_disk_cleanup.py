import unittest
from src.features.disk_cleanup import DiskCleaner

class TestDiskCleaner(unittest.TestCase):

    def setUp(self):
        self.disk_cleaner = DiskCleaner()

    def test_clean_disk(self):
        # Assuming clean_disk returns a success message
        result = self.disk_cleaner.clean_disk()
        self.assertIn("Disk cleanup completed", result)

    def test_analyze_disk_usage(self):
        # Assuming analyze_disk_usage returns a dictionary with usage stats
        result = self.disk_cleaner.analyze_disk_usage()
        self.assertIsInstance(result, dict)
        self.assertIn("total_space", result)
        self.assertIn("used_space", result)
        self.assertIn("free_space", result)

if __name__ == '__main__':
    unittest.main()