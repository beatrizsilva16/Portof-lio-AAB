import unittest
from package_aab.src.MyGraph import MyGraph
from package_aab.src.MetabolicNetwork import MetabolicNetwork
from unittest.mock import MagicMock, Mock

class test_MetabolicNetwork(unittest.TestCase):
    def setUp(self):
        self.m = MetabolicNetwork("metabolite-reaction")
        self.v1 = self.m.add_vertex_type("R1", "reaction")
        self.v2 = self.m.add_vertex_type("R2", "reaction")
        self.v3 = self.m.add_vertex_type("R3", "reaction")
        self.v4 = self.m.add_vertex_type("M1", "metabolite")
        self.v5 = self.m.add_vertex_type("M2", "metabolite")
        self.v6 = self.m.add_vertex_type("M3", "metabolite")
        self.v7 = self.m.add_vertex_type("M4", "metabolite")
        self.v8 = self.m.add_vertex_type("M5", "metabolite")
        self.v9 = self.m.add_vertex_type("M6", "metabolite")
        self.e1 = self.m.add_edge("M1", "R1")
        self.e2 = self.m.add_edge("M2", "R1")
        self.e3 = self.m.add_edge("R1", "M3")
        self.e4 = self.m.add_edge("R1", "M4")
        self.e5 = self.m.add_edge("M4", "R2")
        self.e6 = self.m.add_edge("M6", "R2")
        self.e7 = self.m.add_edge("R2", "M3")
        self.e8 = self.m.add_edge("M4", "R3")
        self.e9 = self.m.add_edge("M5", "R3")
        self.e10 = self.m.add_edge("R3", "M6")
        self.e11 = self.m.add_edge("R3", "M4")
        self.e12 = self.m.add_edge("R3", "M5")
        self.e13 = self.m.add_edge("M6", "R3")

    def test_getNodeType(self):
        x = self.m.get_nodes_type("reaction")
        y = ["R1", "R2", "R3"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

    def test_getNodeType(self):
        x = self.m.get_nodes_type("reaction")
        y = ["R1", "R2", "R3"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

    def test_getNodeType(self):
        x = self.m.get_nodes_type("metabolite")
        y = ["M1", "M2", "M3", "M4", "M5", "M6"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

if __name__ == '__main__':
    unittest.main()