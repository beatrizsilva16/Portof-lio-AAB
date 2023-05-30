import pprint


class SuffixTree:

    """
    Class that creates a suffix tree of a pattern that will be searched in a sequence.
    It allows pre-processing a target sequence, making its search more efficient.
    It is the solution to pre-process very large sequences, discovering which trees contain a given pattern,
    finding out the longest common substring in a set of sequences and calculating the maximum overlap of a set of
    sequences.
    """
    def __init__(self, seqs: str):
        self.trie = {}  # Trie structure represented as a dictionary
        self.nodes = {0: (-1, {})}  # root node
        # dictionary with tuples of each node
        # 1st element is the suffix position (for leaves) or -1 (if not leaf -> internal nodes)
        # 2nd element corresponds to a dictionary
        # keys: symbols of the arc; values: index of the destination nodes <- represents the leaves of the tree
        self.num = 0
        self.seqs = seqs  # Input sequences
        self.check_seqs()

    def check_seqs(self):
        """
        Method that verifies if the sequence introduced is a string
        """
        if type(self.seqs) != str:
            raise TypeError("Input sequence must be a string.")
    
    def print_tree(self):
        """
        Method that prints the tree structure (dictionary)
        """
        pprint.pprint(self.trie, width=1)
                
    def add_node(self, origin, symbol: str, leaf_num=-1) -> None:
        """
        Method that adds nodes to the tree.
        :param origin: current node
        :param symbol: character referring to the node to be added
        :param leaf_num: leaf number (-1 is default, correspond to an internal node)
        """
        self.num += 1  # add a node in the trie
        self.nodes[origin][1][symbol] = self.num  # creates a new node and links it to an existing node
                                                  # (via - origin parameter)
        self.nodes[self.num] = (leaf_num, {})  # create new node with leaf number and empty dictionary
        
    def add_suffix(self, p, suf_num):
        """
        Method that adds suffix to the tree.
        :param p: pattern
        :param suf_num: suffix number for leaves or -1 for non-leaves
        """
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():
                if pos == len(p) - 1:
                    self.add_node(node, p[pos], suf_num)
                else:
                    self.add_node(node, p[pos])
            node = self.nodes[node][1][p[pos]]
            pos += 1
    
    def suffix_tree_from_seq(self, text):
        """
        Method that creates the suffix tree by adding a symbol ("$") at the end of the sequence and calls the previous method
        for each suffix in the sequence -> no suffix will be prefixed with another suffix.
        :param text: sequence that will be added to the tree
        """
        t = text + "$"  # adds "$" in the final text
        for i in range(len(t)):
            self.add_suffix(t[i:], i)

    def get_leafes_below(self, node):
        """
        Auxiliary method to collect all the leafes below a given node.
        param node: node from which the information of the sheets below this one are searched.
        :return: list of sheets below a given node.
        """
        res = []
        if self.nodes[node][0] >=0: 
            res.append(self.nodes[node][0])            
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res

    def find_pattern(self, pattern):
        """
        Method that looks for patterns (trie) starting from the root until it reaches the end node or fails the search.
        :param pattern: pattern to search for
        :return: list of sheets below a given node or none (if search fails)
        """
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)

# tests

def test():
    seq = "TACTA"
    st = SuffixTree("TACTA")
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print(st.find_pattern("TA"))  # output: [0,3]  values of the leafes
    print(st.find_pattern("ACG"))  # output: None