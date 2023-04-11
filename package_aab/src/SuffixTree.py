"""
Class: SuffixTree - Trie of sufixes
"""

class SuffixTree:
    '''
    Class that creates a suffix tree of a pattern that will be searched in a sequence.
    It allows pre-processing a target sequence, making its search more efficient.
    It is the solution to pre-process very large sequences, discovering which trees contain a given pattern,
    finding out the longest common substring in a set of sequences and calculating the maximum overlap of a set of
    sequences.
    '''

    def __init__(self):
        """
        Method storing the values used in the other methods.
        """
        self.nodes = {0: (-1, {})}  # This line initializes a dictionary called nodes
        # with one key-value pair. The key is the integer 0, and the value is a tuple
        # with two elements: the first element is -1, which represents the position of
        # a suffix if the node is a leaf, or -1 if the node is an internal node; the second
        # element is an empty dictionary, which will be used to store the edges leading to the child nodes.
        self.num = 0  # assign unique indices to the nodes as they are added to the tree.

    def printTree(self) -> None:
        """
        Method that prints the suffix tree.
        """
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:  # if the node is an internal node
                print(k, "->", self.nodes[k][1])  # print the key followed by an arrow and the dictionary of child nodes
            else:  # if the node is a leaf node
                print(k, ":",
                      self.nodes[k][0])  # print the key followed by a colon and the position of the represented suffix

    def addNode(self, origin: int, symbol: str, leafnum=-1) -> None:
        """
        Method that adds nodes to the tree.
        :param origin: current node
        :param symbol: character to be added to the node
        :param leafnum: leaf number (-1 is default)
        """
        # print("Symbol: ", symbol)
        # print("Leaf number: ", leafnum)
        self.num += 1  # adds a node to the tree, increasing its size
        self.nodes[origin][1][
            symbol] = self.num  # creates a new node and links it to an existing one (through the origin parameter)
        self.nodes[self.num] = (leafnum, {})  # creates a new node with the leaf number and an empty dictionary

    def addSuffix(self, p: list, sufnum: int) -> None:
        """
        Method that adds suffix to the tree.
        :param p: pattern
        :param sufnum: suffix number for leaves or -1 for non-leaves
        """
        pos = 0  # initial position of the pattern. Iterates the symbols of the pattern p,
                 # while the node remains the current node of the tree, starting from the root (node 0)
        node = 0
        while pos < len(p):  # while the first position of the pattern is less than the size of the pattern,
            if p[pos] not in self.nodes[node][1].keys():  # if the initial position of the pattern is not present in the dictionary of nodes keys (if there is no arc yet),
                if pos == len(p) - 1:  # if the initial position is the last one of the pattern,
                    self.addNode(node, p[pos], sufnum)  # adds a node with the suffix
                else:  # otherwise,
                    self.addNode(node, p[pos])  # doesn't add a suffix
            node = self.nodes[node][1][p[
                pos]]  # if there is an arc in the initial position of the pattern, it will be the current node and the iteration will start from this node
            pos += 1  # increment i by 1 to move to the next iteration, repeating the process until the end of the pattern (len(p)).

    def suffixTreeFromSeq(self, text: str) -> None:
        """
        Method that creates the suffix tree, adding a symbol ("$") at the end of the sequence and calling the previous method
        for each suffix of the sequence -> no suffix will be the prefix of another suffix.
        :param text: sequence that will be added to the tree
        """
        t = text + "$"  # adds "$" at the end of the text
        for i in range(len(t)):  # for each index in the range of the text size (with $),
            self.addSuffix(t[i:], i)  # add suffix in each iteration

    def findPattern(self, pattern: str):
        """
        Method that searches for patterns (trie) starting from the root until reaching the final node or failing the search.
        :param pattern: pattern to search for
        :return: list of leaves below a given node or None (if search fails)
        """
        pos = 0  # starting position
        node = 0  # node
        for pos in range(
                len(pattern)):  # for each position along the length of the pattern to search, starting from the root,
            if pattern[pos] in self.nodes[node][1].keys():  # if the arcs are present in the pattern symbol set,
                node = self.nodes[node][1][pattern[pos]]  # add the pattern to the tree node
            else:  # if the arcs are not present in the pattern symbol set,
                return None  # return None -> the pattern does not occur
        return self.getLeavesBelow(
            node)  # at the end of the for loop, return the set of leaves below a given node using the recursively implemented auxiliary method get_leaves_below

    def getLeavesBelow(self, node: int) -> list:
        """
        Auxiliary method for collecting all leaves below a given node.
        :param node: node from which to search for leaf information below it
        :return: list of leaves below a given node
        """
        res = []  # empty list that will contain the leaves below a given node and that will be returned
        if self.nodes[node][0] >= 0:  # if the leaf with the pattern in question is found,
            res.append(self.nodes[node][0])  # the leaf is added to the final list
        else:  # otherwise,
            for k in self.nodes[node][1].keys():  # for each character of the node,
                newnode = self.nodes[node][1][k]  # create a new node with that character
                leaves = self.getLeavesBelow(newnode)  # create a leaf with the new node
                res.extend(leaves)
        return res




