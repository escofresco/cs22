import unittest

from util.file_reader import read_graph_from_file

class TestFileReader(unittest.TestCase):
    def test_proper_graph(self):
        filename = 'test_files/graph_medium_undirected.txt'
        graph = read_graph_from_file(filename)

        self.assertEqual(len(graph.get_vertices()), 6)

    # def test_improper_graph(self):
    #     filename = 'test_files/graph_medium_undirected.txt'
    #
    #     with self.assertRaises(ValueError):
    #         graph = read_graph_from_file(filename)
