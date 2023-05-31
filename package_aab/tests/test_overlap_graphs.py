import unittest
from package_aab.src.Overlap_graphs import OverlapGraph


class test_OverlapGraph(unittest.TestCase):
    def setUp(self):
        frag = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        self.gr = OverlapGraph(frag, True)

    def test_validPath(self):
        path = ["ACC-2", "CCA-8", "CAT-5", "ATG-3", "TGG-13", "GGC-10", "GCA-9", "CAT-6", "ATT-4", "TTT-15", "TTC-14",
               "TCA-12", "CAT-7", "ATA-1", "TAA-11"]
        x = self.gr.check_if_valid_path(path)
        y = True
        self.assertEqual(x, y)



if __name__ == "__main__":
    unittest.main()