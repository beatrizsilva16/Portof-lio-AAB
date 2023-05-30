from package_aab.src.MyGraph import MyGraph


class DeBruijnGraph(MyGraph):
    """
    Class implemented to represent Bruijn graphs. These represent the fragments (k-mers) as
    arcs of the graph and the nodes as sequences of size k-1, corresponding to prefixes or suffixes of the
    fragments.
    This class is a subclass of MyGraph and thus inherits all the methods defined in it.
    """

    def __init__(self, frags: list):
        """
        Constructor method that stores the values used in the other methods
        :param frags: a set of sequences (k-mers)
        """
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o: str, d: str):
        """
        Method that adds the arc (o,d) to the graph, checking that it doesn't already exist there
        param o: arc vertice
        param d: vertex of arc
        """
        if o not in self.graph.keys(): #se o vertice o não existe
            self.add_vertex(o) #adiciona vertice o
        if d not in self.graph.keys(): #se o vertice d não existe
            self.add_vertex(d) #adiciona vertice d
        self.graph[o].append(d) #adiciona o valor d ao vertice o

    def in_degree(self, v: str) -> int:
        """
        Method that calculates the degree of entry of node v
        :param v: node
        :return: returns the node's degree of entry
        """
        count_nodes = 0
        for k in self.graph.keys(): #para cada nodo no grafo
            if v in self.graph[k]: #se o nodo v se encontra no grafo
                count_nodes += self.graph[k].count(v) #contagem dos nodos presentes no grafo
        return count_nodes

    def create_deBruijn_graph(self, frags: list):
        """
        Method implementing the creation of a DeBruijn graph
        :param frags: a set of sequences
        """
        for seq in frags: #para cada sequência em fragmentos
            suffix_seq = suffix(seq) #cria o sufixo da sequência
            self.add_vertex(suffix_seq) #adiciona o sufixo como um vertice ao grafo
            prefix_seq = prefix(seq) #cria o prefixo da sequência
            self.add_vertex(prefix_seq) #adiciona o prefixo como um vertice ao grafo
            self.add_edge(prefix_seq,suffix_seq) #adiciona o arco entre o prefixo e o sufixo

    def seq_from_path(self, path: list) -> str:
        """
        Method that gets the sequence from the constructed path.
        param path: path of the list graph
        :return: returns the sequence represented by the constructed path
        """
        seq = path[0]
        #define o início da sequência como o primeiro nodo no caminho (nodo correspondente ao index 0 da lista path)
        for i in range(1, len(path)):
            #para cada nodo presente no caminho desde o nodo correspondente ao index 1 da lista do caminho (path)
            next = path[i] #define o próximo nodo como sendo o nodo no index seguinte da lista do caminho
            seq += next[-1] #adiciona o nodo à sequêcia
        return seq


def suffix(seq: str) -> str:
    """
    Method that gets the sequence suffix obtained in the "seq_from_path" method.
    :param seq: sequence represented by the constructed path
    :return: returns the sequence suffix seq, which corresponds to the sequence except the first character
    """
    return seq[1:]


def prefix(seq: str) -> str:
    """
    Method that gets the sequence prefix obtained in the "seq_from_path" method.
    :param seq: sequence represented by the constructed path
    :return: returns the sequence prefix seq, which corresponds to the sequence except the last character
    """
    return seq[:-1]


def composition(k: int, seq: str) -> list:
    """
    Method that recovers the original sequence, giving as input values the obtained sequence and the value of k
    param k: size of the fragments
    param seq: sequence obtained
    :return: returns the original sequence in list
    """
    seq_original = [] #criar lista vazia da sequência original
    for i in range(len(seq) - k + 1): #percorre a sequência, subtraindo o tamanho do fragmento e incrementando + 1
        seq_original.append(seq[i:i + k]) #adiciona à lista o fragmento de tamanho k
    seq_original.sort() #ordenar a lista
    return seq_original