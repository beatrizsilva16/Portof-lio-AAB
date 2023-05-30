import pprint


class Trie:
    """
    Class responsible for implementing the prefix tree that allows pre-processing
    of a set of patterns. The symbols of a given alphabet are associated with the arcs of a tree.
    The trie is built from a set of patterns, starting from the root node and iterating
    each pattern, adding the necessary nodes so that the tree contains the path from the root to the leaf,
    representing the pattern.
    """

    def __init__(self, seqs: str):
        self.trie = {}  # Trie structure represented as a dictionary
        self.seqs = seqs  # Input sequences
        self.check_seqs()  # Check if sequences are strings
        self.insert(seqs)  # Insert sequences into the trie

    def check_seqs(self):
        """
        Method that verifies if the sequence is a string
        """
        if type(self.seqs) != str:
            raise TypeError("Input sequence must be a string.")

    def print_trie(self):
        """
        Method that prints the tree structure (dictionary)
        """
        pprint.pprint(self.trie, width=1)  # Print the trie structure

    def insert(self, seq: str) -> None:
        """
        Method that inserts the sequences into the trie
        :param seq: sequences introduced
        :return:
        """
        if ' ' in seq:  # If multiple sequences are given as a single string
            seqs = seq.split()
            for s in seqs:  # Insert each sequence separately
                self.insert_sequence(s)
        else:
            self.insert_sequence(seq)  # Insert the single sequence

    def insert_sequence(self, seq) -> None:
        """
        Method that inserts a single sequence into the trie.
        :param seq: sequence introduced
        :return: 
        """
        node = self.trie
        for char in seq:  # Traverse through each character in the sequence
            if char not in node:  # Create a new node if the character is not present
                node[char] = {}
            node = node[char]  # Move to the next node
        node["#$#"] = True  # Mark the end of a sequence with a special key

    def matches(self, seq) -> bool:
        """
        Method  that verifies if a given sequence matches any sequence present in the trie
        :param seq: sequence introduced
        :return: booleano
        """
        node = self.trie
        for char in seq:  # Traverse through each character in the sequence
            if char not in node:  # If any character is not present, the sequence is not a match
                return False
            node = node[char]  # Move to the next node
        return "#$#" in node  # Check if the end marker is present in the last node
