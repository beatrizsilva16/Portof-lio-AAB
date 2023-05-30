def test1():
    m = MetabolicNetwork("metabolite-reaction")
    m.add_vertex_type("R1", "reaction")
    m.add_vertex_type("R2", "reaction")
    m.add_vertex_type("R3", "reaction")
    m.add_vertex_type("M1", "metabolite")
    m.add_vertex_type("M2", "metabolite")
    m.add_vertex_type("M3", "metabolite")
    m.add_vertex_type("M4", "metabolite")
    m.add_vertex_type("M5", "metabolite")
    m.add_vertex_type("M6", "metabolite")
    m.add_edge("M1", "R1")
    m.add_edge("M2", "R1")
    m.add_edge("R1", "M3")
    m.add_edge("R1", "M4")
    m.add_edge("M4", "R2")
    m.add_edge("M6", "R2")
    m.add_edge("R2", "M3")
    m.add_edge("M4", "R3")
    m.add_edge("M5", "R3")
    m.add_edge("R3", "M6")
    m.add_edge("R3", "M4")
    m.add_edge("R3", "M5")
    m.add_edge("M6", "R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction"))
    print("Metabolites: ", m.get_nodes_type("metabolite"))


def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction"))
    print("Metabolites: ", mrn.get_nodes_type("metabolite"))
    print()

    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("example-net.txt")
    mmn.print_graph()
    print()

    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("example-net.txt")
    rrn.print_graph()
    print()

    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("example-net.txt")
    mrsn.print_graph()
    print()

    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("example-net.txt")
    rrsn.print_graph()
    print()


test1()
print()
test2()

