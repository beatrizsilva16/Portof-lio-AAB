from typing import List


class BWT:
    """
    Class for implementing the Burrows-Hweeler algorithm. The algorithm is useful for
    compressing large sequences, thus reducing their space. Moreover, it is possible to find patterns in the
    compression format efficiently.
    """
    def __init__(self, seq='', buildsufarray=False, sa=None):
        self.seq = seq
        self.check_seqs()
        self.bwt = self.build_bwt(seq, buildsufarray)
        self.sa = sa

    def check_seqs(self):
        """
        Method that checks if the sequence introduced is a string
        :return:
        """
        if not isinstance(self.seq, str):
            raise TypeError("The sequence introduced must be a string.")

    def set_bwt(self, bw):
        """
        Method that sets the BWT string directly for a BTW instance. It is useful in scenarios where we
        have a precomputed BWT string and want to assign it to the bwt attribute of the BWT instance
        without recomputing it using the build_bwt method.
        :param bw:
        :return:
        """
        self.bwt = bw  # Set the BWT string attribute

    def build_bwt(self, text, buildsufarray=False) -> str:
        """
        Method that generates rotations of the text and sorts them to construct the BWT string.
        :param text:
        :param buildsufarray:
        :return:
        """
        # Number of rotations (iterations) is equal o len(text)
        # Removes the first character to the end, and the suffix is added to ls
        ls = [text[i:] + text[:i] for i in range(len(text))]  # list comprehension for rotations
        ls.sort()  # sort them
        # Number of rotations (iterations) is equal o len(text)
        # Construct the BWT string by taking the last character of each rotation
        res = ''.join(ls[i][len(text) - 1] for i in range(len(text)))  # simplified BWT calculation
        #  if buildsufarray is True:
        if buildsufarray:
            self.sa = [len(text) - ls[i].index("$") - 1 for i in range(len(ls))]
        return res

    # implementation of recovery of the original BWT sequence
    def inverse_bwt(self) -> str:
        """
        Method recovers the original sequence from its BWT.
        :return: string of the original sequence
        """
        #  get the first column of the BWT matrix
        firstcol = self.get_first_col()
        #  initialize an empty string to store the result
        res = ""
        #  set the initial character to '$' (end-of-string marker)
        c = "$"
        #  initialize the occurrence count to 1
        occ = 1
        #  iterate over each character in the BWT string
        for i in range(len(self.bwt)):
            #  find the position of the current character (c) in the first column
            pos = self.findithocc(self.bwt, c, occ)
            #  update the current character (c) to the character at position (pos) in the first column
            c = firstcol[pos]
            #  reset the occurrence count to 1
            occ = 1
            #  search for the previous occurrences of the current character (c) in the first column
            k = pos - 1
            while k >= 0 and firstcol[k] == c:
                occ += 1
                k -= 1
            #  append the current character (c) to the result
            res += c
        #  return the recovered original sequence
        return res

    # implementation of search of patterns from BWT
    def last_to_first(self) -> List:
        """
        Creates a list mapping each character in the BWT sequence to its corresponding index in the first column.
        :return: list of indices
        """
        # initializes an empty list called res, which will store the indices.
        res = []
        firstcol = self.get_first_col()
        for i in range(len(firstcol)):
            c = self.bwt[i]
            # counts the number of occurrences of c in the BWT sequence up to index i,
            # adds 1 to account for the current occurrence, and assigns the result to the variable ocs
            ocs = self.bwt[:i].count(c) + 1
            val = self.findithocc(firstcol, c, ocs)
            res.append(val)
        return res

    def get_first_col(self) -> List[str]:
        """
        Method that recovers the first column of BWT sequence.
        The first column correspond the BWT sequence sorted.
        :return: first column of Matrix M
        """
        primeira_col = sorted(self.bwt)
        return primeira_col

    def bw_matching(self, pattern=str) -> List[int]:
        """
        Method for searching for patterns from BWT sequence
        :param pattern: pattern to search
        :return: list of matches found
        """
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt) - 1
        flag = True
        while flag and top <= bottom:
            if pattern:
                symbol = pattern[-1]
                pattern = pattern[:-1]
                lmat = self.bwt[top:(bottom + 1)]
                if symbol in lmat:
                    topindex = lmat.index(symbol) + top
                    bottomindex = bottom - lmat[::-1].index(symbol)
                    top = lf[topindex]
                    bottom = lf[bottomindex]
                else:
                    flag = False
            else:
                res.extend(range(top, bottom + 1))
                flag = False
        return res

    def bw_matching_pos(self, patt) -> List:
        """
        Method that searches for matching patterns
        :param patt: pattern to search
        :return: list of matches found
        """
        res = []
        matches = self.bw_matching(patt)
        for m in matches:
            res.append(self.sa[m])
        res.sort()
        return res

    @staticmethod
    def findithocc(le, elem, index):
        """
        Method that allows the discovered of the i-ésima occurence of
        an symbol in the list
        :param le:
        :param elem:
        :param index:
        :return: -1 in the cases where doesn't occur
        """
        j, k = 0, 0
        while k < index and j < len(le):
            if le[j] == elem:
                k += 1
                if k == index:
                    return j
            j += 1
        return -1
