from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass

class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.id = vertex_id
        self.__neighbors_dict = {} # id -> object

    def __lt__(self, other_vertex):
        return self.get_id() < other_vertex.get_id()

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        if vertex_obj.get_id() in self.__neighbors_dict:
            return
        self.__neighbors_dict[vertex_obj.get_id()] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.neighbors_dict.keys())
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return tuple(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id



class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {} # id -> object
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
        new_vertex = Vertex(vertex_id)
        self.__vertex_dict[vertex_id] = new_vertex
        return new_vertex


    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        return self.__vertex_dict.get(vertex_id)

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        if not (self.contains_id(vertex_id1) and self.contains_id(vertex_id2)):
            return
        vertex1 = self.get_vertex(vertex_id1)
        vertex2 = self.get_vertex(vertex_id2)
        vertex1.add_neighbor(vertex2)

        if not self.__is_directed:
            vertex2.add_neighbor(vertex1)

    def get_vertices(self):
        """
        Return all vertices in the graph.

        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return # everything has been processed

    def is_bipartite(self):
        """
        Return True if the graph is bipartite, and False otherwise.
        """
        def bfs(node):

        seen = set()

        for node in self.get_vertices():



    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        stack = [(start_id, [])]
        seen = set()

        while len(stack):
            cur_id, path = stack.pop()

            if cur_id not in seen:
                path.append(cur_id)

                if cur_id == target_id:
                    return path
                stack.extend(map(lambda node: (node.get_id(), path),
                                 self.get_vertex(cur_id).get_neighbors()))
                seen.add(cur_id)

    def find_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """
        def bfs(node):
            visited = []
            stack = [node]

            while len(stack):
                cur_node = stack.pop()
                cur_node_id = cur_node.get_id()

                if cur_node_id not in seen:
                    visited.append(cur_node_id)
                    stack.extend(cur_node.get_neighbors())
                    seen.add(cur_node_id)
            return visited
        seen = set()
        connected_components = []

        for node in self.get_vertices():

            if node.get_id() not in seen:
                component = bfs(node)

                if len(component):
                    connected_components.append(component)
        print(connected_components)
        return connected_components

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque()
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)
                    # print(vertex_id_to_path)

        if target_id not in vertex_id_to_path: # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.

        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        queue = deque([(start_id, 0)])
        vertices = []
        seen = set()

        while len(queue):
            cur_id, cur_dist = queue.popleft()

            if cur_id not in seen:
                if cur_dist == target_distance:
                    vertices.append(cur_id)
                elif cur_dist < target_distance:
                    vertex = self.get_vertex(cur_id)
                    queue.extend(map(lambda neighbor: (neighbor.get_id(), cur_dist+1),
                                     vertex.get_neighbors()))
                seen.add(cur_id)
        return vertices


    def topological_sort(self):
        raise NotImplemented

    def contains_cycle(self):
        return self.strongly_connected_components(break_on_cycle=True) is None

    def strongly_connected_components(self, break_on_cycle=False):
        """
        Use Tarjan's Algorithm to detect strongly connected components by
        propogating low-link values thoughout cycles. This fixes the randomness
        of DFS that restricts low-link values to special cases.
        Time: O(|V| + |E|)

        Arguments:
            break_on_cycle: If graph is detected to be cyclic, exit function
                            early.

        Returns:
            Tuple of strongly connected components or None if break_on_cycle
            is True and a cycle is detected.
        """
        def dfs(vertex_id):
            ## When DFS finishes visiting all neighbors of node, check if previous
            ## node is on stack. If it is, min current node's low-link value
            ## with previous node's low-link value.
            nonlocal cur_scc_id, scc_count
            stack.append(vertex_id)
            # By creating the vertex_id key in vertexid_to_node_data, it's
            # incidentally marked as visited
            vertexid_to_node_data[vertex_id] = NodeData(cur_scc_id, cur_scc_id,
                                                    True)
            cur_scc_id += 1

            for neighbor in self.get_vertex(vertex_id).get_neighbors():
                neighbor_vertex_id = neighbor.get_id()

                if neighbor_vertex_id not in vertexid_to_node_data:
                    ## neighbor is unvisited
                    dfs(neighbor_vertex_id)

                if vertexid_to_node_data[neighbor_vertex_id].is_on_stack:
                    # Change current node's low-link value to min of
                    # current node's low-link value and neighbor's low-link
                    # value.
                    vertexid_to_node_data[vertex_id].lowlink_val = min(
                        vertexid_to_node_data[vertex_id].lowlink_val,
                        vertexid_to_node_data[neighbor_vertex_id].lowlink_val)

            cur_node_scc_id = vertexid_to_node_data[vertex_id].scc_id
            cur_node_lowlink_val = vertexid_to_node_data[vertex_id].lowlink_val

            if (cur_node_scc_id == cur_node_lowlink_val):
                ## If current node's id equals its low-link value (it has
                ## started a strongly connected component), then pop nodes off
                ## stack until current node is reached.
                scc_count += 1 # New scc found.
                _vertex_id = stack.pop()

                while _vertex_id != vertex_id:
                    ## Backtrack; change _vertex_id's low-link value to
                    ## current vertex_id's scc_id
                    vertexid_to_node_data[_vertex_id].is_on_stack = False
                    vertexid_to_node_data[_vertex_id].lowlink_val = cur_node_scc_id
                    _vertex_id = stack.pop()

                    if break_on_cycle:
                        # Cycle detected
                        return
        @dataclass
        class NodeData:
            __slots__ = ("scc_id", "lowlink_val", "is_on_stack")
            scc_id: int
            lowlink_val: int
            is_on_stack: bool
        node_count = len(self.__vertex_dict)
        # Map vertex id to strongly connected component (scc) id
        vertexid_to_node_data = {}
        stack = [] # Global DFS stack
        cur_scc_id = 0 # Track current scc id to be assigned
        scc_count = 0 # Track number of strongly connected components

        for vertex_id, node in self.__vertex_dict.items():
            if vertex_id not in vertexid_to_node_data:
                ## Node hasn't been visited
                ## Use DFS to visit a node, assign it a low-link value and id,
                ## mark it as visited, and add it to stack
                dfs(vertex_id)

        if (break_on_cycle and scc_count < node_count or
            (node_count == 1 and len(self.get_vertices()[0].get_neighbors()) == 1)):
            # Handle special case where the entire graph is a single connected
            # component or graph consists of a single node that has a self-loop
            return
        # Low-link values which represent distinct strongly connected components
        lowlink_val_to_vertex_id = defaultdict(list)

        for vertex_id, nodedata in vertexid_to_node_data.items():
            lowlink_val_to_vertex_id[nodedata.lowlink_val].append(vertex_id)
        return tuple(map(lambda scc: tuple(scc),
                         lowlink_val_to_vertex_id.values()))
