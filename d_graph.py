# Course: CS261 - Data Structures
# Author: Philip Peiffer
# Assignment: 6 - directed graph
# Description: This program contains an implementation of a directed graph utilizing an adjacency matrix. The program
# contains a class DirectedGraph which has several methods that are common operations related to graphs (add vertex,
# add edge, get edges, perform BFS/DFS, etc.)

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        This method adds a new vertex to the graph. No input required. The method adds a placeholder edge of weight 0
        between the vertex and every other existing vertex currently in the graph. The vertex name is auto assigned to
        the next index number in the list (e.g. first vertex added has name = 0, second name = 1, etc.). Returns an
        integer of the number of vertices in the graph after addition.
        """
        # the matrix is a list of lists, so need to append a new list for the new row and then in each existing
        # row, add the new vertex
        self.v_count += 1
        new_row = [0]

        # loop through existing rows and append a 0 to new row for each existing row, also append a 0 to the
        # existing rows
        for row in self.adj_matrix:
            row.append(0)
            new_row.append(0)

        self.adj_matrix.append(new_row)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        This method adds a new edge to the graph between the src vertex and dst vertex input. Both src and dst must be
        integers representing the index of the vertex. The method also adds the input weight to the edge (defaults to 1)
        . If src or dst do not exist, weight is negative, or src and dst refer to the same index, then this method
        does nothing. No return value.
        """
        # check to see if weight is negative or src and dst are the same (no loops allowed)
        # also have to check for src and dst indices < 0 because python allows negative indexing
        if weight < 0 or src == dst or src < 0 or dst < 0:
            return
        # try to overwrite the matrix at row = src and col = dst
        # in directed graph, edge weight only given at source vertex
        try:
            self.adj_matrix[src][dst] = weight
        # if there's an index error, then src or dst don't exist
        except IndexError:
            return

    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method removes the edge between the source and destination vertex input. The src and dst inputs must be
        integers that represent the index of the vertex in the matrix. If src, dst, or no edge exists, then the
        method does nothing. No return value.
        """
        # check to see if src = dst or if src or dst < 0. In any of those cases, just return without doing anything.
        if src == dst or src < 0 or dst < 0:
            return
        # try to overwrite the matrix at row = src and col = dst to be 0
        try:
            self.adj_matrix[src][dst] = 0
        # if an index error occurs, then src or dst don't exist
        except IndexError:
            return

    def get_vertices(self) -> []:
        """
        This method returns a list of vertices in the graph in no particular order.
        """
        vert_list = []

        # v_count is always 1 greater than the index, so loop until 1 less than v_count adding index to vert_list
        for index in range(self.v_count):
            vert_list.append(index)

        return vert_list

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph. The edges are given as a tuple of 3 values -
        (src vertex, dst vertex, weight). The order of the list is not significant.
        """
        edge_list = []
        # the rows in the matrix represent the src vertex
        # the cols represent the dst
        # since the matrix is not symmetrical, will need to loop through every vertex
        for row_ind in range(self.v_count):
            for col_ind in range(self.v_count):
                edge = self.adj_matrix[row_ind][col_ind]
                if edge != 0:
                    edge_list.append((row_ind, col_ind, edge))
        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        This method requires a list of vertex indices as input. The method checks to see if you can travel from the
        start vertex to the end over edges in the graph. If the path is possible returns True. If not returns False.
        A blank path is valid.
        """
        # each integer in the input is a src, the neighbor integer is a dst.
        # convert the path to a queue
        pq = deque()
        for vert in path:
            pq.append(vert)
        # check to see if the path is empty, if it is return True
        if len(path) == 0:
            return True
        # dequeue the first source vertex
        src = pq.popleft()
        # check if the first vertex was all that was given, if it is check to see if the index is valid, if it is then
        # the path is valid so return True
        if len(pq) == 0 and 0 <= src <= self.v_count:
            return True

        # while the queue is not empty, going to dequeue the dst vertex, try to access the edge
        # if the edge is 0 or indices are outside of the matrix, then return False
        # if the edge exists, move the src to the dst and repeat
        while pq:
            # dequeue the dst vertex
            try:
                dst = pq.popleft()
                edge = self.adj_matrix[src][dst]
                if edge != 0:
                    src = dst
                else:
                    return False
            except IndexError:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        This method performs a depth first search on the graph and returns a list of vertices visited. One input is
        required (the starting vertex - given as an index) and the ending vertex. Another input is optional (the ending
        vertex). If v_start is outside of the graph, returns an empty list. If v_end is outside the graph, returns a
        list as if v_end was absent. In the case of a vertex having multiple edges to visit next, chooses to visit the
        vertex with the smallest index number.
        """
        # initialize a stack to keep next vertices
        next_verts = []
        visited_verts = []
        next_verts.append(v_start)

        # check to make sure the start vert is in the graph
        if 0 <= v_start < self.v_count:

            # while next_verts is not empty, keep going
            while next_verts:
                # pop the top vertex
                src_vert = next_verts.pop()

                # if the vertex that we're currently on is the ending vertex, end the function
                if src_vert == v_end:
                    visited_verts.append(src_vert)
                    return visited_verts

                if src_vert not in visited_verts:
                    # push all the destination verts that have an edge to the stack from the back index forward
                    for dst_vert in range(self.v_count - 1, -1, -1):
                        edge = self.adj_matrix[src_vert][dst_vert]
                        if edge != 0:
                            next_verts.append(dst_vert)
                    visited_verts.append(src_vert)
        return visited_verts

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method performs a breadth first search on the graph and returns a list of vertices visited. One input is
        required (the starting vertex - given as an index) and the ending vertex. Another input is optional (the ending
        vertex). If v_start is outside of the graph, returns an empty list. If v_end is outside the graph, returns a
        list as if v_end was absent. In the case of a vertex having multiple edges to visit next, chooses to visit the
        vertex with the smallest index number.
        """
        # initialize the queue and put the starting vertex in it
        queue = deque()
        queue.append(v_start)
        visited_verts = []

        # check to make sure the starting vertex is in the graph
        if 0 <= v_start < self.v_count:
            # loop through the queue until it's empty
            while queue:
                # dequeue the first vertex
                src_vert = queue.popleft()

                # check to see if you've reached the ending vertex, if you have append to the list of visited verts
                # and end the function
                if src_vert == v_end:
                    visited_verts.append(src_vert)
                    return visited_verts

                if src_vert not in visited_verts:
                    for dst_vert in range(self.v_count):
                        edge = self.adj_matrix[src_vert][dst_vert]
                        if edge != 0:
                            queue.append(dst_vert)
                    visited_verts.append(src_vert)
        return visited_verts

    def has_cycle(self):
        """
        This method returns True if the graph has at least one cycle. Otherwise, the method returns False.
        """
        # A directed graph with no duplicate edges will have a cycle if, when performing a BFS at a vertex, you can
        # encounter the starting vertex in the BFS more than once
        for vert in range(self.v_count):
            # perform a BFS on each vertex in the graph
            queue = deque()
            visited_verts = []
            queue.append(vert)

            while queue:
                src = queue.popleft()

                if src not in visited_verts:
                    for dst in range(self.v_count):
                        edge = self.adj_matrix[src][dst]
                        if edge != 0:
                            # if dst is equal to the starting vertex, return True because you've found a cycle
                            if dst == vert:
                                return True
                            queue.append(dst)
                    visited_verts.append(src)

        return False

    def dijkstra(self, src: int) -> []:
        """
        This method implements the Dijkstra algorithm to compute the length of the shortest path
        from a given vertex to all other vertices in the graph. It returns a list with one value per
        each vertex in the graph, where the value at index 0 is the length of the shortest path from
        vertex SRC to vertex 0, the value at index 1 is the length of the shortest path from vertex
        SRC to vertex 1 etc. If a certain vertex is not reachable from SRC, the returned value is infinity.
        """
        # check to make sure the starting vertex is in the graph
        if 0 <= src < self.v_count:
            # initialize the return list, assigning infinity to every destination vertex to start
            return_list = []
            for vert in range(self.v_count):
                return_list.append(float('inf'))

            # initialize the priority queue that will hold edge weights
            pqueue = []
            heapq.heappush(pqueue, (0, src))
            visited_verts = []

            # perform a BFS, but do so with a priority queue and reference to dst vertex and weight of edge
            while pqueue:
                weight, src_vert = heapq.heappop(pqueue)
                if src_vert not in visited_verts:
                    for dst_vert in range(self.v_count):
                        edge_weight = self.adj_matrix[src_vert][dst_vert]
                        if edge_weight != 0:
                            heapq.heappush(pqueue, (edge_weight + weight, dst_vert))
                    return_list[src_vert] = weight
                    visited_verts.append(src_vert)

            return return_list


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
