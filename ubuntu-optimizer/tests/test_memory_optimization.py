import unittest
from src.features.memory_optimization import MemoryOptimizer

class TestMemoryOptimizer(unittest.TestCase):

    def setUp(self):
        self.memory_optimizer = MemoryOptimizer()

    def test_optimize_memory(self):
        initial_usage = self.memory_optimizer.check_memory_usage()
        self.memory_optimizer.optimize_memory()
        optimized_usage = self.memory_optimizer.check_memory_usage()
        self.assertLess(optimized_usage, initial_usage, "Memory usage should decrease after optimization.")

    def test_check_memory_usage(self):
        usage = self.memory_optimizer.check_memory_usage()
        self.assertIsInstance(usage, float, "Memory usage should be a float value.")

if __name__ == '__main__':
    unittest.main()