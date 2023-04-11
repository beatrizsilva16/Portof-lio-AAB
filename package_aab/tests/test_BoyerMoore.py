import unittest
from package_aab.src.BoyerMoore import BoyerMoore


class TestBoyerMoore(unittest.TestCase):

    def setUp(self):
        alphabet = 'ACTG'
        pattern = 'ACCA'
        self.boyermoore = BoyerMoore(alphabet, pattern)

    def test_search_pattern(self):
        x = self.boyermoore.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        y = [5, 13, 23, 37]
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()