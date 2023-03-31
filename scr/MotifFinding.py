
from MySeq import MySeq
from scr.MyMotifs import MyMotifs
from random import randint
from random import random
from typing import Union
from typing import List

class MotifFinding:
    """
    Class implemented for searching for recurrent patterns in a biological sequence,
    that can be DNA or proteins.
    The pattern to look for can be an exact sequence or a degenerate consensus in which there are
    ambiguous characters.
    """

    def __init__(self, size: int = 8, seqs=None) -> None:
        """
        Method storing the values used in the other methods.
        :param size: size of the motif to search
        :param seqs: list of sequences to search
        """
        self.motifSize = size #guarda o tamanho
        if (seqs != None): # se a lista tiver sequencias
            self.seqs = seqs
            self.alphabet = seqs[0].alphabet()
        else:
            self.seqs = []

    def __len__(self) -> int:
        """
        Method returning the length of sequences
        :return: returns the length of sequences
        """
        return len(self.seqs)

    def __getitem__(self, n: int) -> None:
        """
        Method that allows returning an item from the indexing of an instance
        :param n: position of the value we want to return.
        :return: characteristic of the position entered
        """
        return self.seqs[n]

    def seqSize(self, i: int) -> int:
        """
        Method returning the length of the sequence
        :param i: index of the sequence in the sequence list.
        :return: length of the sequence with index i from the sequence list.
        """
        return len(self.seqs[i])

    def readFile(self, file: str, type: str) -> None:
        """
        Method that reads the sequence file.
        :param file: sequence file.
        :param type: type of the sequences.
        """
        for seq in open(file, "r"):
            self.seqs.append(MySeq(seq.strip().upper(), type))
        self.alphabet = self.seqs[0].alphabet()

    def createMotifFromIndexes(self, indexes: List):
        """
        Method implementing probabilistic motifs of the MyMotif type.
        :param indexes: list of the indexes of the starting positions of the motif
        :return: of the sub-sequences used to create the motif.
        """
        motif_subseq = []
        for i, ind in enumerate(indexes):
            motif_subseq.append(
                MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo))
        return MyMotifs(motif_subseq)

    # SCORES

    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score += maxcol
        return score

    def scoreMult(self, s):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score *= maxcol
        return score

    # EXHAUSTIVE SEARCH

    def nextSol(self, s):
        nextS = [0]*len(s)
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0):
            nextS = None
        else:
            for i in range(pos):
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS

    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0] * len(self.seqs)
        while (s != None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res

    # BRANCH AND BOUND

    def nextVertex(self, s):
        res = []
        if len(s) < len(self.seqs):  # internal node -> down one level
            for i in range(len(s)):
                res.append(s[i])
            res.append(0)
        else:  # bypass
            pos = len(s)-1
            while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0:
                res = None  # last solution
            else:
                for i in range(pos):
                    res.append(s[i])
                res.append(s[pos]+1)
        return res

    def bypass(self, s):
        res = []
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0:
            res = None
        else:
            for i in range(pos):
                res.append(s[i])
            res.append(s[pos]+1)
        return res

    def branchAndBound(self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore:
                    s = self.bypass(s)
                else:
                    s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)

    def heuristicConsensus(self):
       pass

    # heuristic stochastic

    def heuristicStochastic(self):
        pass

    # gibbs sampling

    def gibbs(self, numits):
        pass

    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f:
            tot += (0.01+x)
        #tot = sum(f)
        # if tot == 0: return 0
        val = random() * tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1
