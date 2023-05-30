from MyGraph import MyGraph


class MetabolicNetwork (MyGraph):
    """Subclass of MyGraph that creates a graph with metabolites
    and reactions indicating the type of network construction
    :param: network_type : str, optional
         Informs the type of graph network the algorithm is working with, by default "metabolite-reaction"
            "metabolite-reaction": Graph with metabolites and reactions occuring
            "metabolite-metabolite": Graph with the metabolite that origin others
            "reaction-reaction": Graph with all the reactions that induce others to happen"""
    
    def __init__(self, network_type: str = "metabolite-reaction", split_rev: bool = False):
        """
        Constructor method that saves the values used in the other methods
        param network_type: metabolic network type
        :param split_rev: indicates if the reversible reactions are to be considered as two distinct reactions
        (if True), since it is given as 'False' we consider that they are not two distinct reactions
        :param network_type:
        :param split_rev:
        """
        MyGraph.__init__(self, {})  # Initialize the parent class MyGraph
        self.net_type = network_type  # Save the network type
        self.node_types = {}  # Initialize an empty dictionary to store node types

        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = []  # Create an empty list for metabolite nodes
            self.node_types["reaction"] = []  # Create an empty list for reaction nodes
        self.split_rev = split_rev
    
    def add_vertex_type(self, v: str, nodetype: str) -> list:
        """
        Method that adds node v to the node_types dictionary, checking that it doesn't already exist
        :param v: node to be added
        :param nodetype: vertex type, only "metabolite" or "reaction" supported
        """
        self.add_vertex(v)
        self.node_types[nodetype].append(v)
    
    def get_nodes_type(self, node_type: str) -> list:
        """ Method returning the dictionary with the lists of nodes of each type
        param node_type: node type
        :return: if the node_type given as input belongs to the node_types dictionary it is returned
        if not, returns nothing
        """
        if node_type not in ["metabolite", "reaction"]:
            raise AssertionError("Node type given is not supported")
        if node_type in self.node_types:
            return self.node_types[node_type]
        else:
            return None

    def load_from_file(self, filename: str):
        '''
        Method that loads the content of a file into the graph.

        :param filename: File name with the content to be loaded into the graph.
                         The file should follow specific content restrictions.

        :return: If there is an error on a line of the file, it returns an indication that the line is invalid.
        '''

        rf = open(filename)  # Open the file for reading
        gmr = MetabolicNetwork("metabolite-reaction")  # Create a new MetabolicNetwork object

        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
                # If the line contains a colon (":"), split it into tokens and process the reaction information
            else:
                raise Exception("Invalid line:")
                # If the line does not contain a colon, raise an Exception indicating an invalid line

            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id + "_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id + "_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id + "_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                # If the line contains "<=>", split it into left and right parts, and process the metabolites and edges accordingly
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
                # If the line contains "=>", split it into left and right parts, and process the metabolites and edges accordingly
            else:
                raise Exception("Invalid line:")
                # If the line does not contain "<=>" or "=>", raise an Exception indicating an invalid line

        # Based on self.net_type, convert the gmr object to the desired network type or assign it to self.graph
        if self.net_type == "metabolite-reaction":  # se a rede metabólica for do tipo metabolite-reaction
            self.graph = gmr.graph  # cria o grafo graph_mr da rede metabólica do tipo metabolite-reaction
            self.node_types = gmr.node_types  # dicionário com as listas de nodos de cada tipo
        elif self.net_type == "metabolite-metabolite":  # se a rede metabólica for do tipo metabolite-metabolite
            self.convert_metabolite_net(gmr)  # converter o grafo graph_mr para um grafo apenas de metabolitos
        elif self.net_type == "reaction-reaction":  # se a rede metabólica for do tipo reaction-reaction
            self.convert_reaction_graph(gmr)  # converter o grafo graph_mr para um grafo apenas de reações
        else:  # se não tiver um tipo atribuído
            self.graph = {}  # dicionário que guarda o grafo

    def convert_metabolite_net(self, gmr: dict):
        """Method to convert gmr to a metabolite-metabolite network graph
        :param graph_mr: graph of metabolite-reaction metabolic network"""

        for m in gmr.node_types["metabolite"]:
            self.add_vertex(m)
        sucs = gmr.get_successors(m)
        for s in sucs:
            sucs_r = gmr.get_successors(s)
        for s2 in sucs_r:
            if m != s2:
                self.add_edge(m, s2)
        
    def convert_reaction_graph(self, gmr: dict):
        for r in gmr.node_types["reaction"]:
            pass


