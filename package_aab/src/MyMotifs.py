
"""
Class: MyMotifs
"""


def createMatZeros(line_num: int, col_num: int) -> list:
    """
    Method that creates the matrix of zeros.
    The matrix of zeros is used as a base to store the counts or probabilities
    of each character in each position of the biological sequences that
    are being analyzed.
    :param line_num: number of lines in the matrix
    :param col_num: number of columns in the matrix
    :return: matrix of zeros
    """
    mat_z = []  # empty list to create the matrix of zeros
    for i in range(0, line_num):  # por cada linha de zero ao número de linhas desejado
        mat_z.append([0]*col_num)  # add a zero * col_num
    return mat_z


def printMat(mat: list):
    """
    Method to print the matrix
    :param mat: matrix to print
    """
    for lin in range(len(mat)):
        for col in range(len(mat[lin])):
            print(mat[lin][col], end=' ')
        print()


class MyMotifs:
    """
    Class that presents the methods that allow the manipulation and search of recurring patterns (motifis)
    in biology sequences and do PWM.
    """

    def __init__(self, lseqs: list = [], pwm: list = [], alphabet: str = None):
        """
        Method that keeps the values used in the methods
        :param lseqs: list of sequences introduced
        :param pwm:  probability matrix
        :param alphabet: type of caracters of the sequence introduced
        """
        if lseqs:  # if the parameter introduced is a sequence, it must have the following instances.
            self.size = len(lseqs[0])  # character length of the sequences
            self.seqs = lseqs  # objects of class MySeq
            self.alphabet = lseqs[0].alphabet()  # object of class Myseq, checks the type
            self.doCounts()  # creates the matrix of counts of the characters of the sequences
            self.createPWM()  # creates the PWN matrix (probability matrix)
        else:  # if the parameter introduced is not a sequence it is a PWM
            self.pwm = pwm
            self.size = len(pwm[0])  # length of the first value in the list
            self.alphabet = alphabet  # character type of the sequence entered

    def __len__(self):
        """
        Method that returns the length of the sequence
        """
        return self.size

    def doCounts(self):
        """
        Method that implements the counting matrices.
        """
        self.mat_count = createMatZeros(len(self.alphabet), self.size)  # define uma instância correspondente
        # à matriz probabilística, em que o número de linhas é o número de caracteres do alfabeto e o número
        # de colunas é o comprimento da sequência.
        for seq in self.seqs:  # para cada sequência na lista de sequências
            for i in range(self.size):  # para cada índice da sequência
                lin = self.alphabet.index(seq[i])  # as linhas da matriz correspondem à ordem dos caracteres no alfabeto
                self.mat_count[lin][i] += 1  # increment the count of the character at position i and row lin
                                             # in the counting matrix.

    def createPWM(self) -> None:
        """
        Method that creates the probabilistic matrix. PWMs are probabilistic representations of the characters
        in biological sequences. It calculates the probability of nucleotide i being found at position j.
        """
        if self.mat_count == None:  # if the matrix of counts is not done
            self.doCounts()  # do the matrix of counts
        self.pwm = createMatZeros(len(self.alphabet), self.size)  # creates the matrix of zeros to structure the PWM
        for i in range(len(self.alphabet)):  # percorre o tipo de caracteres da sequência
            for j in range(self.size):  # percorre a sequência
                self.pwm[i][j] = float(self.mat_count[i][j]) / len(self.seqs)
                # calculates the probability for each cell using the formula:
                # counts checked / number of sequences.

    def consensus(self) -> str:
        """
        Method that generates a consensus sequence. Consensus sequences store the most conserved characters in each
        position of the pattern, that is, the highest value of each column of the count matrix.
        :return: string of the consensus sequence.
        """
        cons_seq = ""  # opens an empty string to enter the sequence of characters
        for j in range(self.size):  # runs through the columns of the matrix that have the same length as the sequence
            max_col = self.mat_count[0][j]  # stores the value of the first row of column j
            index_maxval = 0  # sets as initial value
            for i in range(1, len(self.alphabet)):  # runs all lines, i.e,
                # the characters of the sequence type
                if self.mat_count[i][j] > max_col:  # if the count value is greater than the last saved value
                    max_col = self.mat_count[i][j]  # returns it
                    index_maxval = i  # stores the index of the character with the highest count value
            cons_seq += self.alphabet[index_maxval]  # adds to the string the character
        return cons_seq

    def maskedConsensus(self) -> str:
        """
        Method that generates the consensus sequence that is obtained with the characters
        that have an incidence higher than 50%.
        :return: string of the consensus sequence with incidence higher than 50%.
        """
        cons_seq = ""  # opens an empty string to enter the sequence of characters
        for j in range(self.size):  # runs through the columns of the matrix that have the same length as the sequence
            max_col = self.mat_count[0][j]  # returns the value of the first row of column j
            index_maxval = 0  # sets as initial value
            for i in range(1, len(self.alphabet)):  # percorre todas as linhas, ou seja,
                # os caracteres do tipo de sequência
                if self.mat_count[i][j] > max_col:  # se o valor da contagem for superior ao último valor guardado
                    max_col = self.mat_count[i][j]  # devolve o valor em causa
                    index_maxval = i  # guarda o index do caractér com maior valor de contagem
            if max_col > len(self.seqs) / 2:  # se o valor máximo da coluna for superior a metade do número de sequências
                cons_seq += self.alphabet[index_maxval]  # devolve o caractér
            else:
                cons_seq += "-"  # se não tiver uma incidência superior a 50% não devolve um caracter
        return cons_seq

    def probabSeq(self, seq: str) -> float:
        """
        Method that calculates the probability of a pattern being found in a sequence.
        :param seq: sequence intoduced
        :return: the probability of a pattern being found in the sequence
        """
        prob = 1.0  # sets the initial probability to 1
        for i in range(self.size):  # runs the sequence from zero to the length of the sequences entered
            lin = self.alphabet.index(seq[i])  # the lines of the matrix correspond to the order of the characters in the alphabet
            prob *= self.pwm[lin][i]  # multiplies the cell value by the initially set value
        return prob

    def probAllPositions(self, seq: str) -> list:
        """
        Method implemented to calculate the probability of finding patterns in longer sequences
        and calculate the probability of the pattern occurring at each character in the sequence, ie,
        of occurring at each sub-sequence of the pattern size. For example, if the pattern size is 3 and the sequence is
        "ATCGTACG", the method would calculate the probability of the pattern occurring at each of the sub-sequences of
        size 3, which are "ATC", "TCG", "CGT", "GTA", "TAC", "ACG".
        :param seq: sequence introduced
        :return: list of probabilities of the pattern occurring at each subsequence
        """
        subseq_prob = []  # empty list to return probabilities
        for i in range(len(seq)-self.size + 1):  # runs through the entered sequence minus the length of the pattern
            # plus one, in order to scroll the entire sequence until a match is reached
            subseq_prob.append(self.probabSeq(seq))  # add the prob to the list
        return subseq_prob

    def mostProbableSeq(self, seq: str) -> int:
        """
        Method implemented to determine the sub-sequence with the highest probability of matching
        the pattern being searched.
        :param seq: sequence introduced
        return: the index of the sub-sequence with higher probability of matching the pattern in search.
        """
        max_p = - 1.0  # defines the minimum probability, which is a value that is lower than any probability that
        # can be obtained.This is done to ensure that the first calculated probability will be greater than max_p and
        # will be used to update max_p and max_ind.
        max_ind = - 1  # sets the initial value for the index with the highest probability
        for k in range(len(seq)-self.size):  # runs through the entire sequence minus the length of the pattern
            p = self.probabSeq(seq[k:k + self.size])  # calculates the probability of finding the corresponding sub-sequence
            # da posição k à posição k + o comprimento da
            if (p > max_p):  # se a probabilidade for superior a - 1.0
                max_p = p  # define p como a probabilidade máxima
                max_ind = k  # define o índice atual como o índice com o valor máximo de probabilidade
        return max_ind