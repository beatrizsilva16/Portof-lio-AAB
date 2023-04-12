from typing import List


class BoyerMoore:
    def __init__(self, alphabet=str, pattern=str):
        """
        Class to implement the BoyerMoore algorithm, governed by two rules: Bad Caracter
        rule and Good Suffix Rule.
        :param alphabet: alphabet of the sequence/text to analyze. In the bioinformatics field,
        they are typically nucleotide bases nucleotides.
        :param pattern: pattern to find.
        """
        self.alphabet = alphabet
        self.pattern = pattern

        self.occ = {}  # creates an empty dictionary to store the character occurrence

        # # create lists of size equal to the default + 1. each initialized with zeros
        self.f = [0] * (len(self.pattern) + 1)  # list of size of pattern + 1, initialized with zeros
        self.s = [0] * (len(self.pattern) + 1)  # list of the size of the pattern + 1, initialized with zeros

        # calls the methods for processing the Bad Character rule and the Good Suffix Rule
        self.process_bcr()
        self.process_gsr()

    def process_bcr(self):
        """
        Bad Character rule implementation.
        Method where a dictionary is created with all possible symbols (occ) as keys, and the values define
        the rightmost position at which the symbol appears in the pattern (-1 means it does not occur). This allows you to
        quickly calculate the number of positions to follow to search according to the mismatch in the pattern (value for
        the symbol in the dictionary). Note that this value can be negative, meaning that the rule in this case
        is not useful and is ignored in the next iteration.
        """
        for s in self.alphabet:  # to each character in the alphabet:
            self.occ[s] = -1  # assign the value -1 in the dictionary for each character. key s and value -1
        for j in range(0, len(self.pattern)):  # for each index (j) between 0 and the size of the pattern:
            c = self.pattern[j]  #
            self.occ[c] = j  # look up entry in dictionary and update value to index j

    def process_gsr(self):
        """
        Good Suffix rule implementation.
        Calculates the value of the f list (the length of the longest proper suffix that matches the suffix of the pattern),
        and s list (the length of the longest proper suffix that matches the prefix of the pattern).
        """
        i = len(self.pattern)  # assign i the size of the pattern
        j = len(self.pattern) + 1  # assign j the size of the pattern +1

        self.f[i] = j  # changes the last element of the list f to the value of f
        while i > 0:  # while covering the size of the pattern
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]: # as long as j is less than or equal
                # the size of the pattern and pattern[i-1] and pattern[j-1] are different
                # will set list s, in S which means the number of squares that can be advanced if it doesn't fit the pattern
                if self.s[j] == 0:  # if the value of the list is 0 at index j:
                    self.s[j] = j - i  # for this index subtract the value of pattern size+1 - iteration in pattern(i)
                j = self.f[j]  #
            i -= 1  # reducing value of i and j for iteration
            j -= 1
            self.f[i] = j
        j = self.f[0]

        for i in range(0, len(self.pattern)):  # # when it's set to 0 change to the value of j most recently that
            # means to pass the rest of the string
            # for each i between 0 and the size of the pattern:
            if self.s[i] == 0:  # if the value of s[i] is equal to 0:
                self.s[i] = j  # new value of s[i] becomes j
            if i == j:
                j = self.f[j]

    def search_pattern(self, text=str) -> List[int]:
        """
        This method allows to find a pattern in a given text, based on the object of the class that contains the
        pattern and its alphabet.
        :param text: string of the text where we want to look for our pattern
        :return: list with the indexes where the pattern starts
        """
        i = 0  # sets the start position to zero
        res = []  # empty results list
        while i <= (len(text) - len(self.pattern)):  # to start running the sequence and as long as the position in the seq
            # does not exceed the search grid limit
            j = len(self.pattern) - 1  # sets the size of the pattern
            while (j >= 0) and (self.pattern[j] == text[j+i]):  # continue the cycle while giving match
                # (right to left)
                j -= 1
            if j < 0:  # if j to -1 (complete departure)
                res.append(i)
                i = i + self.s[0]  # to move forward i positions as j<0 means it has matched with a pattern
            else:
                c = text[j+i]  # missmatch character
                i += max(self.s[j+1], (j-self.occ[c]))  # advance a sequence depending on the GSR and BCR
        return res