"""
@author: miguelrocha
"""


def createMatZeros(line_n: int, col_n: int) -> list:

    """
    Method to create a matrix of zeros
    :param line_n: number of lines of the matrix
    :param col_n: number of columns of the matrix
    :return: matrix of zeros
    """

    mat_zeros = []  #lista vazia para criar matriz de zeros
    for i in range(0, line_n): #por cada linha de zero ao número de linhas desejado
        mat_zeros.append([0]*col_n) #adiciona um zero col_n vezes
    return mat_zeros


def printMat(mat: list):
    """
    Method to print the matrix
    :param mat: matrix to print
    """
    for lin in range(len(mat)):
        for col in range(len(mat[lin])):
            print(mat[lin][col], end='')
        print()


class MyMotifs:
    """
    Class presenting methods that allow the manipulation and search of recurrent patterns (motifs)
    in biological sequences and the realization of probabilistic pattern matrices (PWM).
    """

    def __init__(self, seqs: list = [], pwm: list = [], alphabet: str = None):
        """
        Method that stores the values used in the rest of the methods
        :param seqs: list of sequences of introduced sequencias
        :param pwm: matrix of prob
        :param alphabet: type of caracters of the sequence introduced
        """

        if seqs:  # se for uma sequencia, então:
            self.size = len(seqs[0]) #comprimento dos carateres da sequência
            self.seqs = seqs  # objetos classe MySeq
            self.alphabet = seqs[0].alphabet() #objeto da classe Myseq, verifica o tipo
            self.doCounts() #cria a matriz de contagens dos caractéres das sequências
            self.createPWM() #cria a matriz de PWN (matriz de probabilidades)

        else: # se for uma PWM
            self.pwm = pwm
            self.size = len(pwm[0])
            self.alphabet = alphabet #tipo de carateres da sequencia introduzida

    def __len__(self):
        """
        Method that returns the length of the sequences
        """
        return self.size

    def doCounts(self):
        """
        Method that implements the matrix of counts
        """
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for seq in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(seq[i])
                self.counts[lin][i] += 1

    def createPWM(self) -> None:
        """
        Method that creates the probabilistic matrix. PWMs are probabilistic representations of the characters
        in biological sequences, i.e. it calculates the probability of nucleotide i being found at position j
        :return:
        """
        if self.counts == None:
            self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)

    def consensus(self) -> str:
        """
        Method that generates a consensus sequence. Consensus sequences store the most conserved characters in each
        in each position of the pattern, that is, the highest value of each column of the count array.
        :return: string of the consensus sequence.
        """
        consenso_seq = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            consenso_seq += self.alphabet[maxcoli]
        return consenso_seq

    def maskedConsensus(self) -> str:
        """
        Method that generates the consensus sequence that is obtained with the characters
        that have an incidence higher than 50%
        :return: string of the consensus sequence with an incidence higher than 50%.
        """
        consenso_seq = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                consenso_seq += self.alphabet[maxcoli]
            else:
                consenso_seq += "-"
        return consenso_seq

    def probabSeq(self, seq: str) -> float:
        """
        Method that calculates the probability of a pattern being found in a sequence
        :param seq: introduced sequence
        :return: the probability of a pattern being found in the sequence
        """
        prob = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            prob *= self.pwm[lin][i]
        return prob

    def probAllPositions(self, seq: str) -> list:
        """
        Method implemented to calculate the probability of finding patterns in longer sequences
        and calculate the probability of the pattern occurring at each character in the sequence, ie,
        of occurring at each sub-sequence of the pattern size.
        :param seq: introduced sequence
        :return: list of probabilities of the pattern occurring at each subsequence
        """
        sub_prob = []
        for _ in range(len(seq)-self.size+1):
            sub_prob.append(self.probabSeq(seq))
        return sub_prob

    def mostProbableSeq(self, seq: str) -> int:
        """
        Method implemented to determine the sub-sequence with the highest probability of matching
        the pattern in search.
        :param seq: introduced sequence
        :return: index of the sub-sequence with the highest probability of matching the pattern in demand
        """
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k + self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind
