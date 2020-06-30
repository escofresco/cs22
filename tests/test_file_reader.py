import unittest

from util.file_reader import read_graph_from_file

objs_to_ids = (lambda vertices:
    tuple(sorted(map(lambda vertex: vertex.get_id(), vertices))))

class TestFileReader(unittest.TestCase):
    def test_small_directed_graph(self):
        filename = 'test_files/graph_small_directed.txt'
        graph = read_graph_from_file(filename)
        vertices = graph.get_vertices()

        self.assertEqual(len(vertices), 4)
        self.assertEqual(objs_to_ids(vertices),
                         ('1','2','3','4'))
        self.assertTrue(graph.is_directed)
        self.assertEqual(objs_to_ids(graph.get_vertex('1').get_neighbors()),
                         ('2',))
        self.assertEqual(objs_to_ids(graph.get_vertex('2').get_neighbors()),
                         ('4',))
        self.assertEqual(objs_to_ids(graph.get_vertex('3').get_neighbors()),
                         ('4',))
        self.assertEqual(objs_to_ids(graph.get_vertex('4').get_neighbors()), ())

    def test_medium_undirected_graph(self):
        filename = 'test_files/graph_medium_undirected.txt'
        graph = read_graph_from_file(filename)
        vertices = graph.get_vertices()

        self.assertEqual(len(vertices), 6)
        self.assertEqual(tuple(sorted(map(lambda vertex: vertex.get_id(), vertices))),
                         ('A','B','C','D','E','F'))
        self.assertFalse(graph.is_directed)
        self.assertEqual(objs_to_ids(graph.get_vertex('A').get_neighbors()),
                         ('B', 'C'))
        self.assertEqual(objs_to_ids(graph.get_vertex('B').get_neighbors()),
                         ('A', 'C', 'D'))
        self.assertEqual(objs_to_ids(graph.get_vertex('C').get_neighbors()),
                         ('A', 'B', 'D', 'E'))
        self.assertEqual(objs_to_ids(graph.get_vertex('D').get_neighbors()),
                         ('B', 'C', 'E', 'F'))
        self.assertEqual(objs_to_ids(graph.get_vertex('E').get_neighbors()),
                         ('C', 'D', 'F',))
        self.assertEqual(objs_to_ids(graph.get_vertex('F').get_neighbors()),
                         ('D', 'E'))

    def test_improper_graph(self):
        filename = 'test_files/improper_graph_type.txt'

        with self.assertRaises(ValueError):
            graph = read_graph_from_file(filename)
