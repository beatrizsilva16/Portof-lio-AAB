import unittest
from package_aab.src.EAMotifs import EAMotifsInt


class TestEAMotifsInt(unittest.TestCase):
    def test_run(self):
        ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
        ea.run()
        best_fitness = ea.getBestFitness()
        self.assertIsNotNone(best_fitness)
        self.assertGreater(best_fitness, 0)

if __name__ == '__main__':
    unittest.main()

import unittest
from package_aab.src.EAMotifs import EAMotifsReal


class TestEAMotifsReal(unittest.TestCase):
    def test_run(self):
        ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt", 2)
        ea.run()
        best_fitness = ea.getBestFitness()
        self.assertIsNotNone(best_fitness)
        self.assertGreater(best_fitness, 0)

if __name__ == '__main__':
    unittest.main()
