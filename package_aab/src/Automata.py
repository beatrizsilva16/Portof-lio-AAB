
class Automata:
    """
    Class implemented for the search of patterns in nucleotide sequences.
    This pattern search method processes a sequence in a linear way,
    reading from left to right.
    The search started at the first state of the "machine" and at the first character of the text,
    at each step of the search the next character of the sequence is considered, the next state is searched
    state and moves to a new state.
    The number of states is equal to the length of the pattern plus one.
    The pattern is found when the pattern being searched for is equal to the length of the pattern entered.
    """

    def __init__(self, alphabet: str, pattern: str):
        """
        Method which saves the values used in the other methods
        :param alphabet: saves all characters present in the sequence
        :param pattern: pattern we want to search for
        """
        self.numstates = len(pattern) + 1  # saves the length of the pattern. Automaton needs
                                           # to have one extra state that represents the final state,
                                           # indicating that the pattern has been found
        self.alphabet = alphabet  # all the characters present in our sequence
        self.transitionTable = {}  # dictionary of the transition table
        self.buildTransitionTable(pattern)  # saves the transition table

    def buildTransitionTable(self, pattern: str):
        """
        Method that constructs the transition table. The transition table returns the next
        state of the automata machine from the current state and previous states.
        :param pattern: pattern to search in the sequence
        """
        for char_p in range(self.numstates):  # loop through each character in the pattern
            for char in self.alphabet:  # loop through each character in the alphabet
                possible_pattern = pattern[:char_p] + char  # creates all possible patterns
                # patern[:char_p] represents the history of previous states. By adding char to
                # the end of this slice, we create a new pattern that includes the current state and
                # the history of previous states.
                match_next_state = overlap(possible_pattern, pattern)  # find the overlap between each possible
                # pattern and the original pattern. The resulting overlap represents the next state of
                # the automaton machine.
                self.transitionTable[(char_p, char)] = match_next_state
                # the transition table is a dictionary where each key is a tuple with the current state
                # and character and the value is the next state

    def printAutomata(self):
        """
        Method that prints the results of the pattern search using the automata.
        :return : automata printed
        """
        print("States: ", self.numstates)  # prints the number of states used in the automata
        print("Alphabet: ", self.alphabet)   # prints the alphabet used in the automata
        print("Transition table:")  # prints the transition table, which shows the current state,
                                    # input character and the next state.
        # iterates over the keys of the transition table, which are tuples containing the current state
        # and input character
        for keys in self.transitionTable.keys():
            # prints the current state, input character and the next state,
            # using the keys to access the values in the transition table.
            print("[", keys[0], "|", keys[1], " -> ", self.transitionTable[keys], "]")

    def nextState(self, current: int, char:str) -> int:
        """
        Method that returns the next state.
        :param current: current state
        :param char: character of the pattern to search for
        :return: the next state
        """
        return self.transitionTable.get((current, char))


    def applyNextState(self, seq: str) -> list:
        """
        Method that returns a list of all next states.
        :param seq: sequence entered
        :return: list of next states
        """
        state = 0  # initialize state as 0 (start state)
        next_state_list = [state]  # create a list to store all next states, starting with the initial state
        for char in seq:  # iterate through all characters in the input sequence
            state = self.nextState(state, char)
            # determine the next state based on the current state and current character
            next_state_list.append(state)  # add the next state to the next_state_list
        return next_state_list

    def patternSeqPosition(self, seq: str) -> list:
        """
        Method that returns the list of positions where an occurrence of the pattern in the sequence starts.
        :param: sequence entered
        :return: list of the positions where an occurrence of the pattern in the sequence starts.
        """
        state = 0  # initialize state to 0
        ocurences_list = []  # create a list to store the positions of pattern occurrences
        for i in range(len(seq)):  # loop through all positions in the sequence
            state = self.nextState(state, seq[
                i])  # get the next state based on the current state and the character at the current position
            if state == self.numstates - 1:  # check if the final state is reached, indicating a match with the pattern
                ocurences_list.append(
                    i - self.numstates + 2)  # add the position where the pattern match starts to the list
                # the calculations above are necessary to obtain the correct starting position of the pattern match
        return ocurences_list


def overlap(seq1: str, seq2: str) -> int:
    """
    Method that overlaps two sequences and checks for matching
    :param seq1: first string
    :param seq2: second string
    :return: last position of the smallest string that matches
    """

    overlap_start = min(len(seq1), len(seq2))  # determine the length of the shortest sequence
    # to start the overlap

    for i in range(overlap_start, 0, -1):  # for loop to iterate through the shortest sequence
        # from the end to the beginning

        if seq1[-i:] == seq2[:i]:  # check if there is a match between the last character of the first
            # sequence and the first character of the second sequence
            return i  # returns the position of the matching character, starting from the end of the
            # shortest sequence
    return 0  # if there is no match, return 0