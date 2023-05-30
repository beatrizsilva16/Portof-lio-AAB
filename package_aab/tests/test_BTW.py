import unittest
from package_aab.src.BWT import BWT


class test_BWT(unittest.TestCase):
    def setUp(self):
        self.bwt = BWT("TAGACAGAGA$")

class test_BWtMethods(test_BWT):
    def test_runTest(self):
        x = self.bwt.bwt
        y = "AGGGTCAAAA$"
        self.assertEqual(x, y)

    def test_lastToFirst(self):
        x = self.bwt.last_to_first()
        y = [1, 7, 8, 9, 10, 6, 2, 3, 4, 5, 0]
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()