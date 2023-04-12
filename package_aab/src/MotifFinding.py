
"""
Class: MotifFinding
"""

from package_aab.src.MySeq import MySeq
from package_aab.src.MyMotifs import MyMotifs
from random import randint
from random import random
from typing import Union
from typing import List


class MotifFinding:
    """
    Class implemented for searching for recurrent patterns in a biological sequence,
    which can be DNA or proteins.
    The pattern to look for can be an exact sequence or a degenerate consensus in which there are
    ambiguous characters.
    """

    def __init__(self, size: int = 8, seqs=None) -> None:
        """
        Method that stores the values used in the other methods.
        param size: size of motifs to find
        :param seqs: list of sequences to search
        """
        self.motifSize = size  # stores the size
        if seqs != None:  # if the list of sequence contains sequences
            self.seqs = seqs
            self.seq_type = seqs[0].alphabet()  # stores the type of characters present in the sequence
        else:
            self.seqs = []  # list of sequences

    def __len__(self) -> int:
        """
        Method that returns the length of the strings.
        :return: returns the length of the sequences.
        """
        return len(self.seqs)

    def __getitem__(self, n: int) -> None:
        """
        Method that allows returning an item from the indexing of an instance.
        :param n: position of the value that we want to return.
        :return: character of the position entered
        """
        return self.seqs[n]

    def seqSize(self, i: int) -> int:
        """
        Method that returns the length of the sequence.
        :param i: index of the sequence in the sequence list.
        :return: length of the sequence with index i from the sequence list.
        """
        return len(self.seqs[i])

    def readFile(self, file: str, type: str) -> None:
        """
        Method that reads the sequence file.
        param file: sequence file.
        param type: type of the sequences.
        """
        for seq in open(file, "r"):  # for each sequence in the file
            self.seqs.append(MySeq(seq.strip().upper(), type))  # add a list of sequence in the class
        self.seq_type = self.seqs[0].alphabet()  # identify the type of sequence

    def createMotifFromIndexes(self, indexes: list):
        """
        Method that implements probabilistic motifs of type MyMotif.
        :param indexes: list of the indexes of the initial positions of the motif
        of the sub-sequences used to create the motif.
        :return:
        """
        motif_subseq = []  # empty list to store the subsequences where the motifs begin and end.
        for i, ind in enumerate(indexes):  # for each sequence corresponding to the motif to be started in the index (ind)
            motif_subseq.append(MySeq(self.seqs[i][ind:(ind+self.motifSize)],self.seqs[i].seq_type))
            # adds to the list the sequence corresponding to the motif plus the sequence type
        return MyMotifs(motif_subseq)

    # SCORES

    def score(self, s: list) -> int:
        """
        Method implemented for the scoring function.
        The scoring function iterates over all motif positions and determines the maximum
        value of the motif score.
        :param s: list of motif indices in the entered sequences.
        :return: maximum score of the motif score.
        """
        score = 0  # Initialize the score = zero.
        motif = self.createMotifFromIndexes(s)  # Set the motif as the one created in the previous method.
        motif.doCounts()  # Create a matrix of counts of the motifs.
        mat = motif.mat_count  # Store the matrix of counts in the mat variable.
        # Iterate over the columns of the matrix.
        for j in range(len(mat[0])):
            # Set the maximum value to the value of the first row of the column.
            maxcol = mat[0][j]
            # Iterate over the remaining rows of the column.
            for i in range(1, len(mat)):
                # If the value of the current cell is greater than the maximum value, set the
                # new maximum value to the value of the current cell.
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
                    # Add the maximum value of each column to the total score.
            score += maxcol
            # Return the maximum score.
        return score

    def scoreMult(self, s):
        """
        Method implemented for the multiplication of the maximum motif scores.
        The scoreMult() method provides a way to quantify the importance of each occurrence of a motif by calculating
        the maximum score for each position in the motif, and then multiplying these scores together to get an overall
        score.
        :param s: list of the motif indexes in the introduced sequences.
        :return: multiplication of maximum scores.
        """
        score = 1.0  # Initialize the score to 1.0.
        motif = self.createMotifFromIndexes(s)  # Set the motif as the one created in the previous method.
        motif.createPWM()  # Create a PWM for the motif.
        mat = motif.pwm  # Store the PWM in the mat variable.
        # Iterate over the columns of the matrix.
        for j in range(len(mat[0])):
            maxcol = mat[0][j]  # Set the maximum value to the value of the first row of the column.
            # Iterate over the remaining rows of the column
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:  # If the value of the current cell is greater than the maximum value, set the
                                        # new maximum value to the value of the current cell.
                    maxcol = mat[i][j]
            score *= maxcol  # Multiply the maximum value of each column to the total score.

        # Return the multiplication of maximum scores.
        return score

    # EXHAUSTIVE SEARCH
    def nextSol(self, s: list) -> list:
        """
        Auxiliary method (to exhaustiveSearch) that gives the next vector of starting positions.
        Method implemented to iterate over all the possible values of the motif position in the entered sequence.
        :param s: list of the motif indexes in the entered sequence.
        :return: list of all the possible values of the position of the motif in the entered sequence.
        """
        nextS = [0] * len(s)  # create a list of zeros with the same length as s to store the next solution
        pos = len(s) - 1  # set the initial position to the end of the list s
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:  # iterate over the positions in s
            # while the position is greater than or equal to 0 and the index value in s is equal to the difference
            # between the size of the sequence at position pos and the size of the motif
            pos -= 1  # decrement the position by 1
        if (pos < 0):  # if the position is less than 0
            nextS = None  # there are no possible solutions, set nextS to None
        else:  # if the position is not less than 0
            for i in range(pos):  # iterate over the possible values
                nextS[i] = s[i]  # set the possible value in nextS to the corresponding value in s
            nextS[pos] = s[pos] + 1  # set the last value in nextS to the next value after the last value in s
            for i in range(pos + 1, len(s)):  # iterate over the remaining values in s
                nextS[i] = 0  # set the remaining values in nextS to 0
                # if s did not have all possible values at the positions after pos
        return nextS  # return the list of possible values for the next solution

    def exhaustiveSearch(self) -> list:
        """
        Method implemented to find the motif with the vector of best scores.
        This method allows to derive the profile and the consensus sequence.
        :return: vector of best scores
        """
        best_score = -1  # Define the best score as -1
        score_vect = []  # Create an empty list to store the vector of scores
        s = [0] * len(self.seqs)  # Create a list of zeros for the indices of the sequences
        while s != None:  # While there are still more solutions to search
            sc = self.score(s)  # Calculate the score for the current set of indices
            if sc > best_score:  # If the current score is better than the current best score
                best_score = sc  # Set the current score as the new best score
                score_vect = s  # Update the vector of best scores with the current set of indices

            s = self.nextSol(s)  # Move on to the next set of indices

        return score_vect  # Return the vector of best scores

    # BRANCH AND BOUND
    def nextVertex(self, s: list) -> list:
        """
        Method implemented to find the next vertex.
        :param s: list of indices of the motifs in the entered sequences.
        :return: list of next vertices
        """
        vert_list = []  # Create an empty list to store the next vertices
        if len(s) < len(self.seqs):  # Check if the length of the index list is less than the number of sequences
            # If the index list is shorter than the number of sequences, it means that not all sequences are included
            # and add a value of 0 to the list of vertices
            for i in range(len(s)):
                vert_list.append(s[i])
            vert_list.append(0)
        else:  # If the length of the index list is equal to or greater than the number of sequences
            pos = len(s) - 1  # gives us the last index in the list.
                              # pos  is stored as the initial position for the next vertex search.
            while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1  # Check the position of the current index and move to the next index if the current index
                          # has reached the last motif
            if pos < 0:  # If all positions have been visited, return None as there are no more vertices to explore
                vert_list = None
            else:  # Otherwise, create a list of vertices by adding the current indices before and after incrementing
                   # the current index by 1
                for i in range(pos):
                    vert_list.append(s[i])
                vert_list.append(s[pos] + 1)
        return vert_list

    def bypass(self, s: list) -> list:
        """
        Method implemented to bypass the condition explained above.
        :param s: index list of the motifs in the entered sequences.
        :return: list of indexes with zeros in the non-corresponding positions.
        """
        res = []  # Create an empty list to store the indices with zeros at non-matching positions
        pos = len(s) - 1  # gives us the last index in the list.
                          # pos  is stored as the initial position for the next vertex search.
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1  # Check the position of the current index and move to the next index if the current index
                      # has reached the last motif
        if pos < 0:  # If all positions have been visited, return None as there are no more indices to explore
            res = None
        else:  # Otherwise, create a list of indices by adding the current indices before and after incrementing the current index by 1
            for i in range(pos):
                res.append(s[i])
            res.append(s[pos] + 1)
        return res

    def branchAndBound(self) -> Union[list, List[int], None]:
        """
        Method that implements to iterate over the initial position of the list of solutions to find the best solution
        motif.
        :return:  the vector of starting positions s (representative of the best motif found)
        """
        best_score = -1  # initializing best_score to -1 ensures that the first calculated score will always
        # be greater than best_score, allowing it to become the new best_score if necessary.
        best_motif = None  # initializes the best motif to None
        size = len(self.seqs)  # gets the number of sequences
        s = [0] * size  # creates a list of zeros with length equal to the number of sequences
        while s != None:  # while the list is not empty
            if len(s) < size:  # if the length of the index list is less than the number of sequences
                optimScore = self.score(s) + (size - len(s)) * self.motifSize  # calculates the optimal score
                # the optimal score is the current score plus the product of the difference between
                # the number of sequences and the length of the index list, and the size of the motif
                if optimScore < best_score:  # if the optimal score is less than the best score
                    s = self.bypass(s)  # performs a bypass
                else:  # if the optimal score is greater than or equal to the best score
                    s = self.nextVertex(s)  # finds the next best solution
            else:  # if the length of the index list is equal to the number of sequences
                sc = self.score(s)  # calculates the score of the index list
                if sc > best_score:  # if the score is greater than the best score
                    best_score = sc  # updates the best score
                    best_motif = s  # updates the best motif
                s = self.nextVertex(s)  # finds the next vertex
        return best_motif  # returns the best motif found

    # Consensus (heuristic)

    def heuristicConsensus(self) -> list:
        """
        '''Method that computes the heuristic consensus algorithm:
        - Considering only the first two sequences, choose the initial positions s1 and s2 that give a better score.
        - For each of the following sequences, iteratively, choose the best starting position in the sequence, in order
         to maximize the score.

        :return: list of starting positions s (representative of the best motif found)
        """
        # Initialize the MotifFinding object with the first two sequences
        mf = MotifFinding(self.motifSize, self.seqs[:2])
        # Obtain the starting positions with exhaustive search for the first two sequences
        s = mf.exhaustiveSearch()
        # For each of the following sequences, iteratively, choose the best starting position in the sequence, in order
        # to maximize the score
        for a in range(2, len(self.seqs)):
            # Append a zero to the starting positions list for the new sequence
            s.append(0)  # the algorithm does not know where the motif starts in this sequence
                         # Once the algorithm iteratively determines the best starting position
                         # for this sequence, it will replace the 0 with the actual starting position.
            best_score = -1  # define the best score
            melhorPosition = 0  # define the best position
            # Check all possible starting positions for the new sequence and choose the one with the highest score
            for b in range(self.seqSize(a) - self.motifSize + 1):
                s[a] = b
                scoreatual = self.score(s)  # calculates the score and sets it as current value
                if scoreatual > best_score:  # if the current score is higher than the best
                    best_score = scoreatual  # saves the current one as better
                    melhorPosition = b  # returns the best position as the position with the best score
                # returns the index of a as the best position
                s[a] = melhorPosition
        # Return the list of starting positions as representative of the best motif found
        return s


    def heuristicStochastic(self) -> list:
        """
        Method that computes the heuristic stochastic consensus algorithm, using the most likely segments to adjust
        starting positions to achieve the best profile (motif)
        :return: the vector of starting positions s (representative of the best motif found)
        """
        # Initialize starting positions randomly
        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):  # run the list of sequences
            s[i] = randint(0, self.seqSize(i) - self.motifSize)

        # Calculate the score of the starting positions
        best_score = self.score(s)

        # Initialize the loop for improvement
        improve = True  # sets the best one with true
        while improve:  # as long as the improvement is true
            # Create motif and PWM from current starting positions
            motif = self.createMotifFromIndexes(s)  # defines the motifs from the index list
            motif.createPWM()  # creates the PWM

            # Update starting positions based on the most probable sequence for each sequence
            for i in range(len(self.seqs)):  # run the index list in the range of the number of sequences
                s[i] = motif.mostProbableSeq(self.seqs[i])  # calculates the sub-sequence

            # Calculate the score of the updated starting positions
            scr = self.score(s)

            # Check if there is improvement in score and update best_score accordingly
            if scr > best_score:
                best_score = scr
            else:
                improve = False

        # Return the final list of starting positions
        return s

    # Gibbs sampling
    def gibbs(self, num_iterations :int) -> list:
        """
        Method that implements the Gibbs Sampling algorithm, by choosing new segments at random (increasing
        the possibilities of converging to a correct solution). The algorithm starts with a set of randomly
        selected motif positions, and then in each iteration, it chooses one sequence at random, removes it from
        consideration, and recomputes the motif position based on the remaining sequences. This process continues
        for a fixed number of iterations, after which the algorithm returns the best set of motif positions found so far.
        :param num_iterations: number of iterations
        :return: list of best scores
        """
        # Initialize randomly starting positions
        s = []
        for i in range(len(self.seqs)):
            s.append(randint(0, len(self.seqs[i]) - self.motifSize - 1))

        # Initialize best score and positions
        best_score = self.score(s)  # calculate score based on the initial positions
        bests = list(s)

        # Perform Gibbs Sampling
        for it in range(num_iterations):  # loop for the specified number of iterations
            # Choose a sequence at random
            seq_idx = randint(0, len(self.seqs) - 1)  # choose a random sequence index
            seq = self.seqs[seq_idx]  # get the corresponding sequence

            # Remove the selected sequence from positions and sequences
            s.pop(seq_idx)
            removed = self.seqs.pop(seq_idx)

            # Create a motif and PWM from remaining positions
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()

            # Insert the removed sequence back into the list of sequences
            self.seqs.insert(seq_idx, removed)

            # Compute probability of each position in the selected sequence
            r = motif.probAllPositions(seq)

            # Use roulette method to choose a new position for the selected sequence
            pos = self.roulette(r)

            # Insert the new position into the list of positions
            s.insert(seq_idx, pos)

            # Update the best score and positions if a better score is found
            score = self.score(s)
            if score > best_score:
                best_score = score
                bests = list(s)

        # Return the best positions found
        return bests

    def roulette(self, f: list) -> int:
        """
        Method implemented to simulate examples of a roulette wheel.
        The probability of choosing a certain position is proportional to your score.
        :param f: list of positions
        :return: chosen value
        """
        # Calculate the sum of all values in the list f, plus a small constant 0.01 for each value
        tot = 0.0
        for x in f:
            tot += (0.01+x)
        # Generate a random value between 0 and the sum of all values in f
        val = random() * tot
        # Traverse the list f and accumulate the sum of each value plus 0.01 until it exceeds the random value val
        # The index of the value that causes this condition to be met is returned
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        # Return the index of the chosen value in f
        return ind-1