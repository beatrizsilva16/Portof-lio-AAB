import unittest
from package_aab.src import EvolAlgorithm


class TestEvolAlgorithm(unittest.TestCase):

    def test_ea_run(self):
        # Test the evolutionary algorithm with the specified parameters
        ea = EvolAlgorithm(100, 20, 50, 10)
        ea.run()

        # Assert that the best solution has 10 genes
        self.assertEqual(len(ea.bestsol.getGenes()), 10)

        # Assert that the best fitness is greater than or equal to 1.0
        self.assertGreaterEqual(ea.bestsol.getFitness(), 1.0)


if __name__ == '__main__':
    unittest.main()
