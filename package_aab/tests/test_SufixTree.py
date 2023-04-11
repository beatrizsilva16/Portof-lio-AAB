import unittest
from suffix_tree import SuffixTree

class test_SuffixTree(unittest.TestCase):
    def setUp(self):
        self.seq = "TACTA"
        self.suffixtree = SuffixTree()
        self.suffixtree.suffixTreeFromSeq(self.seq)


class test_SuffixTreeMethods(test_SuffixTree):

    def test_findPattern(self):
        x = self.suffixtree.findPattern("TA")
        y = '[0, 3]'
        self.assertEqual(str(x), y)

    def test_doesntFindPattern(self):
        x = self.suffixtree.findPattern("ACG")
        y = 'None'
        self.assertEqual(str(x), y)

if __name__ == '__main__':
    unittest.main()