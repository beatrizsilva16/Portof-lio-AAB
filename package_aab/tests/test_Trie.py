import unittest
from package_aab.src.Trie import Trie


class TestTrie(unittest.TestCase):
    def test_insert(self):
        node = Trie("AAA AAG ACTT")
        self.assertRaises(TypeError, node.check_seqs, ["dps"])
        self.assertRaises(TypeError, node.check_seqs, True)
        self.assertRaises(TypeError, node.check_seqs, 284)

    def test_matches(self):
        node = Trie("AAA AAG ACTT")
        self.assertEqual(node.matches("AAA"), True)
        self.assertEqual(node.matches("TTT"), False)

    def test_insert_single_sequence(self):
        node = Trie("AAA AAG ACTT")
        node.insert("AAA")
        self.assertEqual(node.matches("AAA"), True)

    def test_insert_multiple_sequences(self):
        node = Trie("AAA AAG ACTT")
        node.insert("AAA")
        node.insert("AAG")
        node.insert("ACTT")
        self.assertEqual(node.matches("AAA"), True)
        self.assertEqual(node.matches("AAG"), True)
        self.assertEqual(node.matches("ACTT"), True)


if __name__ == '__main__':
    unittest.main()