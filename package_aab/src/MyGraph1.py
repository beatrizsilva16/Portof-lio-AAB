from typing import Union


class MyGraph:

    def __init__(self, g: dict = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g
    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self) -> list:
        ''' Method that returns the list of nodes in the graph '''
        return list(self.graph.keys())

    def get_edges(self) -> list:
        ''' Method returning the list of arcs
        v represent the origin node
        d represent the destination node'''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d))
        return edges

    def size(self) -> tuple:
        ''' Method that returns the size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())

    ## add nodes and edges

    def add_vertex(self, v: Union[str, int, float]):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():  # checks if the vertex v is already in the graph's dictionary
            self.graph[v] = []  # adds the new vertex v to the graph by creating a new key in the graph dictionary
            # with the value of an empty list

    def add_edge(self, o: Union[str, int, float], d: Union[str, int, float]):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph
        :param o: represents the origin (starting) vertex
        :param d: represents the destination (ending) vertex of the edge
        '''
        # Check if origin vertex is already present in the graph
        if o not in self.graph.keys():  # se o não exista, é adicionado vertice o
            self.add_vertex(o)
        if d not in self.graph.keys():  # verifica se o vertice d está no dicionário, caso não esteja é adicionado
            self.add_vertex(d)
        if d not in self.graph[o]:  # verifica se o vertice d é um valor de vertice o
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v: Union[str, int, float]) -> list:
        """ Method for obtain successors of the given element"""
        return list(self.graph[v].keys())  # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v: Union[str, int, float]) -> list:
        """ Method to obtain predecessors of the given element"""
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v: Union[str, int, float]) -> list:
        """ Method to obtain adjacents of the given element """
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res

    ## degrees

    def out_degree(self, v: Union[str, int, float]) -> int:
        """ Method to obtain the number of out degree. Represents the number of successors/ramifications
            this node of the graph possesses """
        return len(self.graph[v])

    def in_degree(self, v: Union[str, int, float]) -> int:
        """Method to obtain the number of in degree. Represents the number of predecessors this node of the graph possesses"""
        return len(self.get_predecessors(v))

    def degree(self, v: Union[str, int, float]) -> int:
        """Method that calculates degree of node v (all adjacent nodes either forerunners or successors)"""
        return len(self.get_adjacents(v))

    ## BFS and DFS searches

    def reachable_bfs(self, v: Union[str, int, float]) -> list:
        """Method of nodes reachable from v
        starts with the source node, then visits all its successors, followed by its successors
        until all possible nodes are visited
        :param v: starting node
        :return: returns list of nodes reachable from v
        """
        # Initialize a list with the starting node v
        l = [v]
        # Initialize an empty list to store the reachable nodes
        res = []
        # Start a while loop that runs as long as there are nodes in l
        while len(l) > 0:
            # Remove the first node from the list l using pop(0) and assign it to the variable node
            node = l.pop(0)
            # If the node is not the starting node v, append it to the reachable nodes list res
            if node != v:
                res.append(node)
            # Loop over all the adjacent nodes elem of the node using the adjacency list self.graph[node]
            for elem in self.graph[node]:
                # If the adjacent node elem is not already in the reachable nodes list res, and
                # it is not in the queue l, and it is not equal to the current node, add it to the queue l
                if elem not in res and elem not in l and elem != node:
                    # If all the conditions are satisfied, add the adjacent node elem to the queue l
                    l.append(elem)
        # Return the reachable nodes list res
        return res

    def reachable_dfs(self, v: Union[str, int, float]) -> list:
        """Method of nodes reachable from v, from left to right (in depth)
        starts with the source node, explores its first successor, then its first successor
        until no further exploration is possible, then returns to explore more alternatives.
        :param v: node
        :return: returns list of nodes reachable from v"""
        # Initialize a list containing the starting node
        l = [v]
        # Initialize a list to store the nodes visited so far
        res = []
        # Continue as long as there are nodes in l
        while len(l) > 0:
            # Remove the first node from the list l using pop(0) and assign it to the variable node
            node = l.pop(0)
            if node != v: res.append(node)
            # Initialize a variable to keep track of the position to insert the next successor node
            s = 0
            # Iterate over all successors of the current node
            for elem in self.graph[node]:
                # If the successor node has not already been visited and is not already in l
                if elem not in res and elem not in l:
                    # Insert the successor node at the beginning of l
                    l.insert(s, elem)
                    # Increment the position counter (index)
                    s += 1
        # Return the list of visited nodes
        return res

    def distance(self, s: Union[str, int, float], d: Union[str, int, float]):
        """
        Method that calculates the distance between two nodes, s and d, in a graph represented as an adjacency list
        :param s: node s where the path begins
        :param d: node d where the path ends
        :return: returns the distance between the nodes s and d"""
        # Check if s and d are the same node
        if s == d:
            return 0

        queue = [(s, 0)]  # Use a queue instead of a list for better performance
        visited = set()  #  stores the visited nodes

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

    def shortest_path(self, s: Union[str, int, float], d: Union[str, int, float]):
        """Method that returns the shortest path between s and d (list of nodes it passes through)
        :param s: node s, node where the path begins
        :param d: node d, node where the path ends
        :return: return the shortest path, list of nodes it passes through"""
        # Check if s and d are the same node
        if s == d:
            return []
        # Initialize the list l with (s, []) and visited with s
        l = [(s, [])]
        visited = [s]
        # Loop while there are nodes in the list l
        while len(l) > 0:
            # Pop the first element of l and assign its node and predecessors to node and preds, respectively
            node, preds = l.pop(0)
            # Loop through each element elem in the adjacency list of node
            for elem in self.graph[node]:
                # Check if elem is the destination node d
                if elem == d:
                    # Return the predecessors plus the current node and d
                    return preds + [node, elem]
                # Check if elem has not been visited before
                elif elem not in visited:
                    # Append elem to visited and add (elem, preds + [node]) to the list l
                    l.append((elem, preds + [node]))
                    visited.append(elem)
        # If the loop completes without finding d, return None
        return None

    def reachable_with_dist(self, s: Union[str, int, float]) -> list:
        '''Method that returns a list of the reachable nodes from the given "s" and respective distance needed
        :param s: node s
        :return:  list of tuples of the reachable nodes and distance: (Node, Distance)
        '''
        # Initialize an empty list to store reachable nodes and distances
        res = []
        # Initialize a list with the starting node and distance 0
        l = [(s, 0)]
        # Loop until all reachable nodes have been processed
        while len(l) > 0:
            # Remove the first node from the list and its distance
            node, dist = l.pop(0)
            # If the node is not the starting node, add it to the result list
            if node != s:
                res.append((node, dist))
            # For each neighbor of the current node
            for elem in self.graph[node]:
                # If the neighbor is not already in the list of nodes to explore and not in the result list
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem):
                    # Add the neighbor to the list of nodes to explore with distance increased by 1
                    l.append((elem, dist + 1))
        # Return the list of reachable nodes and their distances
        return res

    ## cycles
    def node_has_cycle(self, v: Union[str, int, float]) -> bool:
        '''Method that verifies if a node has a cycle, i.e. if it starts and ends at the same node'''
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v:
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list(tl, val):
    res = False
    for (x, y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    gr.print_graph()
    print(gr.get_nodes())
    print(gr.get_edges())


def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)

    gr2.add_edge(1, 2)
    gr2.add_edge(2, 3)
    gr2.add_edge(3, 2)
    gr2.add_edge(3, 4)
    gr2.add_edge(4, 2)

    gr2.print_graph()


def test3():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    gr.print_graph()

    print(gr.get_successors(2))
    print(gr.get_predecessors(2))
    print(gr.get_adjacents(2))
    print(gr.in_degree(2))
    print(gr.out_degree(2))
    print(gr.degree(2))


def test4():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})

    print(gr.distance(1, 4))
    print(gr.distance(4, 3))

    print(gr.shortest_path(1, 4))
    print(gr.shortest_path(4, 3))

    print(gr.reachable_with_dist(1))
    print(gr.reachable_with_dist(3))

    gr2 = MyGraph({1: [2, 3], 2: [4], 3: [5], 4: [], 5: []})

    print(gr2.distance(2, 1))
    print(gr2.distance(1, 5))

    print(gr2.shortest_path(1, 5))
    print(gr2.shortest_path(2, 1))

    print(gr2.reachable_with_dist(1))
    print(gr2.reachable_with_dist(5))


def test5():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    print(gr.node_has_cycle(2))
    print(gr.node_has_cycle(1))
    print(gr.has_cycle())

    gr2 = MyGraph({1: [2, 3], 2: [4], 3: [5], 4: [], 5: []})
    print(gr2.node_has_cycle(1))
    print(gr2.has_cycle())


if __name__ == "__main__":
    test1()
    # test2()
    # test3()
    # test4()
    # test5()
