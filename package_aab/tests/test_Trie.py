import unittest
from package_aab.src import Trie

class test_Trie(unittest.TestCase):
    def setUp(self) -> None:
        self.pat = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
        self.trie = Trie()
        self.trie.trieFromPatterns(self.pat)


class test_TrieMethods(test_Trie):

    def test_prefixTrieMatch(self):
        x = self.trie.prefixTrieMatch("GAGATCCTA")
        y = "GAGAT"
        self.assertEqual(x, y)

    def test_trieMatches(self):
        x = self.trie.trieMatches("GAGATCCTA")
        y = ["(0, 'GAGAT')", "(2, 'GAT')", "(4, 'TC')", "(5, 'CCTA')"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

if __name__ == '__main__':
    unittest.main()