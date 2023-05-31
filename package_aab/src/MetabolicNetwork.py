from package_aab.src.MyGraph import MyGraph


class MetabolicNetwork(MyGraph):
    """
    Classe responsável pela implementação de redes metabólicas. As redes metabólicas são construídas através da leitura
    de um ficheiro que possui a informação sobre a rede.
    Esta classe é uma subclasse da MyGraph e, desta forma, herdará todos os métodos definidos na mesma.
    Há 3 tipos de rede metabólica, nomeadamente a:
        - Rede de Metabolitos ("metabolite-metabolite") -> rede na qual metabolitos são os nodos do grafo e os
    reações os arcos;
        - Rede de Reações ("reaction-reaction") -> rede na qual as reações são os nodos do grafo e os metabolitos são
    os arcos ;
        - Rede de Metabolitos e reações ("metabolite-reaction") -> rede na qual os metabolitos e as reações são nodos e
    os arcos indicam a sua interação.
    """

    def __init__(self, network_type="metabolite-reaction", split_rev=False):
        """
        Método construtor que guarda os valores utilizados nos restantes métodos
        :param network_type: tipo de rede metabólica
        :param split_rev: indica se as reações reversíveis são para serem consideradas como duas reações distintas
        (se True), sendo que como é dado como 'False' consideramos que não são duas reações distintas
        """
        MyGraph.__init__(self, {})
        self.net_type = network_type
        self.node_types = {} #dicionário com as listas de nodos de cada tipo
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = [] #lista com o nodos do tipo "metabolite"
            self.node_types["reaction"] = [] #lista com os nodos do tipo "reaction"
        self.split_rev = split_rev

    def add_vertex_type(self, v : str, nodetype : str):
        """
        Método que adiciona o nodo v ao dicionário node_types, conferindo se este já não existe
        :param v: nodo
        :param nodetype: tipo do nodo
        """
        self.add_vertex(v)
        self.node_types[nodetype].append(v)

    def get_nodes_type(self, node_type : str):
        """
        Método que retorna o dicionário com as listas de nodos de cada tipo
        :param node_type: tipo de nodo
        :return: se o node_type dado como input pertence ao dicionário node_types é retornado o mesmo
        se não, não retorna nada
        """
        if node_type in self.node_types:
            return self.node_types[node_type]
        else:
            return None

    def load_from_file(self, filename : str):
        """
        Método que recebe e abre um ficheiro criado anteriormente com as informações da rede metabólica e
        (onde cada reação será uma linha) e converte a informação do mesmo para ser introduzida nos
        atributos desta subcalsse. Exemplo de linha no ficheiro: "R1: M1 + M2 => M3 + M4"
        :param filename: nome do ficheiro que queremos abrir
        :return: caso haja um erro numa linha do ficheiro retorna a indicação que aquela linha é inválida
        """
        file = open(filename) #abre o ficheiro
        graph_mr = MetabolicNetwork("metabolite-reaction") #cria o grafo da rede metabólica do tipo metabolite-reaction
        for line in file: #para cada linha do ficheiro
            if ":" in line: #se houver ":" na linha
                tokens = line.split(":") #divide a linha desde os ":"
                reac_id = tokens[0].strip() #remove os caracteres antes e depois do id da reação
                graph_mr.add_vertex_type(reac_id, "reaction")
                #adiciona a reação ao dicionário node_types, identificando o tipo "reaction"
                reaction_line = tokens[1]
            else:
                raise Exception("Invalid line:") #se a linha não possuir ":" é uma linha inválida
            if "<=>" in reaction_line: #se houver "<=>" na linha da reação (reação reversível)
                left, right = rline.split("<=>") #divide a linha desde os "<=>" em "left" e "right"
                metabolites_left = left.split("+") #divide os metabolitos da esquerda desde o "+"
                for met in metabolites_left: #para cada metabolito na esqueda
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        graph_mr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    if self.split_rev: #True - se considerarmos a reação reversível como duas reações distintas
                        graph_mr.add_vertex_type(reac_id + "_b", "reaction")
                        #adiciona a reação b ao dicionário node_types, identificando o tipo "reaction"
                        graph_mr.add_edge(met_id, reac_id) #adiciona o arco da primeira reação (met_id,reac_id) ao grafo
                        graph_mr.add_edge(reac_id + "_b", met_id) #adiciona o arco reação b (met_id,reac_id) ao grafo
                    else: #False - se não considerarmos a reação reversível como duas reações distintas
                        graph_mr.add_edge(met_id, reac_id) #adiciona o arco da reação num sentido (met_id,reac_id) ao grafo
                        graph_mr.add_edge(reac_id, met_id) #adiciona o arco da reação noutro sentido(reac_id,met_id) ao grafo
                metabolites_right = right.split("+") #divide os metabolitos da direita desde o "+"
                for met in metabolites_right:#para cada metabolito na direita
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        graph_mr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    if self.split_rev: #True - se considerarmos a reação reversível como duas reações distintas
                        graph_mr.add_edge(met_id, reac_id + "_b") #adiciona o arco reação b (met_id,reac_id) ao grafo
                        graph_mr.add_edge(reac_id, met_id) #adiciona o arco da reação contrária (met_id,reac_id) ao grafo
                    else: #False - se não considerarmos a reação reversível como duas reações distintas
                        graph_mr.add_edge(met_id, reac_id) #adiciona o arco da reação num sentido (met_id,reac_id) ao grafo
                        graph_mr.add_edge(reac_id, met_id) #adiciona o arco da reação noutro sentido(reac_id,met_id) ao grafo
            elif "=>" in line: #se houver "=>" na linha da reação (reação irreversível)
                left, right = rline.split("=>") #divide a linha desde os "=>" em "left" e "right"
                metabolites_left = left.split("+") #divide os metabolitos da esquerda desde o "+"
                for met in metabolites_left: #para cada metabolito na esqueda
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        graph_mr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    graph_mr.add_edge(met_id, reac_id) #adiciona o arco da reação (met_id,reac_id) ao grafo
                metabolites_right = right.split("+") #divide os metabolitos da direita desde o "+"
                for met in metabolites_right: #para cada metabolito na direita
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        graph_mr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    graph_mr.add_edge(reac_id, met_id) #adiciona o arco da reação (met_id,reac_id) ao grafo
            else: #se a linha não possuir "<=>" ou "=>" é uma linha inválida
                raise Exception("Invalid line:")

        if self.net_type == "metabolite-reaction": #se a rede metabólica for do tipo metabolite-reaction
            self.graph = graph_mr.graph #cria o grafo graph_mr da rede metabólica do tipo metabolite-reaction
            self.node_types = graph_mr.node_types  #dicionário com as listas de nodos de cada tipo
        elif self.net_type == "metabolite-metabolite": #se a rede metabólica for do tipo metabolite-metabolite
            self.convert_metabolite_net(graph_mr) #converter o grafo graph_mr para um grafo apenas de metabolitos
        elif self.net_type == "reaction-reaction": #se a rede metabólica for do tipo reaction-reaction
            self.convert_reaction_graph(graph_mr) #converter o grafo graph_mr para um grafo apenas de reações
        else: #se não tiver um tipo atribuído
            self.graph = {} #dicionário que guarda o grafo

    def convert_metabolite_net(self, graph_mr : dict):
        """
        Método para converter o graph_mr num grafo de uma rede metabólica do tipo "metabolite-metabolite"
        :param graph_mr: grafo da rede metabólica do tipo metabolite-reaction
        """
        for m in graph_mr.node_types["metabolite"]:
            #para cada nodo do grafo que representa o tipo "metabolite" na lista desse tipo no dicionário node_types
            self.add_vertex(m) #adiciona cada nodo do tipo "metabolite", verificando se ainda não existe no grafo
            sucessors = graph_mr.get_sucessors(m) #obtém a lista de nodos sucessores de cada nodo do tipo "metabolite"
            for s in sucessors: #para cada sucessor
                sucessors_r = graph_mr.get_successors(s) #obtém a lista de sucessores do sucessor
                for s2 in sucessors_r: #para cada sucessor do sucessor
                    if m != s2: #se o nodo do tipo "metabolite" for diferente do sucessor do sucessor
                        self.add_edge(m,s2) #adiciona o arco entre os dois metabolitos, o m e o s2

    def convert_reaction_graph(self, graph_mr : dict):
        """
        Método para converter o graph_mr num grafo de uma rede metabólica do tipo "reaction-reaction"
        :param graph_mr: grafo da rede metabólica do tipo metabolite-reaction
        """
        for r in graph_mr.node_types["reaction"]:
            #para cada nodo do grafo que representa o tipo "reaction" na lista desse tipo no dicionário node_types
            self.add_vertex(r) #adiciona cada nodo do tipo "reaction", verificando se ainda não existe no grafo
            sucessors = graph_mr.get_sucessors(r)  # obtém a lista de nodos sucessores de cada nodo do tipo "reaction"
            for s in sucessors:  # para cada sucessor
                sucessors_r = graph_mr.get_successors(s)  # obtém a lista de sucessores do sucessor
                for s2 in sucessors_r:  # para cada sucessor do sucessor
                    if r != s2:  # se o nodo do tipo "reaction" for diferente do sucessor do sucessor
                        self.add_edge(r, s2)  # adiciona o arco de reação entre o r e o s2
