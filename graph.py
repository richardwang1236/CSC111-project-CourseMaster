from __future__ import annotations
from typing import Any
import networkx as nx

a1 = []


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

    def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.item == target_item:
            # Our base case: the target_item is the current vertex
            return True
        else:
            visited.add(self)  # Add self to the set of visited vertices
            for u in self.neighbours:
                if u not in visited:  # Only recurse on vertices that haven't been visited
                    if u.check_connected(target_item, visited):
                        return True

            return False

    def get_connected_component(self, visited: set[_Vertex]):
        """Return a set of all ITEMS connected to self by a path that does not use
        any vertices in visited.

        The items of the vertices in visited CANNOT appear in the returned set.

        Preconditions:
            - self not in visited

        Implementation notes:
            1. This can be implemented in a similar way to _Vertex.check_connected.
            2. This method must be recursive, and will have an implicit base case:
               when all vertices in self.neighbours are already in visited.
            3. Use a loop accumulator to store a set of the vertices connected to self.
        """
        global a1
        visited.add(self)
        a = {self.item}
        for u in self.neighbours:
            if u not in visited:
                a1.append((self.item, u.item))
                a = a.union(u.get_connected_component(visited))
        return a


class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def get_vertices(self):
        return self._vertices

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            # raise ValueError
            return

    def get_connected_component(self, item: Any):
        """Return a set of all ITEMS connected to the given item in this graph.

        Raise a ValueError if item does not appear as a vertex in this graph.

        >>> g = Graph()
        >>> for i in range(0, 5):
        ...     g.add_vertex(i)
        >>> g.add_edge(0, 1)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(1, 3)
        >>> g.add_edge(2, 3)
        >>> g.get_connected_component(0) == {0, 1, 2, 3}
        True

        Note: we've implemented this method for you, and you should not change it.
        Instead, your task is to implement _Vertex.get_connected_component below.
        """
        if item not in self._vertices:
            raise ValueError
        else:
            return self._vertices[item].get_connected_component(set())

    def get_exc(self, item: Any):
        global a1
        a1 = []
        if item not in self._vertices:
            return 'Course not found'
        else:
            connected = self.get_connected_component(item)
            g = Graph()
            for v in connected:
                g.add_vertex(v)
            for v in a1:
                g.add_edge(v[0], v[1])
            for x in self._vertices[item].neighbours:
                g.add_edge(item, x.item)

            return g

    def to_networkx(self, max_vertices: int = 50000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.item)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


class DirectdGraph:
    """A directed graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self._vertices[item] = _Vertex(item, set())

    def add_arc(self, item1: Any, item2: Any) -> None:
        """Add an arc between the two vertices with the given items in this graph.
        which must be item1 ---> item2 so item2 has a neighbor of item1 but item1 does not have neighbor of item2

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            # raise ValueError
            return

    def see_pre(self, item: Any):
        if item not in self._vertices:
            return 'Course Not Found'
        else:
            return [x.item for x in self._vertices[item].neighbours]

    def to_networkx(self, max_vertices: int = 50000) -> nx.DiGraph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.DiGraph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.item[-1])

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.item[-1])

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(u.item, v.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


class Course:
    """ A course in Uoft"""
    code: str
    title: str
    introduction: str
    br: list
    pre: list
    exc: list
    distribution: list

    def __init__(self, code: str, title: str, introduction: str, br: list, pre: list, exc: list, distribution: list):
        self.code = code
        self.title = title
        self.introduction = introduction
        self.br = br
        self.pre = pre
        self.exc = exc
        self.distribution = distribution
