import unittest
from package_aab.src import MySeq


class test_MySeq(unittest.TestCase):
    def setUp(self):
        self.seq_dna1 = MySeq("ACTGCCAT", "dna")
        self.seq_dna2 = MySeq("ATGCATGAAT", "dna")
        self.seq_dna3 = MySeq("ATGCCCGCTTT", "dna")
        self.seq_rna1 = MySeq("ACUGCCGUCAUA", "rna")
        self.seq_rna2 = MySeq("AGAAUGACGACCUAG", "rna")
        self.seq_prot1 = MySeq("MFLSP_AHMGREQTG_", "prot")

    def test_transcricao(self):
        x = self.seq_dna1.transcription()
        y = "ACUGCCAU"
        self.assertEqual(str(x), y)


    def test_reverseComplement(self):
        x = self.seq_dna1.reverseComplement()
        y = "ATGGCAGT"
        self.assertEqual(str(x), y)

    def test_rnaCodon(self):
        x = self.seq_rna1.rnaCodon()
        y = ["ACU", "GCC", "GUC", "AUA"]
        self.assertEqual(x, y)

    def test_seqTranslation(self):
        x = self.seq_dna3.seqTranslation()
        y = "MPA"
        self.assertEqual(str(x), y)

    def test_orfs(self):
        x = self.seq_dna2.orfs()
        y = ["MHE", "CMN", "A_", "IHA", "FMH", "SC"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

    def test_allProtein(self):
        x = self.seq_prot1.allProtein()
        y = ["MFLSP", "MGREQTG"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

    def test_longestProteinSeq(self):
        x = self.seq_prot1.longestProteinSeq()
        y = "MGREQTG"
        self.assertEqual(str(x), y)


if __name__ == '__main__':
    unittest.main()