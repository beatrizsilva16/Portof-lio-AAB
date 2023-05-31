from package_aab.src.MyGraph import MyGraph


class OverlapGraph(MyGraph):
    """
    A classe OverlapGraph será uma sub-classe da classe MyGraph para representar grafos orientados
    """

    def __init__(self, frags: list, reps:bool = False):
        MyGraph.__init__(self, {})
        if reps:
            self.create_overlap_graph_with_reps(frags)
        else:
            self.create_overlap_graph(frags)
        self.reps = reps

    def create_overlap_graph(self, frags:list):
        """
        Método para criar o grafo de overlap a partir das ligações do sufixos com os prefixos
        :param frags: fragmentos ou conjuntos de sequencias
        """
        for seq in frags:
            self.add_vertex(seq) #adiciona vertices
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf: #serve para definir os arcos
                    self.add_edge(seq, seq2) #adiciona arcos


    def create_overlap_graph_with_reps(self, frags:list):
        """
        Método para criar grafo de overlap com repetições de elementos
        :param frags: fragmentos ou conjuntos de sequencias
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

    def get_instances(self, seq:str) -> list:
        """
        :param seq: sequencia
        :return: a lista da sequencia
        """
        res = []
        for k in self.graph.keys():
            if seq in k: res.append(k)
        return res

    def get_seq(self, node:str):
        """
        Método que retorna o nodo
        :param node: nodo
        :return: se o nodo não tiver presente no grafo retorna None,
        """
        if node not in self.graph.keys():
            return None
        if self.reps:
            return node.split("-")[0]
        else:
            return node

    def seq_from_path(self, path:list):
        """
        Método para dar a sequencia contruida dado um caminho no grafo
        :param path: caminho
        :return: se o caminho não é hamiltonian retorna None, retorna seq
        """
        if not self.check_if_hamiltonian_path(path):
            return None
        seq = self.get_seq(path[0])
        for i in range(1, len(path)):
            nxt = self.get_seq(path[i])
            seq += nxt[-1]
        return seq

#funções auxiliares
def composition(k : int, seq : str) -> list:
    """
    Método da composição
    :param k: valor de k, numero de nucléotidos
    :param seq: sequencia
    :return: a lista separando por k nucleótidos
    """
    res = []
    for i in range(len(seq) - k + 1):
        res.append(seq[i:i + k])
    res.sort()
    return res


def suffix(seq : str) -> list:
    """
    Método do sufixo
    :param seq: sequencia
    :return: a sequencia sem o primeiro elemento
    """
    return seq[1:]


def prefix(seq : str) -> list:
    """
    Método do prefixo
    :param seq: sequencia
    :return: a sequencia sem o ultimo nucleotido
    """
    return seq[:-1]