import unittest
from package_aab.src.SuffixTree import SuffixTree


class test_SuffixTree(unittest.TestCase):
    def setUp(self):
        self.seq = "TACTA"
        self.suffixtree = SuffixTree("TACTA")
        self.suffixtree.suffix_tree_from_seq(self.seq)


class test_SuffixTreeMethods(test_SuffixTree):
    def test_findPattern(self):
        x = self.suffixtree.find_pattern("TA")
        y = '[0, 3]'
        self.assertEqual(str(x), y)

    def test_doesntFindPattern(self):
        x = self.suffixtree.find_pattern("ACG")
        y = 'None'
        self.assertEqual(str(x), y)


if __name__ == '__main__':
    unittest.main()