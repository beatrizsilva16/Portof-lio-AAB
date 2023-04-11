from typing import List


class BWT:
    """
    Class for implementing the Burrows-Hweeler algorithm where different methods have been created. The algorithm is useful for
    compressing large sequences, thus reducing their space. Moreover, it is possible to find patterns in the
    compression format efficiently.
    """
    def __init__(self, seq='', buildsufarray=False, sa=None):
        self.bwt = self.build_bwt(seq, buildsufarray)
        self.sa = sa

    def set_bwt(self, bw):
        self.bwt = bw

    def build_bwt(self, text, buildsufarray=False) -> str:
        """
        Method to build the matrix for Burrows-Wheeler transformation.
        param text: sequence we want to use
        param buildsufarray: parameter to create a suffix array. Default: False.
        """
        ls = []  # Create a list for our rotations.

        for i in range(len(text)):  # $ is already included in the sequence.
            # Add all possible rotations.
            ls.append(text[i:] + text[:i])
        # Alphabetically sort the obtained sequences.
        ls.sort()

        # Get the Burrows-Wheeler Transform (BWT):
        res = ''
        for i in range(len(text)):  # For each character in the sequence,
                # get the last column of the matrix, called the Burrows-Wheeler Transform (BWT).
            res += ls[i][len(text) - 1]

        # If buildsufarray is True:
        if buildsufarray:
            self.sa = []
            for i in range(len(ls)):
                # For each element in the list of rotations, get the index where the $ sign is.
                stpos = ls[i].index("$")
                # Add the initial position of each suffix to the list of suffixes.
                # Suffix arrays allow us to search for the position of matches with the BWT.
                self.sa.append(len(text) - stpos - 1)
        return res

    # recuperação da sequencia original
    def inverse_bwt(self) -> str:
        """
        Method to get the original sequence
        :return: string of the original sequence
        """
        # Note that the 1st symbol of the sequence should be immediately after the $.
        firstcol = self.get_first_col()  # Call method to get the 1st column to index.
        res = ""
        c = "$"  # $ is the first character.
        occ = 1  # First occurrence.
        for i in range(len(self.bwt)):   # Traverse BWT (last column)
            # Find the index where $ occurs for the first time.
            pos = findithocc(self.bwt, c, occ)
            c = firstcol[pos]  # in the first column tells us which letter it corresponds to, #gives us the value of "$"
            occ = 1
            k = pos - 1  # position prior to the first "$" index
            while firstcol[k] == c and k >= 0:  # as long as the value of the position before "$" is equal to the value of $
            # and the k-index is greater than zero
                occ += 1  # increase next occurrence
                k -= 1  # set k for the next cycle #k becomes equal pos - 2
            res += c  # add character
        return res

    # implementing the search for patterns from BWT
    def last_to_first(self) -> List:
        """
        Method to create the table with the last column and the first column
        :return: list of indices of the transform
        """
        res = []
        firstcol = self.get_first_col()  # call method to get the first column
        for i in range(len(firstcol)):  # for each element of the first column
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c) + 1
            val = findithocc(firstcol, c, ocs)
            res.append(val)
        return res

    def get_first_col(self) -> List[str]:
        """
        Method to retrieve the first column. note that the first column is the alphabetical ordering of the transform
        :return: list of the first column
        """
        primeira_col = []
        for c in self.bwt:  # for each symbol in the transform
            primeira_col.append(c)  # add to the list the character to iterate from the transform.sort()  # colocar por ordem alfabética
        return primeira_col  # we have our first column

    def bw_matching(self, pattern=str) -> List[int]:
        """
        Method to look for patterns from the Burrows-Wheeler transform.
        :param pattern: pattern we want to find
        :return: list with matches
        """
        lf = self.last_to_first()  # call the method to make matrix
        res = []
        # 1st step is to identify the last symbol of the pattern and see where it matches in the last column
        # identify positions of these symbols in the first row, updating the T (top) and B (bottom) indices
        top = 0  # Initial position of the first column
        bottom = len(self.bwt) - 1  # final position of the first column
        flag = True
        while flag and top <= bottom:  # # As long as the bottom is greater or equal to the top we continue
            if pattern != "":  # if the pattern is other than empty string
                symbol = pattern[-1]  # last symbol of the pattern
                pattern = pattern[:-1]  # all elements but the last in the pattern
                lmat = self.bwt[top:(bottom+1)]  # column using top and bottom
                if symbol in lmat:  # for each character in the column (top-bottom) if the symbol is in the array:
                    topindex = lmat.index(symbol) + top  # configure the top in the column
                    bottomindex = bottom - lmat[::-1].index(symbol)  # configure the bottom in the column
                    top = lf[topindex]  # make the matrix with the new top, bot
                    bottom = lf[bottomindex]
                else:
                    flag = False  # if symbol is not in the array, abort
            else: #
                for i in range(top, bottom + 1):
                    res.append(i)
                flag = False
        print("res: ", res)
        return res

    def bw_matching_pos(self, patt) -> List:
        """
        Method that finds the matches of a pattern
        :param patt: pattern we want to find
        :return: list of matches found
        """
        res = []
        matches = self.bw_matching(patt)  # obtain matches
        for m in matches:  # for each match:
            res.append(self.sa[m])  # append of each array of the suffix
        res.sort()
        return res  # return list with matches found


def findithocc(le, elem, index):
    """
    Method to find out the position of the i-th occurrence of a symbol
    in a list (returns -1 if it doesn't occur).
    param le: array to look for
    param elem: element to search for
    :param index: occurrence to look for
    """
    j, k = 0, 0  # j, number of times it has already found; k, index that runs through the seq.
    while k < index and j < len(le):
        if le[j] == elem:
            k += 1
            if k == index:
                return j
        j += 1
    return -1