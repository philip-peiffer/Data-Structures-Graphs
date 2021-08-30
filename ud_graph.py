# Course: CS-261 Data Structures
# Author: Philip Peiffer
# Assignment: 6 - undirected graph
# Description: This program contains an implementation of an undirected graph utilizing an edge list. The program
# contains a class UndirectedGraph which has several methods that are common operations related to graphs (add vertex,
# add edge, get edges, perform BFS/DFS, etc.)

import heapq
from collections import deque
import random

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        This method adds the input as a vertex to the graph. Allowable input value is a string. If the vertex
        already exists in the graph, this method does nothing. No return value.
        """
        # validate the input is a string
        if not isinstance(v, str):
            return

        # add vertex if it's not in the dictionary already
        if v not in self.adj_list:
            self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        This method adds a new edge to the graph between the two input vertices, u and v. If either of the
        vertices are not in the graph before this method is called, this method adds the vertices and the edge.
        If the edge already exists, the method does nothing. No return value.
        """
        # check to see if u and v are the same, if they are end the function (no loops)
        if u == v:
            return

        # check to see if u and v are in adj list dictionary, if they're not add them
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        # then check to see if edge exists between them, if not add the edge
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        This method removes the edge between the input vertices from the graph. If either of the vertices
        does not exist, or if there is no edge between them, then this method does nothing. No return value.
        """
        # first check to verify u and v are in the adj list, if one of them isn't end the function
        if u not in self.adj_list or v not in self.adj_list:
            return

        # check u edges to see if v is adjacent, if it's not end the function
        if v not in self.adj_list[u]:
            return

        # if above checks pass, remove the edge
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        This method removes the input vertex and all connected edges. If the vertex does not exist, the
        method does nothing. No return value.
        """
        # if v is not in dictionary, end the function
        if v not in self.adj_list:
            return

        # loop through edges that are adjacent to v
        while self.adj_list[v]:
            u = self.adj_list[v][0]
            # run remove_edge on each vertex pair
            self.remove_edge(v, u)

        # remove v from the dictionary
        del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        This method returns a list of vertices in the graph (any order).
        """
        return_list = []

        for key in self.adj_list:
            return_list.append(key)

        return return_list

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph (any order).
        """
        edge_list = []

        # copy the existing adjacency dictionary
        copy_graph = self.copy_graph()

        # loop through the vertices in the graph and append the edges at each vertex to the edge list
        for v in self.adj_list:
            # loop through the vertices in the adjacency list and append them to edge list
            for u in copy_graph.adj_list[v]:
                edge_list.append((v, u))
            # remove the first vertex and all edges to it from the copy graph to avoid duplicates
            copy_graph.remove_vertex(v)

        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of vertex names as input. The method returns true if provided path is
        valid (i.e. can travel over vertices input by edges), otherwise it returns False. An empty path
        returns True.
        """
        # handle the case of only 1 input vertex
        if len(path) == 1:
            if path[0] not in self.adj_list:
                return False

        # if more than 1 vertex input, loop through vertices in path list
        for index in range(len(path) - 1):
            curr_vert = path[index]
            next_vert = path[index + 1]
            # check to see if the next vertex is adjacent to the curr_vert
            if curr_vert not in self.adj_list or next_vert not in self.adj_list[curr_vert]:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        This method performs a depth first search on the graph and returns a list of visited indices. Requires
        a starting vertex as input, and can be passed an ending vertex if desired. In the case where a vertex
        has multiple adjacent vertices, the search chooses the next vertex to visit based on ascending order.
        In the case of the starting vertex not being in the graph, an empty list is returned.
        """
        # initialize the lists that will hold the next vertices and visited vertices
        next_verts = []     # implement next_verts as a stack
        visited_verts = []

        # check to make sure starting vertex is in graph
        if v_start not in self.adj_list:
            return visited_verts

        # add starting vertex to list of next vertices
        next_verts.append(v_start)

        # while next vertices is not empty:
        while next_verts:
            # remove the top vertex from the stack
            curr_vert = next_verts.pop()

            # check to see if the curr_vertex is in the list of visited vertices
            if curr_vert not in visited_verts:
                # add the curr_vertex to the return list
                visited_verts.append(curr_vert)

                # check to make sure curr_vertex is not the ending vertex
                if curr_vert == v_end:
                    return visited_verts

                # loop through adjacent vertices, adding them to a heap of adjacent vertices
                adj_verts = []
                for adj_vert in self.adj_list[curr_vert]:
                    # if adjacent vertex isn't in visited vertices, add it to the list of adjacent verts
                    if adj_vert not in visited_verts:
                        heapq.heappush(adj_verts, adj_vert)

                # convert the heap of adj_verts to a sorted list
                sorted_list = []
                heap_length = len(adj_verts)
                for _ in range(heap_length):
                    sorted_list.append(heapq.heappop(adj_verts))

                # loop from the back of the sorted list forward so that smallest vertex is on top of stack
                for _ in range(heap_length - 1, -1, -1):
                    next_verts.append(sorted_list.pop())

        return visited_verts

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method performs a breadth first search on the graph and returns a list of visited indices. Requires
        a starting vertex as input, and can be passed an ending vertex if desired. In the case where a vertex
        has multiple adjacent vertices, the search chooses the next vertex to visit based on ascending order.
        In the case of the starting vertex not being in the graph, an empty list is returned.
        """
        # initialize the visited vertex list and queue to hold next verts
        visited_verts = []
        queue = deque()
        queue.append(v_start)

        # check to make sure v_start is in the graph
        if v_start not in self.adj_list:
            return visited_verts

        # loop until the queue is empty
        while queue:
            # dequeue the first vertex in the queue
            curr_vert = queue.popleft()

            # add the vertex to the list of visited verts
            visited_verts.append(curr_vert)

            # check to see if current vertex is the ending vertex, if it is end the function
            if curr_vert == v_end:
                return visited_verts

            # add all of the curr_vert's neighbors to the next_verts, but in ascending order
            # create new adj_heap, add neighbors to it, then enqueue them from start to end to queue
            adj_heap = []
            for adj_vert in self.adj_list[curr_vert]:
                heapq.heappush(adj_heap, adj_vert)
            while adj_heap:
                vert = heapq.heappop(adj_heap)
                if vert not in visited_verts and vert not in queue:
                    queue.append(vert)
        return visited_verts

    def count_connected_components(self):
        """
        This method returns the number of connected components in the graph.
        """
        comps = self.get_connected_components()
        return len(comps)

    def get_connected_components(self):
        """
        This method returns a list of the connected components in the graph. The connected components
        are a list of vertices in that component.
        """
        components = []
        # loop through each vertex in the adjacency list
        for vert in self.adj_list:
            new_comp = True
            # if it's the first vertex, components is empty, so mark new_comp as true to skip iteration
            if not components:
                new_comp = True
            # if we're past the first vertex, check to see if the vertex exists in the other existing
            # components, if it does then mark new_comp as False because the vertex is not part of a new
            # component
            else:
                for comp in components:
                    if vert in comp:
                        new_comp = False
            # if the vertex was not found in any of the other components, you have a new component so perform
            # a bfs on the vertex to get a list of vertices in the component and append that to the existing
            # components
            if new_comp:
                components.append(self.bfs(vert))
        return components

    def has_cycle(self):
        """
        This method returns True if the graph contains a cycle, False otherwise.
        """
        # a graph has a cycle if you can remove an edge and still have the same number of components
        # copy the graph so that we can remove edges and not ruin the original graph
        copy_graph = self.copy_graph()
        # find number of components to start
        num_comps = copy_graph.count_connected_components()

        # loop through the vertices
        for v in copy_graph.adj_list:
            # check to see if the length of edges is more than 1, if it's not it can't be part of a cycle
            # so skip to next vertex
            num_edges = len(copy_graph.adj_list[v])
            if num_edges > 1:
                # for each edge, remove it and see how many components you have left
                while copy_graph.adj_list[v]:
                    u = copy_graph.adj_list[v][0]
                    copy_graph.remove_edge(u, v)
                    comps_after = copy_graph.count_connected_components()

                    # if number of components hasn't changed, you found a cycle so return True
                    if num_comps == comps_after:
                        return True
                    # if the number has changed, it'll increase by 1, so just add 1 instead of another call to function
                    num_comps += 1

        return False

    def copy_graph(self):
        """
        This method returns a deep copy of the graph.
        """
        copy_graph = UndirectedGraph()
        for v in self.adj_list:
            copy_graph.add_vertex(v)
            for u in self.adj_list[v]:
                copy_graph.adj_list[v].append(u)
        return copy_graph

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
