import unittest
from package_aab.src.MyGraph import MyGraph


class test_MyGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.gr = MyGraph({1: {2: None}, 2: {3: None}, 3: {2: None, 4: None}, 4: {2: None}})

        self.gr1 = MyGraph()
        self.gr1.add_vertex(1)
        self.gr1.add_vertex(2)
        self.gr1.add_vertex(3)
        self.gr1.add_vertex(4)

        self.gr1.add_edge(1, 2)
        self.gr1.add_edge(2, 3)
        self.gr1.add_edge(3, 2)
        self.gr1.add_edge(3, 4)
        self.gr1.add_edge(4, 2)

        self.gr2 = MyGraph({1: {2: None, 3: None}, 2: {4: None}, 3: {5: None}, 4: {6: None}, 5: {3: None}, 6: {}})

    def test_get__nodes(self):
        self.assertEqual(self.gr.get_nodes(), [1, 2, 3, 4])
        self.assertEqual(self.gr1.get_nodes(), [1, 2, 3, 4])
        self.assertEqual(self.gr2.get_nodes(), [1, 2, 3, 4, 5, 6])

    def test_get__edges(self):
        self.assertEqual(self.gr.get_edges(), [(1, 2), (2, 3), (3, 2), (3, 4), (4, 2)])
        self.assertEqual(self.gr1.get_edges(), [(1, 2), (2, 3), (3, 2), (3, 4), (4, 2)])
        self.assertEqual(self.gr2.get_edges(), [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 3)])

    def test_get__successors(self):
        self.assertEqual(self.gr.get_successors(1), [2])
        self.assertEqual(self.gr1.get_successors(2), [3])
        self.assertEqual(self.gr2.get_successors(4), [6])
        self.assertEqual(self.gr2.get_successors(1), [2, 3])

    def test_get__predecessors(self):
        self.assertEqual(self.gr.get_predecessors(3), [2])
        self.assertEqual(self.gr1.get_predecessors(2), [1, 3, 4])
        self.assertEqual(self.gr2.get_predecessors(3), [1, 5])
        self.assertEqual(self.gr2.get_predecessors(2), [1])

    def test_get__adjacents(self):
        self.assertEqual(self.gr.get_adjacents(3), [2, 4])
        self.assertEqual(self.gr1.get_adjacents(2), [1, 3, 4])
        self.assertEqual(self.gr2.get_adjacents(3), [1, 5])
        self.assertEqual(self.gr2.get_adjacents(2), [1, 4])

    def test_out__degree(self):
        self.assertEqual(self.gr.out_degree(3), 2)
        self.assertEqual(self.gr1.out_degree(2), 1)
        self.assertEqual(self.gr2.out_degree(4), 1)
        self.assertEqual(self.gr2.out_degree(6), 0)

    def test_in__degree(self):
        self.assertEqual(self.gr.in_degree(3), 1)
        self.assertEqual(self.gr1.in_degree(2), 3)
        self.assertEqual(self.gr2.in_degree(4), 1)
        self.assertEqual(self.gr2.in_degree(1), 0)

    def test_degree(self):
        self.assertEqual(self.gr.degree(4), 2)
        self.assertEqual(self.gr1.degree(2), 3)

    def test_all__degrees(self):
        self.assertEqual(self.gr.all_degrees(), {1: 1, 2: 3, 3: 2, 4: 2})
        self.assertEqual(self.gr1.all_degrees(), {1: 1, 2: 3, 3: 2, 4: 2})
        self.assertEqual(self.gr2.all_degrees(), {1: 2, 2: 2, 3: 2, 4: 2, 5: 1, 6: 1})

    def test_reachable_reachable__bfs(self):
        self.assertEqual(self.gr2.reachable_bfs(1), [2, 3, 4, 5, 6])
        self.assertEqual(self.gr2.reachable_bfs(6), [])

    def test_reachable_reachable__dfs(self):
        self.assertEqual(self.gr2.reachable_bfs(1), [2, 3, 4, 5, 6])
        self.assertEqual(self.gr2.reachable_bfs(6), [])

    def test_distance(self):
        self.assertEqual(self.gr.distance(1, 4), 3)
        self.assertEqual(self.gr1.distance(3, 4), 1)
        self.assertEqual(self.gr2.reachable_bfs(6), [])

    def test_shortest__path(self):
        self.assertEqual(self.gr.shortest_path(1, 4), [1, 2, 3, 4])
        self.assertEqual(self.gr1.shortest_path(4, 3), [4, 2, 3])
        self.assertEqual(self.gr2.shortest_path(1, 4), [1, 2, 4])

    def test_reachable_with_dist(self):
        self.assertEqual(self.gr.reachable_with_dist(1), [(2, 1), (3, 2), (4, 3)])
        self.assertEqual(self.gr1.reachable_with_dist(2), [(3, 1), (4, 2)])
        self.assertEqual(self.gr2.reachable_with_dist(3), [(5, 1)])

    def test_node_has_cycle(self):
        self.assertFalse(self.gr.node_has_cycle(1))
        self.assertTrue(self.gr.node_has_cycle(2))
        self.assertTrue(self.gr1.node_has_cycle(4))
        self.assertFalse(self.gr2.node_has_cycle(1))
        self.assertTrue(self.gr2.node_has_cycle(3))

    def test_has_cycle(self):
        self.assertTrue(self.gr.has_cycle())
        self.assertTrue(self.gr.has_cycle())
        self.assertTrue(self.gr1.has_cycle())
        self.assertTrue(self.gr2.has_cycle())

    def test_mean_degree(self):
        self.assertEqual(self.gr2.mean_degree(), 1.6666666666666667)

    def test_prob_degree(self):
        self.assertEqual(self.gr1.prob_degree(), {1: 0.25, 2: 0.5, 3: 0.25})
        self.assertEqual(self.gr2.prob_degree(), {2: 0.6666666666666666, 1: 0.3333333333333333})

    def test_mean_distances(self):
        self.assertEqual(self.gr.mean_distances(), (1.5555555555555556, 0.75))
        self.assertEqual(self.gr1.mean_distances(), (1.5555555555555556, 0.75))
        self.assertEqual(self.gr2.mean_distances(), (1.5, 0.3333333333333333))

    def test_all_clustering_coefs(self):
        self.assertEqual(self.gr.all_clustering_coefs(), {1: 0.0, 2: 0.3333333333333333, 3: 1.0, 4: 1.0})
        self.assertEqual(self.gr1.all_clustering_coefs(), {1: 0.0, 2: 0.3333333333333333, 3: 1.0, 4: 1.0})
        self.assertEqual(self.gr2.all_clustering_coefs(), {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0})

    def test_mean_clustering_coef(self):
        self.assertEqual(self.gr.mean_clustering_coef(), 0.5833333333333333)
        self.assertEqual(self.gr1.mean_clustering_coef(), 0.5833333333333333)
        self.assertEqual(self.gr2.mean_clustering_coef(), 0.0)

    def test_mean_clustering_perdegree(self):
        self.assertEqual(self.gr.mean_clustering_perdegree(), {1: 0.0, 3: 0.3333333333333333, 2: 1.0})
        self.assertEqual(self.gr1.mean_clustering_perdegree(), {1: 0.0, 3: 0.3333333333333333, 2: 1.0})
        self.assertEqual(self.gr2.mean_clustering_perdegree(), {2: 0.0, 1: 0.0})


if __name__ == '__main__':
    unittest.main()