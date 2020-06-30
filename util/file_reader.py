from itertools import chain

from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    with open(filename) as file:
        file_it = iter(file)
        graph_type = {'D': True, 'G': False}.get(next(file_it).strip('\n'))

        if graph_type is None:
            raise ValueError()
        graph = Graph(is_directed=graph_type)

        for num in next_alnum(next(file_it)):
            ## Use the second line to add the vertices to the graph
            graph.add_vertex(num)

        for line in file_it:
            ## Use the 3rd+ line to add the edges to the graph
            lineit = next_alnum(line)

            try:
                node1, node2 = next(lineit), next(lineit)
                graph.add_edge(node1, node2)
            except:
                pass
    return graph

def next_alnum(line):
    """Read numeric strings from a comma-separated line.

    Yields:
        Next alphanumeric string in line
    """
    word = []

    for char in chain(line, ','):

        if char.isalnum():
            word.append(char)

        if char ==  ',':
            yield ''.join(word)
            word = []
