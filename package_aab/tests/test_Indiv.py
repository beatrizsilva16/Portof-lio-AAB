import unittest
from package_aab.src import Indiv

class TestIndiv(unittest.TestCase):

    def setUp(self):
        self.lb = 0
        self.ub = 1
        self.size = 10
        self.indiv = Indiv(self.size, lb=self.lb, ub=self.ub)

    def test_initRandom(self):
        indiv = Indiv(self.size, lb=self.lb, ub=self.ub)
        genes = indiv.getGenes()
        self.assertEqual(len(genes), self.size)
        for gene in genes:
            self.assertGreaterEqual(gene, self.lb)
            self.assertLessEqual(gene, self.ub)

    def test_mutation(self):
        indiv = Indiv(self.size, lb=self.lb, ub=self.ub)
        old_genes = indiv.getGenes()
        indiv.mutation()
        new_genes = indiv.getGenes()
        self.assertEqual(len(old_genes), len(new_genes))
        self.assertListEqual(sorted(old_genes), sorted(new_genes))

    def test_crossover(self):
        indiv1 = Indiv(self.size, lb=self.lb, ub=self.ub)
        indiv2 = Indiv(self.size, lb=self.lb, ub=self.ub)
        offspring1, offspring2 = indiv1.crossover(indiv2)
        self.assertIsInstance(offspring1, Indiv)
        self.assertIsInstance(offspring2, Indiv)
        self.assertEqual(len(offspring1.getGenes()), self.size)
        self.assertEqual(len(offspring2.getGenes()), self.size)

if __name__ == '__main__':
    unittest.main()
