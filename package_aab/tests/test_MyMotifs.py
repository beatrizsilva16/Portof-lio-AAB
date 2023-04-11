import unittest
from package_aab.src import MyMotifs
from package_aab.src import MySeq

class test_MyMotifs(unittest.TestCase):
    def setUp(self) -> None:
        self.seq1 = MySeq("AAAGTT", "dna")
        self.seq2 = MySeq("CACGTG", "dna")
        self.seq3 = MySeq("TTGGGT", "dna")
        self.seq4 = MySeq("GACCGT", "dna")
        self.seq5 = MySeq("AACCAT", "dna")
        self.seq6 = MySeq("AACCCT", "dna")
        self.seq7 = MySeq("AAACCT", "dna")
        self.seq8 = MySeq("GAACCT", "dna")
        self.lseqs = [self.seq1, self.seq2, self.seq3, self.seq4, self.seq5, self.seq6,
                      self.seq7, self.seq8]
        self.motifs = MyMotifs(self.lseqs)

    def test_mat_count(self):
        x = self.motifs.mat_count
        y = ["[4, 7, 3, 0, 1, 0]", "[1, 0, 4, 5, 3, 0]",
             "[2, 0, 1, 3, 2, 1]", "[1, 1, 0, 0, 2, 7]"]
        for test, truth in zip(x,y):
            self.assertEqual(str(test), truth)

    def test_pwm(self):
        x = self.motifs.pwm
        y = ["[0.5, 0.875, 0.375, 0.0, 0.125, 0.0]",
             "[0.125, 0.0, 0.5, 0.625, 0.375, 0.0]",
             "[0.25, 0.0, 0.125, 0.375, 0.25, 0.125]",
             "[0.125, 0.125, 0.0, 0.0, 0.25, 0.875]"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

    def test_consensus(self):
        x = self.motifs.consensus()
        y = "AACCCT"
        self.assertEqual(x, y)

    def test_maskedConsensus(self):
        x = self.motifs.maskedConsensus()
        y = "-A-C-T"
        self.assertEqual(x, y)


    def test_probabSeq(self):
        seq = "AAACCT"
        x = self.motifs.probabSeq(seq)
        y = "0.0336456298828125"
        self.assertEqual(str(x), y)

    def test_probAllPosition(self):
        seq = "AAACCT"
        x = self.motifs.probAllPositions(seq)
        y = "[0.0336456298828125]"
        self.assertEqual(str(x), y)

    def test_mostProbableSeq(self):
        seq = "CTATAAACCTTACATC"
        x = self.motifs.mostProbableSeq(seq)
        y = "4"
        self.assertEqual(str(x), y)



if __name__ == '__main__':
    unittest.main()