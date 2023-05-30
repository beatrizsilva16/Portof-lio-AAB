class MyGraph:
    """
    Class for implementation of graphs. Class MyGraph is a parent class of different
    ones such as: MetabolicNetwork, OverlapGraph and DeBruijnGraph. This class essentially builds
    graphs with a given dictionary of values or strings.
    """
    def __init__(self, g: dict = {}):
        """
        Constructor - takes dictionary to fill the graph as input; default is empty dictionary
        :param g: dictionary that stores the graph
        """
        self.graph = g

    def print_graph(self):
        """
        Method that prints the content of the graph as adjacency list
        """
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    def get_nodes(self) -> list:
        """
        Method that obtain list of nodes in the graph
        """
        return list(self.graph.keys())

# Basic info

    def get_edges(self) -> list:
        """
        Method that gets the edges in the graph as a list of tuples (origin, destination)
        v represent the origin
        d represent the destination
        """
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d)) #os arcos são o par de nodos anterior e seguinte
        return edges

    def size(self):
        """
        Method that obtains the size of the graph: number of nodes and number of edges
        """

        return len(self.get_nodes()), len(self.get_edges())

# add nodes and edges
    def add_vertex(self, v: str):
        """
        Method that adds a vertex to the graph and tests if vertex exists or not, adding if True
        :param v: element to add in the graph
        """
        if v not in self.graph.keys(): #caso v não exista, é adicionado
            self.graph[v] = []

    def add_edge(self, o: str, d: str):
        """
        Method that add edge to the graph; if vertices do not exist, they are added to the graph
        :param o: vertice do arco
        :param d: vertice do arco
        :return:
        """
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys(): #se o não exista, é adicionado vertice o
            self.add_vertex(o)
        if d not in self.graph.keys(): #verifica se o vertice d está no dicionário, caso não esteja é adicionado
            self.add_vertex(d)
        if d not in self.graph[o]: #verifica se o vertice d é um valor de vertice o
            self.graph[o].append(d) #adiciona o valor d ao o


## successors, predecessors, adjacent nodes

    def get_successors(self, v:str):
        """
        Method that obtains the successors of the given element
        :param v: node
        :return: returns a list of successor nodes of node v
        """
        return list(
            self.graph[v])

    def get_predecessors(self, v:str) -> list:
        """
        Method that obtains predecessors of the given element
        :param v: node
        :return: returns a list of predecessor nodes of node v
        """
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v:str) -> list:
        """
        Method that obtains adjacents of the given element
        :param v: node
        :return: returns the list of nodes adjacent to node v
        """
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res

    ## degrees
    def out_degree(self, v:str) -> int:
        """
        Method that obtains the number of out degree. Represents the number
        of successors/ramifications this node of the graph possesses
        :param v: node
        :return: returns degree of exit from node
        """
        return len(self.graph[v])

    def in_degree(self, v:str) -> int:
        """
        Method that obtains number of in degree. Represents the number of
        predecessors this node of the graph possesses
        :param v: nodo
        :return: returns degree of entry from node
        """
        return len(self.get_predecessors(v))

    def degree(self, v:str) -> int:
        """
        Method that obtains the number of degree. Represents the number
        adjacentes nodes of the given one
        :param v: node
        :return: returns degree of node v
        """
        return len(self.get_adjacents(v))

    def all_degrees(self, deg_type="inout") -> dict:
        """
        Method that computes the degree (of a given type) for all nodes.
         "Deg_type" can be "in", "out", or "inout"
        :param deg_type: tipo de grau (entrada, saída ou ambos)
        :return: returns the degrees
        """
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout": #Se for graus de saida ou de entrada e saída
                degs[v] = len(self.graph[v]) #
            else:
                degs[v] = 0
        if deg_type == "in" or deg_type == "inout": #Se for graus de entrada ou de entrada e saída
            for v in self.graph.keys(): #para cada key no grafo
                for d in self.graph[v]: #para cada valor de v
                    if deg_type == "in" or v not in self.graph[d]: #Se for graus de entrada ou v não for um valor de d no grafo
                        degs[d] = degs[d] + 1   #adiciona +1 ao valor de d
        return degs

    def highest_degrees(self, all_deg=None, deg_type="inout", top=10) ->list:
        """
        Method that calculates higher degrees
        param all_deg: input and output grades, or both
        param deg_type: degree type (input, output or both)
        :return: list of the highest degrees
        """
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_deg[:top]))


    def mean_degree(self, deg_type="inout") -> dict:
        """
        Method to calculate the average degrees
        :param deg_type: type of degree (input, output or both)
        :return: returns the average degrees
        """
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))

    def prob_degree(self, deg_type="inout") -> dict:
        """
        Method for calculating degree probability
        :param deg_type: type of degree (input, output or both)
        :return: returns the probability of degrees
        """
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res

## BFS and DFS searches

    def reachable_bfs(self, v):
        """Method of nodes reachable from v
        starts with the source node, then visits all its successors, followed by its successors
        until all possible nodes are visited
        :param v: starting node
        :return: returns list of nodes reachable from v
        """
        l = [v]
        res = []
        while len(l) > 0: #enquanto há elementos na lista l
            node = l.pop(0) #isolar o primeiro elemento da lista l, queue de nodos
            if node != v: res.append(node) #se o nodo for diferente de v, adicionar o nodo a res
            for elem in self.graph[node]: #para todos os sucessores do nodo
                if elem not in res and elem not in l and elem != node: #se não existe em res e em l e se o sucessor é diferente do nodo
                    l.append(elem) #adicionar na queue para verificar
        return res

    def reachable_dfs(self, v):
        """Method of nodes reachable from v, from left to right (in depth)
        starts with the source node, explores its first successor, then its first successor
        until no further exploration is possible, then returns to explore more alternatives.
        :param v: node
        :return: returns list of nodes reachable from v
        """
        l = [v]
        res = []
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodos
            node = l.pop(0) #isolar o primeiro elemento da lista l
            if node != v: res.append(node) #se o nodo for diferente de v, adicionar o nodo a res
            s = 0 #ira ser usado para criar o stack//é reposto a 0 antes do loop for abaixo
            for elem in self.graph[node]: #para todos os sucessores do nodo
                if elem not in res and elem not in l: #se não existe em res e em l e se o sucessor é diferente do nodo
                    l.insert(s, elem) #cria um stack/vai voltar a verificar o mais recente/insere no inicio da lista
                    s += 1 #caso haja multiplos sucessores, o s vai aumentar de forma a colocar as proximas iteraçoes na posicao depois da iteraçao anterior (stack)
        return res

    def distance(self, s, d):
        """
        Method that calculates the distance between two nodes, s and d, in a graph represented as an adjacency list
        :param s: node s where the path begins
        :param d: node d where the path ends
        :return: returns the distance between the nodes s and d
        """
        # Check if s and d are the same node
        if s == d:
            return 0
        queue = [(s, 0)]  # Use a queue instead of a list for better performance
        visited = set()  # stores the visited nodes
        while queue:
            node, dist = queue.pop(0)  # Take the first element from the queue
            if node in visited:  # Skip processing if node has been visited before
                continue
            visited.add(node)  # Mark node as visited
            if node == d:  # Check if the current node is the destination node
                return dist
            for neighbor in self.graph[node]:  # Explore neighbors of the current node
                if neighbor not in visited:  # Check if the neighbor has not been visited
                    queue.append((neighbor, dist + 1))  # Add neighbor to the queue with updated distance
        # If the loop completes without finding the destination node, return None
        return None

    def shortest_path(self, s, d):
        """Method that returns the shortest path between s and d (list of nodes it passes through)
        :param s: node s, node where the path begins
        :param d: node d, node where the path ends
        :return: return the shortest path, list of nodes it passes through"""
        if s == d:
            return []
        l = [(s, [])] #lista com um tuplo com o nodo e o caminho
        visited = [s] #nodos visitados
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds + [node, elem]
                elif elem not in visited:
                    l.append((elem, preds + [node]))
                    visited.append(elem)
        return None

    def reachable_with_dist(self, s: str):
        """Method that returns a list of the reachable nodes from the given "s" and respective distance needed
        :param s: node s
        :return:  list of tuples of the reachable nodes and distance: (Node, Distance)
        """
        res = []
        l = [(s, 0)] #lista com tuplo com s e distância de s a s(0)
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodos
            node, dist = l.pop(0)
            if node != s: #se nodo for diferente de s
                res.append((node, dist)) #não conta o s
            for elem in self.graph[node]: #para
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem): # vai ver se o p se encontra dentro de l ou em res
                    l.append((elem, dist + 1)) # adiciona o vertice a que se liga
        return res

    def mean_distances(self):
        """
        Method that calculates the cverage distance dethod for Each Node
        :return: returns the average distance and the proportion of nodes reachable
        """
        total = 0
        num_reachable = 0 #números de nodos no grafo ligados entre si
        for k in self.graph.keys(): #para cada key no grafo
            distsk = self.reachable_with_dist(k) #a lista correspondente aos nodos atingidos e a respetiva distância
            for _, dist in distsk: #para cada carater correspondente à distancia na lista
                total += dist #vamos adicionar o valor da distância ao total
            num_reachable += len(distsk) #número de nodos atingidos vai corresponder ao comprimento da lista (distsk) obtida, todas as ligações entre todos os nodos
        meandist = float(total) / num_reachable #média da distancia total dos nodos atingidos
        n = len(self.get_nodes()) #número total de nodos
        return meandist, float(num_reachable) / ((n - 1) * n)

    def closeness_centrality(self, node: str):
        """
        Method of averaging approach to distances travelled between affected nodes
        :param node: node
        :return: returns the average distance between affected nodes
        """
        dist = self.reachable_with_dist(node) #a lista correspondente aos nodos atingidos e a respetiva distância
        if len(dist) == 0: #se o número de nodos atingidos for igual a 0
            return 0.0 #retorna 0
        s = 0.0
        for d in dist: s += d[1] #para cada nodo é adicionada a distância à variavel s
        return len(dist) / s

    def highest_closeness(self, top=10) -> list:
        cc = {} #dicionário
        for k in self.graph.keys(): #para cada key no grafo
            cc[k] = self.closeness_centrality(k) #nodo corresponde
        ord_cl = sorted(list(cc.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_cl[:top]))

    def betweenness_centrality(self, node) -> float:
        total_sp = 0
        sps_with_node = 0
        for s in self.graph.keys():
            for t in self.graph.keys():
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)
                    if sp is not None:
                        total_sp += 1
                        if node in sp: sps_with_node += 1
        return sps_with_node / total_sp

    ## cycles
    def node_has_cycle(self, v):
        """
        Method to check if the node has a cycle, that is if it begins and ends in the same node
        :param v: node
        :return: value of "False" or "True" if the node has no cycle or has a cycle, respectively
        """
        l = [v] #vai buscar o nodo v e cria uma lista
        res = False
        visited = [v] #lista de nodos visitados
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodos
            node = l.pop(0) #isolar o primeiro elemento da lista l
            for elem in self.graph[node]: #para cada elemento vai buscar ao grafo (dicionário) o nodo adjacente
                if elem == v:   #se o elemento da lista corresponder ao nodo
                    return True
                elif elem not in visited: #caso o elemento da lista não corresponder ao nodo visitado
                    l.append(elem) #adiciona o elemento à lista l
                    visited.append(elem) #adiciona o elemento à lista de nodos visitados
        return res #retorna False

    def has_cycle(self) -> bool:
        """
        Method that checks if the graph has a loop, that is if the path is closed
        :return: value of "False" or "True" if the path is not closed or closed, respectively.
        """
        res = False
        for v in self.graph.keys():  #para cada nodo vai buscar ao grafo (dicionário) o nodo adjacente
            if self.node_has_cycle(v): #se o nodo tiver ciclo
                return True
        return res #retorna False

    ## clustering

    def clustering_coef(self, v) -> float:
        """
        Clustering coefficient calculation method, to measure the extent to which each node is embedded in a cohesive group
        :param v: node
        :return: clustering coefficient
        """
        adjs = self.get_adjacents(v) #lista de nodos adjacentes
        if len(adjs) <= 1: #se o número de nodos adjacentes for inferior ou igual a 1, só terá 1 ou 0 nodos adjacentes
            return 0.0 #logo, não tem nodos suficientes para formar pares
        ligs = 0
        for i in adjs: #para cada nodo i (anterior) adjacente
            for j in adjs: #para cada nodo j (seguinte) adjacente
                if i != j: #se nodo i diferente de nodo j
                    if j in self.graph[i] or i in self.graph[j]: #se nodo j estiver no grafo adjacente a i ou i estiver no grafo adjacente a j
                        ligs = ligs + 1
        return float(ligs) / (len(adjs) * (len(adjs) - 1))
        #o número de pares de nodos adjacentes a dividir pelo número de pares que é possivel serem formados

    def all_clustering_coefs(self) -> dict:
        """
        Method that calculates all coefficients
        :return: dictionary of coefficients of each node where the key corresponds to each node and each coefficient
        """
        ccs = {} #dicionário de coeficientes
        for k in self.graph.keys(): #para cada key no grafo
            ccs[k] = self.clustering_coef(k)
            #cálculo do coeficiente de cada nodo, valor adicionado no dicionário ccs
        return ccs

    def mean_clustering_coef(self) -> float:
        """
        Method of the global average of coefficients
        :return: the value of the average of all coefficients
        """
        ccs = self.all_clustering_coefs() #cálculo de todos os coeficientes
        return sum(ccs.values()) / float(len(ccs)) #cálculo da média

    def mean_clustering_perdegree(self, deg_type="inout") -> dict:
        """
        Method that calculates values for the average of coefficients for all nodes
        :param deg_type: type of degree (input, output or both)
        :return: returns the dictionary of nodes and their coefficient
        """
        degs = self.all_degrees(deg_type) #graus de entrada e saída, ou ambos para todos os nodos do grafo
        ccs = self.all_clustering_coefs() #coeficiente de todos os nodos em dicionário
        degs_k = {} #dicionário de grau k
        for k in degs.keys(): #para cada k grau
            if degs[k] in degs_k.keys(): #se cada grau k de entrada e saída, ou ambos está dentro
                degs_k[degs[k]].append(k) #o que estava no dicionário passa para uma lista
            else: #senão
                degs_k[degs[k]] = [k] #grau k permanece no dicionário
        ck = {} #dicionário da média dos coeficientes considerando nodos de grau k.
        for k in degs_k.keys():#para cada k grau
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            #para grau v calcular o total, o coeficiente de todos os nodos (dicionário)
            ck[k] = float(tot) / len(degs_k[k])
            #calcula o coeficiente a dividir pelo comprimento do grau k
        return ck

    ## Hamiltonian

    def check_if_valid_path(self, p:list) -> bool:
        """
        Method of checking if path is correct
        :param p:path
        :return: value of "False" or "True" if path is invalid or valid, respectively.
        """
        if p[0] not in self.graph.keys(): #se o primeiro nodo do caminho não pertencer ao grafo
            return False #caminho inválido
        for i in range(1, len(p)): #para cada nodo no caminho
            if p[i] not in self.graph.keys() or p[i] not in self.graph[p[i - 1]]:
                #se o nodo não pertencer ao grafo ou não for o primeiro no caminho
                return False #caminho inválido
        return True #caminho válido

    def check_if_hamiltonian_path(self, p:list) -> bool:
        """
        Method checking if path is Hamiltonian
        :param p: path
        :return: value of "False" or "True" if the Hamiltonian path is invalid or valid, respectively.
        """
        if not self.check_if_valid_path(p):  # se não for um caminho válido
            return False
        to_visit = list(self.get_nodes())  # lista dos nodos a visitar
        if len(p) != len(to_visit):  # verifica se o número de nodos do caminho for diferente do número de nodos a visitar
            return False
        for i in range(len(p)):  # para cada nodo no caminho
        # verifica se os nodos no caminho e na lista a visitar são iguais
            if p[i] in to_visit:  # se o nodo tiver na lista a visitar
                to_visit.remove(p[i])  #remove da lista dos nodos a visitar
                return False
        if not to_visit: #caso contrário,se os nodos na lista de nodos não tiverem presentes na lista a visitar
            return True # é um caminho hamiltonian pois passou por todos os nodos e não existem mais nodos a visitar
        else: #se houver nodos na lista a visitar
            return False #não é um caminho hamiltonian

    def search_hamiltonian_path(self):
        """"
        Hamiltonian pathfinding method
        :return: if p is different from None returns p otherwise returns None
        """
        for ke in self.graph.keys(): #para cada key no grafo
            p = self.search_hamiltonian_path_from_node(ke)
            if p != None:
                return p
        return None

    def search_hamiltonian_path_from_node(self, start : int):
        """
        Hamiltonian pathfinding method on the graph
        :param start: initial node
        :return: Hamiltonian path in list
        """
        current = start #para iniciar o nodo atual tem de ser o nodo inicial
        visited = {start: 0}
        #dicionário em que as key é o nodo atual e os values o index
        path = [start] #caminho em lista dos nodos
        while len(path) < len(self.get_nodes()):
        #enquanto o caminho for menor que o número de nodos do grafo
            nxt_index = visited[current] #o proximo index corresponde ao index atual
            if len(self.graph[current]) > nxt_index:
            #se o comprimento do grafo até ao nodo atual for superior ao próximo index
                nxtnode = self.graph[current][nxt_index]
                #o próximo nodo é o nodo adjacente ao nodo atual
                visited[current] += 1
                #para percorrer todos os nodos adjacente ao nodo atual
                if nxtnode not in path:
                #se o próximo nodo não tiver no caminho (lista)
                    path.append(nxtnode)
                    #adicionar à lista path o próximo nodo
                    visited[nxtnode] = 0
                    #adicionar o nodo adjacente que visitamos ao dicionário de nodos visitados
                    #e guarda o valor como zero para ler os nodos adjacentes a partir da primeira posição
                    current = nxtnode
                    #o nodo atual passa a ser o próximo nodo
            else: #se não
                if len(path) > 1:
                #se houver um caminho,ou seja, o comprimento da lista for maior que um
                    rmvnode = path.pop() #remove o nodo da lista path e retorna o nodo removido
                    del visited[rmvnode] #elimina o nodo removido do diciónario de nodos visitados
                    current = path[-1] #inicia a nova procura de um caminho a partir do ultimo nodo da lista
                else: #senão
                    return None
        return path #caminho hamiltonianos em lista

    # Eulerian
        #Caminho que passa por todos os arcos do grafo exatamente uma vez

    def check_balanced_node(self, node) -> bool:
        """
        Method to check if a node is balanced
        :param node: node
        :return: value of "False" or "True", if the node's input degree is not equal/or is equal to the node's output degree, respectively
        """
        return self.in_degree(node) == self.out_degree(node)

    def check_balanced_graph(self) -> bool:
        """
        Checking method if the graph is balanced
        return:value of "False" or "True", if the graph is unbalanced or balanced, respectively
        """
        for n in self.graph.keys(): #para cada key do grafo
            if not self.check_balanced_node(n): #se não for um nó balanceado
                return False
        return True

    def check_nearly_balanced_graph(self):
        """
        Method to check if the graph is semi-balanced
        :return: returns none (if the graph is not semi-balanced) or the tuples
        """
        res = None, None #forma um tuplo
        for n in self.graph.keys(): #para cada key do grafo
            indeg = self.in_degree(n) #indeg vai corresponder ao indice do grau de entrada
            outdeg = self.out_degree(n) #outdeg vai corresponder ao indice do grau de saída
            if indeg - outdeg == 1 and res[1] is None:
            #se o grau de entrada a subtrair pelo de saída corresponder a 1 e o tuplo de indice 1 for none
                res = res[0], n #o tuplo vai passar o ter o valor de n
            elif indeg - outdeg == -1 and res[0] is None:
            #se o grau de entrada a subtrair pelo de saída corresponder a -1  e o tuplo de indice 0 for none
                res = n, res[1] #vai subtituir o valor de n no tuplo de indice 0
            elif indeg == outdeg:
            #se o grau de entrada e saída forem iguais
                pass #passa
            else:
                return None, None
        return res

    def is_connected(self) -> bool:
        """
        Method for checking whether it is connected or not
        :return: value of "False" or "True", if not connected or connected, respectively
        """
        total = len(self.graph.keys()) - 1
        for v in self.graph.keys(): #para cada key do grafo
            reachable_v = self.reachable_bfs(v) #lista de nodos atingíveis a partir de v
            if (len(reachable_v) < total):
                return False
        return True

    def eulerian_cycle(self):
        """
        Eulerian cycle passes through all arcs of the examining graph once, returning to the starting node
        :return: value of "None" (if not an Eulerian cycle) or the list res (cycle list)
        """
        if not self.is_connected() or not self.check_balanced_graph():
        #se não estiver conetado ou não o grafo não tiver balanceado, ou seja verifica se é Euleriano
            return None
        edges_visit = list(self.get_edges()) #arcos a visitar vai ser a lista de arcos
        res = [] #lista vazia
        while edges_visit: #enquanto os arcos a visitar
            pair = edges_visit[0]
            #par dos nodos correspondentes a arcos a visitar do grafo
            # vai buscar no tuplo da primeira posição da lista de arcos
            i = 1 #define o index como 1, para mudar a posição
            if res != []: #se a lista não for vazia
                while pair[0] not in res: #enquanto o primeiro par de nodos não tiver na lista correspondente ao ciclo
                    pair = edges_visit[i] #guarda o par de nodos da posição i
                    i = i + 1 #incrementa o index da lista de par de nodos para ir lendo a lista
            edges_visit.remove(pair) #remove o par da lista de arcos a visitar porque vai visitar
            start, nxt = pair #pega no par de nodos e define o primeiro nodo como o start e o segundo nodo como o nxt
            cycle = [start, nxt] #lista do ciclo em que o star é o nodo inicial e o nxt é o último nodo
            while nxt != start: #enquanto o próximo for diferente do inicial, para andar para a frente no grafo
                for adj in self.graph[nxt]: #itera cada nodo adjacente ao próximo nodo
                    if (nxt, adj) in edges_visit: #verifica se o próximo nodo e o nodo adjacente têm um arco
                        pair = (nxt, adj) #se sim, define como arco
                        nxt = adj #define o adjacente como próximo.
                        cycle.append(nxt) #adiciona o próximo nodo ao ciclo.
                        edges_visit.remove(pair) #remove o par acabado de visitar
            if not res: #se a lista for vazia
                res = cycle #a lista de nodos do ciclo passa a ser a lista de resolução
            else: #caso já tenha conteúdo
                pos = res.index(cycle[0]) #cria a variavel pos, indice do ciclo na primeira posição
                for i in range(len(cycle) - 1): #itera as posições dos nodos na lista cycle
                    res.insert(pos + i + 1, cycle[i + 1])
                    #insere na lista res na dada posição (pos+i+1) o nodo da lista cycle(da posição i+1)
        return res


    def eulerian_path(self):
        """
        Eulerian path method, if existent
        :return: returns the path
        """
        unb = self.check_nearly_balanced_graph()
        if unb[0] is None or unb[1] is None:
            return None #se não houver pontos semibalanciados não há caminho
        self.graph[unb[1]].append(unb[0])
        cycle = self.eulerian_cycle() #função do ciclo euleriano
        for i in range(len(cycle) - 1): #itera as posições dos nós
            if cycle[i] == unb[1] and cycle[i + 1] == unb[0]:
            #quando o nó da lista cycle na posição i for igual ao segundo nodo semibalanceado e
            # o nó seguinte for igual ao primeiro nodo semibalanceado
                break #quebra o loop
        path = cycle[i + 1:] + cycle[1:i + 1]
        #o path fica os nodos do ciclo começando na posição i+1 e
        # os nodos desde a segunda posição até i+1
        return path


def is_in_tuple_list(tl, val) -> bool:
    res = False
    for (x, y) in tl:
        if val == x:
            return True
    return res