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

    def test_get_vertices_from_route(self):
        data = util.read_route_data("data/1_Poisy-ParcDesGlaisins.txt")
        self.graph.get_vertices_from_route(data["regular_date_go"])
        stations = ["LYCÉE_DE_POISY","POISY_COLLÈGE","Vernod","Meythet_Le_Rabelais","Chorus","Mandallaz","GARE","France_Barattes", "C.E.S._Barattes","VIGNIÈRES","Ponchy","PARC_DES_GLAISINS"]
        indices = [0,1,2,3,4,5,6,7,8,9,10,11]
        labels = list(zip(indices, stations))
        self.assertEqual(self.graph.vertices, indices)
        self.assertEqual(self.graph.labels, labels)

    def test_get_edges_from_route(self):
        data = util.read_route_data("data/1_Poisy-ParcDesGlaisins.txt")
        self.graph.get_vertices_from_route(data["regular_date_go"])
        self.graph.get_edges_from_route(data["regular_date_go"], 1)
        indices_start = [0,1,2,3,4,5,6,7,8,9,10]
        indices_end = [1,2,3,4,5,6,7,8,9,10,11]
        edges = list(zip(indices_start, indices_end))
        edges = [(e[0], e[1], None, 1) for e in edges]
        self.assertEqual(self.graph.edges, edges)

if __name__ == '__main__':
    unittest.main()