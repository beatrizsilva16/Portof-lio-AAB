import unittest

from package_aab.src import Automata

# States:  4
# Alphabet:  AC
# Transition table:
# 0 , A  ->  1
# 0 , C  ->  0
# 1 , A  ->  1
# 1 , C  ->  2
# 2 , A  ->  3
# 2 , C  ->  0
# 3 , A  ->  1
# 3 , C  ->  2
# [0, 0, 1, 2, 3, 1, 2, 3, 1]
# [1, 4]


class TestAutomata(unittest.TestCase):

    def setUp(self):
        self.numstates = 4
        self.alphabet = "AC"
        self.pattern = "ACA"
        self.automata = Automata(self.alphabet, self.pattern)


    def test_buildTransitionTable(self):
        expected_table = {
            (0, 'A'): 1,
            (0, 'C'): 0,
            (1, 'A'): 1,
            (1, 'C'): 2,
            (2, 'A'): 3,
            (2, 'C'): 0,
            (3, 'A'): 1,
            (3, 'C'): 2

        }
        self.assertEqual(self.automata.transitionTable, expected_table)

    def test_applyNextState(self):
        seq = "CACAACAA"
        expected_states = [0, 0, 1, 2, 3, 1, 2, 3, 1]
        self.assertEqual(self.automata.applyNextState(seq), expected_states)

    def test_patternSeqPosition(self):
        seq = "CACAACAA"
        expected_positions = [1, 4]
        self.assertEqual(self.automata.patternSeqPosition(seq), expected_positions)

if __name__ == '__main__':
    unittest.main()
