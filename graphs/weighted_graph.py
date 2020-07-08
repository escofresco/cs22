from collections import namedtuple

from graphs.graph import Graph, Vertex

class WeightedVertex(Vertex):

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.id = vertex_id
        self.neighbors_dict = {} # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (number): The weight of this edge.
        """
        if vertex_obj.get_id() in self.neighbors_dict.keys():
            return # it's already a neighbor

        self.neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return [neighbor for (neighbor, weight) in self.neighbors_dict.values()]

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex."""
        return list(self.neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'


class WeightedGraph(Graph):

    INFINITY = float('inf')

    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {}
        self.__is_directed = is_directed

    @property
    def is_directed(self):
        return self.__is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        if vertex_id in self.vertex_dict.keys():
            return False # it's already there
        vertex_obj = WeightedVertex(vertex_id)
        self.vertex_dict[vertex_id] = vertex_obj
        return True

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.vertex_dict.keys():
            return None
        vertex_obj = self.vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        weight (number): The edge weight.
        """
        all_ids = self.vertex_dict.keys()
        if vertex_id1 not in all_ids or vertex_id2 not in all_ids:
            return False
        vertex_obj1 = self.get_vertex(vertex_id1)
        vertex_obj2 = self.get_vertex(vertex_id2)
        vertex_obj1.add_neighbor(vertex_obj2, weight)
        if not self.is_directed:
            vertex_obj2.add_neighbor(vertex_obj1, weight)

    def get_vertices(self):
        """Return all the vertices in the graph"""
        return list(self.vertex_dict.values())

    def __iter__(self):
        """Iterate over the vertex objects in the graph, to use sytax:
        for vertex in graph"""
        return iter(self.vertex_dict.values())

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root


    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if(parent_map[vertex_id] == vertex_id):
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        # Create a list of all edges in the graph, sort them by weight
        # from smallest to largest
        Edge = namedtuple("Edge", "start end weight")
        edges = set()

        for vertex in self.get_vertices():
            for neighbor, weight in vertex.get_neighbors_with_weights():
                if self.is_directed:
                    edges.add(Edge(vertex.get_id(), neighbor.get_id(), weight))
                else:
                    edges.add(Edge(*sorted((vertex.get_id(), neighbor.get_id())),
                                   weight))
        edges = list(edges)
        edges.sort(reverse=True, key=lambda edge: edge.weight)

        # Create a dictionary `parent_map` to map vertex -> its "parent".
        # Initialize it so that each vertex is its own parent.
        parent_map = {vertex.get_id(): vertex.get_id() for vertex in self.get_vertices()}

        # Create an empty list to hold the solution (i.e. all edges in the
        # final spanning tree)
        min_spanning_tree = []

        while len(min_spanning_tree) < len(self.vertex_dict) - 1:
            # While the spanning tree holds < V-1 edges, get the smallest
            # edge.
            edge = edges.pop()

            if self.find(parent_map, edge.start) != self.find(parent_map, edge.end):
                # If the two vertices connected by the edge are in different sets
                # (i.e. calling `find()` gets two different roots), then it will not
                # create a cycle, so add it to the solution set and call `union()` on
                # the two vertices.
                self.union(parent_map, edge.start, edge.end)
                min_spanning_tree.append((edge.start, edge.end, edge.weight))


        # Return the solution list.
        return min_spanning_tree

    def minimum_spanning_tree_prim(self):
        """
        Use Prim's Algorithm to return the total weight of all edges in the
        graph's spanning tree.

        Assume that the graph is connected.
        """
        vertex_to_weight = {vertex: float('inf')
                            for vertex in self.get_vertices()}
        # Choose one vertex and set its weight to 0
        vertex_to_weight[tuple(vertex_to_weight.keys())[0]] = 0
        total = 0

        while len(vertex_to_weight):
            # While `vertex_to_weight` is not empty:
            # 1. Get the minimum-weighted remaining vertex, remove it from the
            #    dictionary, & add its weight to the total MST weight
            # 2. Update that vertex's neighbors, if edge weights are smaller than
            #    previous weights
            min_weighted_vertex = None
            min_weight = float('inf')

            for vertex, weight in vertex_to_weight.items():
                if weight < min_weight:
                    min_weighted_vertex = vertex
                    min_weight = weight
            del vertex_to_weight[min_weighted_vertex]
            total += min_weight

            for neighbor, weight in min_weighted_vertex.get_neighbors_with_weights():
                if neighbor in vertex_to_weight:
                    vertex_to_weight[neighbor] = min(vertex_to_weight[neighbor],
                                                     weight)

        return total

    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight of the shortest path
        from a start vertex to a destination.
        """
        # Create a dictionary `vertex_to_distance` and initialize all
        # vertices to INFINITY - hint: use `float('inf')`
        vertex_to_distance = {vertex: float('inf')
                              for vertex in self.get_vertices()}
        vertex_to_distance[self.get_vertex(start_id)] = 0
        total = 0

        while len(vertex_to_distance):
            # While `vertex_to_distance` is not empty:
            # 1. Get the minimum-distance remaining vertex, remove it from the
            #    dictionary. If it is the target vertex, return its distance.
            # 2. Update that vertex's neighbors by adding the edge weight to the
            #    vertex's distance, if it is lower than previous.
            closest_vertex = None
            min_distance = float('inf')

            for vertex, distance in vertex_to_distance.items():
                if distance < min_distance:
                    closest_vertex = vertex
                    min_distance = distance
            del vertex_to_distance[closest_vertex]
            total += min_distance

            if closest_vertex.get_id() == target_id:
                return min_distance

            for neighbor, weight in closest_vertex.get_neighbors_with_weights():
                if neighbor in vertex_to_distance:
                    vertex_to_distance[neighbor] = min(vertex_to_distance[neighbor],
                                                       min_distance+weight)
        # Return None if target vertex not found.

    def floyd_warshall(self):
        """
        Return the All-Pairs-Shortest-Paths dictionary, containing the shortest
        paths from each vertex to each other vertex.
        """
        pass
