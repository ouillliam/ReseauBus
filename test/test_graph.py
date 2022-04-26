import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from graph import Graph
import util

class TestGraph(unittest.TestCase):

    graph = None

    def setUp(self):
        self.graph = Graph()

    def test_build_vertices_from_route(self):
        data = util.read_route_data("data/1_Poisy-ParcDesGlaisins.txt")
        self.graph.build_vertices_from_route(data["regular_date_go"])
        stations = ["LYCÉE_DE_POISY","POISY_COLLÈGE","Vernod","Meythet_Le_Rabelais","Chorus","Mandallaz","GARE","France_Barattes", "C.E.S._Barattes","VIGNIÈRES","Ponchy","PARC_DES_GLAISINS"]
        indices = [0,1,2,3,4,5,6,7,8,9,10,11]
        labels = list(zip(indices, stations))
        self.assertEqual(self.graph.vertices, indices)
        self.assertEqual(self.graph.labels, labels)

    def test_build_edges_from_route(self):
        data = util.read_route_data("data/1_Poisy-ParcDesGlaisins.txt")
        self.graph.build_vertices_from_route(data["regular_date_go"])
        self.graph.build_edges_from_route(data["regular_date_go"], 1)
        indices_start = [0,1,2,3,4,5,6,7,8,9,10]
        indices_end = [2,2,3,4,5,6,7,8,9,10,11]
        edges_test = list(zip(indices_start, indices_end))
        edges_graph = [(e[0], e[1]) for e in self.graph.edges]

        self.assertEqual(edges_graph, edges_test)

    def init_graph_test_path(self):
        self.graph.vertices = [1,2,3,4,5]
        self.graph.labels = list(zip(self.graph.vertices, self.graph.vertices))

        departure_time = "10:00"
    
        departures = [
            [1, 2, (departure_time, "10:11", 10), 1],
            [2, 3, ("10:21", "10:21", 10), 1],
            [3, 5, ("10:31", "10:31", 10), 1],
            [1, 5, (departure_time, "10:05", 50), 2],
            [1, 4, (departure_time, "10:00", 20), 3],
            [4, 5, ("10:20", "10:20", 20), 3]
        ]

        return departures

    def test_path_foremost(self):
        departures = self.init_graph_test_path()

        self.graph.set_weights(departures, 1, True)
        distances = self.graph.get_distances(1, False)
        path = self.graph.get_path_from_distances(5, distances)

        self.assertEqual(path, [1,4,5])

    def test_path_fastest(self):
        departures = self.init_graph_test_path()

        self.graph.set_weights(departures, 1, False)
        distances = self.graph.get_distances(1, False)
        path = self.graph.get_path_from_distances(5, distances)

        self.assertEqual(path, [1,2,3,5])

    def test_path_shortest(self):
        departures = self.init_graph_test_path()

        self.graph.set_weights(departures, 1, False)
        distances = self.graph.get_distances(1, True)
        path = self.graph.get_path_from_distances(5, distances)

        self.assertEqual(path, [1,5])

if __name__ == '__main__':
    unittest.main()