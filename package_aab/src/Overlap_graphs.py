from package_aab.src.MyGraph import MyGraph


class OverlapGraph(MyGraph):

    def __init__(self, frags: list, reps: bool=False):
        """"
        Construction of a graph from the elements of the list "frags" provided.
        Graph can accept repeats or not, depending on the user preference
        """
        MyGraph.__init__(self, {})
        if reps:
            self.create_overlap_graph_with_reps(frags)
        else:
            self.create_overlap_graph(frags)
        self.reps = reps

    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags: list):
        """
        Graph creation without repetitions consideration. Relation between nodes is created if overlap of prefix and suffix exists
        :param frags: List of elements to add to the graph
        """
        for seq in frags:
            self.add_vertex(seq)
        for g in frags:
            for f in frags:
                if suffix(g) == prefix(f): self.add_edge(g, f)

    def create_overlap_graph_with_reps(self, frags: list):  # caso de replicas de fragmentos
        """
        Graph creation considering repititions. Here each element possesses an identifier as "-" + number. Relation between nodes is created if overlap of prefix and suffix exists
        :param frags: List of elements to add to the graph
        :return:
        """
        idnum = 1
        for seq in frags:
            self.add_vertex(seq + "-" + str(idnum))
        idnum = idnum + 1
        idnum = 1
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf:
                    for x in self.get_instances(seq2):
                        self.add_edge(seq + "-" + str(idnum), x)
        idnum = idnum + 1

    def get_instances(self, seq):
        """
        Auxiliary function of "create_overlap_graph" and "create_overlap_graph_with_reps" methods that obtains the elements of the graph where "seq" occurs in the graph
        :param seq: Sequence to encounter the occurrences of this in the graph
        :return: Elements where "seq" was found in the graph
        """
        res = []
        for k in self.graph.keys():
            if seq in k: res.append(k)
        return res

    def get_seq(self, node):
        """
        Auxiliary method of "seq_from_path" that obtains the sequence separated from the number identifier. Example: "ACC-1" -> "ACC"
        :param node: Node to obtain the only the sequence
        :return: Final sequence without the identifier
        """
        if node not in self.graph.keys(): return None
        if self.reps:
            return node.split("-")[0]
        else:
            return node

    def seq_from_path(self, path):
        """
        Obtain sequence from a give path. Essentially obtains the first element of the list and adds to the string the final character of the rest of the elements
        :param path: List elements of a path
        :return: String with the final sequence obtained from the path
        """
        if self.check_if_hamiltonian_path(path):
            seq = self.get_seq(path[0])
            for i in range(1, len(path)):
                next = self.get_seq(path[i])
                seq += next[-1]
            return seq
        else:
            return None


# auxiliary
def composition(k: int, seq: str) -> list:
    """
    Method to obtain each element of "k" size possible from the sequence "seq"
    :param k: Size of each element to retrieve
    :param seq: Original sequence
    :return:  List of elements from the "seq" with "k" size
    """
    res = []
    for i in range(len(seq) - k + 1):
        res.append(seq[i:i + k])
    res.sort()
    return res


def suffix(seq: str) -> str:
    """
    Method to get the suffix of a given sequence
    :param seq: Original sequence
    :return: Suffix from the given sequence
    """
    return seq[1:]


def prefix(seq):
    """
    Method to get the prefix of a given sequence
    :param seq: Original sequence
    :return: Prefix from the given sequence
    """
    return seq[:-1]


# testing / mains
def test1():
    seq = "CAATCATGATG"
    k = 3
    print(composition(k, seq))


def test2():
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags, False)
    ovgr.print_graph()


def test3():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()


def test4():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    path = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3']
    print(ovgr.check_if_valid_path(path))
    print(ovgr.check_if_hamiltonian_path(path))
    path2 = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3', 'TGG−13', 'GGC−10', 'GCA−9', 'CAT−6', 'ATT−4', 'TTT−15', 'TTC−14',
             'TCA−12', 'CAT−7', 'ATA−1', 'TAA−11']
    print(ovgr.check_if_valid_path(path2))
    print(ovgr.check_if_hamiltonian_path(path2))
    print(ovgr.seq_from_path(path2))


def test5():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)

    path = ovgr.search_hamiltonian_path()
    print(f"Path -> {path}")
    print(ovgr.check_if_hamiltonian_path(path))
    print(ovgr.seq_from_path(path))


def test6():
    orig_sequence = "CAATCATGATGATGATC"
    frags = composition(3, orig_sequence)
    print(frags)
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    print(f"Path -> {path}")
    print(ovgr.seq_from_path(path))


test1()
print()
test2()
print()
test3()
print()
test4()
print()
test5()
print()
test6()