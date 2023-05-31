import unittest
from package_aab.src.debrujin import DeBruijnGraph


class test_DeBruijnGraph(unittest.TestCase):
    def setUp(self):
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC",
                 "TTT"]
        self.debruijn = DeBruijnGraph(frags)

    def test_balancedGraph(self):
        x = self.debruijn.check_nearly_balanced_graph()
        y = ("AC", "AA")
        self.assertEqual(x, y)

    def test_eulerianPath(self):
        x = self.debruijn.eulerian_path()
        y = ["AC", "CC", "CA", "AT", "TT", "TT", "TC", "CA", "AT", "TG", "GG", "GC", "CA", "AT", "TA", "AA"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)


if __name__ == "__main__":
    unittest.main()