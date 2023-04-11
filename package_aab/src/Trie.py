'''
Class: Trie - Trie of prefixes
'''

class Trie:
    '''
    Class responsible for implementing the prefix tree that allows pre-processing
    of a set of patterns. The symbols of a given alphabet are associated with the arcs of a tree.
    The trie is built from a set of patterns, starting from the root node and iterating
    each pattern, adding the necessary nodes so that the tree contains the path from the root to the leaf,
    representing the pattern.
    '''
    def __init__(self):
        '''
        Method storing the values used in the other methods
        '''
        self.nodes = {0: {}}  # A dictionary that stores the nodes of the trie. Each node is
        # represented by a unique integer key. The value of each key is a dictionary that stores
        # the edges of the node, i.e., the symbols that are associated with the arcs of the tree
        # and the destination nodes they lead to. The root node is represented by 0 and is initially
        # assigned an empty dictionary.
        self.num = 0  # An integer that stores the number of nodes created. Initially set to 0.
    def printTrie(self):
        '''
        Method that print the trie
        '''
        for k in self.nodes.keys():
            print(k, "->", self.nodes[k])

    def addNode(self, origin: int, symbol: str) -> None:
        '''
        Method that adds a node to the trie.
        This method is used by the add_pattern method.
        :param origin: existing node
        :param symbol: character referring to the node to be added (arc identification)
        '''
        self.num += 1  # adds a new node to the tree, increasing its size
        self.nodes[origin][
            symbol] = self.num  # creates a new node and links it to an existing one (through the origin parameter)
        self.nodes[self.num] = {}  # creates a new node with an empty dictionary

    def addPattern(self, p: list) -> None:
        '''
        Method that adds a pattern to the trie
        :param p: input pattern
        '''
        position = 0  # initialize position of pattern
        node = 0  # start from the root node (0)
        while position < len(p):  # iterate through the pattern, until the end is reached
            if p[position] not in self.nodes[node].keys():  # if the current symbol is not a key in the node's
                                                            # dictionary of edges,
                self.addNode(node, p[position])  # create a new node and edge for the current symbol
            node = self.nodes[node][
                p[position]]  # update the current node to the node connected by the edge for the current symbol
            position += 1  # move to the next symbol in the pattern

    def trieFromPatterns(self, pats: list) -> None:
        '''
        Method that adds each pattern of the input to the trie.
        :param pats: input patterns
        '''
        for p in pats:
            self.addPattern(p)  # adds each pattern present in the pattern list

    def prefixTrieMatch(self, text: str):
        '''
        Method to search if a trie pattern is a sequence prefix.
        Scrolls through the sequence of characters and the tree, starting at the root, following the
        arcs corresponding to the characters of the sequence until one of the following occurs:
        - If it reaches a leaf of the trie, the pattern has been identified;
        - The character of the sequence does not exist -> no pattern was identified in the trie.
        :param text: sequence of characters
        :return: prefix match or None
        '''
        position = 0  # initialize the position to 0 (start of the sequence)
        match = ""  # initialize the match string to an empty string
        node = 0  # initialize the node to the root of the trie
        while position < len(text):  # while there are still characters left in the sequence
            if text[position] in self.nodes[node].keys():  # if the current character is in the
                                                           # keys of the current node
                node = self.nodes[node][text[position]]  # update the current node to the next node
                                                         # corresponding to the current character
                match += text[position]  # add the current character to the match string
                if self.nodes[node] == {}:  # if the current node is a leaf (has an empty dictionary as its value)
                    return match  # return the match string, as a pattern has been identified
                else:  # if the current node is not a leaf
                    position += 1  # move to the next character in the sequence
            else:
                return None  # if the current character is not in the keys of the current node,
                             # no pattern was identified in the trie
        return None  # if the end of the sequence is reached without finding a leaf node,
                     # no pattern was identified in the trie

    def trieMatches(self, text: str) -> list:
        '''
        Method to, using the prefixTrieMatch method, look for occurrences (matches) of the pattern in the sequence.
        Iterative process - matches the sequence, removes the first symbol from the sequence, repeats the process
        is repeated for all suffixes in the sequence.
        :param text: sequence
        :return: list of matches
        '''
        res = []  # create an empty list to store matches
        for i in range(len(text)):  # iterate through each position in the sequence
            m = self.prefixTrieMatch(text[
                                     i:])  # use the prefixTrieMatch method to find matches for the remaining part of the sequence starting from position i
            if m != None:  # if a match is found,
                res.append((i, m))  # add the position and the match to the result list as a tuple
        return res  # return the list of matches
