from package_aab.src.MySeq import MySeq
from package_aab.src.MotifFinding import MotifFinding
from unittest import TestCase


class TestMotifFinding(TestCase):

    def test_score(self):
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(mf.score([20, 25, 45, 50, 37]), 19)
        self.assertEqual(mf.score([57, 1, 5, 25, 0]), 20)
        self.assertEqual(mf.score([1, 20, 50, 5, 2]), 24)
        self.assertEqual(mf.score([60, 35, 9, 10, 40]), 20)
        self.assertEqual(mf.score([52, 40, 9, 7, 1]), 19)

    def test_score_mult(self):
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(mf.scoreMult([20, 25, 45, 50, 37]), 0.0022118400000000005)
        self.assertEqual(mf.scoreMult([57, 1, 5, 25, 0]), 0.002949120000000001)
        self.assertEqual(mf.scoreMult([1, 20, 50, 5, 2]), 0.014929919999999998)
        self.assertEqual(mf.scoreMult([60, 35, 9, 10, 40]), 0.0033177600000000003)
        self.assertEqual(mf.scoreMult([52, 40, 9, 7, 1]), 0.00221184)

    def test_exhaustive_search(self):
        mf = MotifFinding(3, [MySeq("ATAGAGCTGA", "dna"), MySeq("ACGTAGATGA", "dna"), MySeq("AAGATAGGGG", "dna")])
        self.assertEqual(mf.exhaustiveSearch(), [1, 3, 4])

    def test_branch_and_bound(self):
        mf = MotifFinding(3, [MySeq("ATAGAGCTGA", "dna"), MySeq("ACGTAGATGA", "dna"), MySeq("AAGATAGGGG", "dna")])
        self.assertEqual(mf.branchAndBound(), [1, 3, 4])
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(mf.branchAndBound(), [52, 40, 9, 7, 1])

    def test_consensus(self):
        mf = MotifFinding(3, [MySeq("ATAGAGCTGA", "dna"), MySeq("ACGTAGATGA", "dna"), MySeq("AAGATAGGGG", "dna")])
        sol = [1, 3, 4]
        consensus_result = mf.createMotifFromIndexes(sol).consensus()
        self.assertEqual(str(consensus_result), "TAG")

    def test_heuristicConsensus(self):
        mf = MotifFinding(3, [MySeq("ATAGAGCTGA", "dna"), MySeq("ACGTAGATGA", "dna"), MySeq("AAGATAGGGG", "dna")])
        sol = mf.heuristicConsensus()
        x = mf.score(sol)
        y = "9"
        self.assertEqual(str(x), y)

