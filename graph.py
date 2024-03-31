from __future__ import annotations
from typing import Any
from dataclasses import field
import heapq
import copy
import networkx as nx


class Course:
    """A course in Uoft"""

    code: str
    title: str
    introduction: str
    br: list
    pre: list
    exc: list
    distribution: list

    def __init__(
        self,
        code: str,
        title: str,
        introduction: str,
        br: list,
        pre: list,
        exc: list,
        distribution: list,
    ):
        self.code = code
        self.title = title
        self.introduction = introduction
        self.br = br
        self.pre = pre
        self.exc = exc
        self.distribution = distribution

    def __repr__(self) -> str:
        """
        Debug
        """
        return f"{self.code}"


class _Vertex:
    """A vertex in a graph."""

    item: Any = field(compare=True)
    after: set[_Vertex]
    prev: set[_Vertex]
    rating: float

    def __init__(
        self,
        item: Any,
        after: set[_Vertex],
        prev: set[_Vertex],
        rating: float = 0,
    ) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.after = after
        self.prev = prev
        self.rating = rating

    def __eq__(self, __value: _Vertex) -> bool:
        """Reload operator =="""
        return self.item == __value.item

    def __gt__(self, __value: _Vertex) -> bool:
        """Reload operator >"""
        return self.item > __value.item

    def __lt__(self, __value: _Vertex) -> bool:
        """Reload operator <"""
        return self.item < __value.item

    def __hash__(self):
        """
        Reload hash function\\
        Since the default hash function goes away ;sad;
        """
        return hash(str(self.item))

    def __repr__(self) -> str:
        """
        Debug
        """
        return f"V[{self.item}]"

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
        for u in self.after:
            path = (self.item, u.item)
            # if u not in visited:
            if path not in a1:
                a1.append(path)
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
        """
        Returns all the vertices in the graph
        """
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
            v1.after.add(v2)
            v2.after.add(v1)
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
        """
        Return a graph that contains all the exclusions of the given course
        """
        global a1
        a1 = []
        if item not in self._vertices:
            return "Course not found"
        else:
            connected = self.get_connected_component(item)
            g = Graph()
            for v in connected:
                g.add_vertex(v)
            for v in a1:
                g.add_edge(v[0], v[1])
            # for x in self._vertices[item].neighbours:
            #     g.add_edge(item, x.item)

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

            for u in v.after:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


class DirectedGraph:
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

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, set(), set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph(from item1 to item2).

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.after.add(v2)
            v2.prev.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_vertices(self) -> dict[Any, _Vertex]:
        """
        Returns all the vertices in the graph
        """
        return self._vertices

    def minimal_graph(self, start: list[Any], end: list[Any]) -> list[_Vertex]:
        """
        Return a minimal list of vertices in self such that there is a path between each pair of nodes in start and end.
        """
        new_vertices = self.dijkstra(start, end)

        # Build a new graph
        new_graph = DirectedGraph()
        for i in new_vertices:
            for j in i:
                for k in range(len(j)):
                    if j[k] not in new_graph.get_vertices():
                        new_graph.add_vertex(j[k].item)
                    if j[k].item not in start and k != 0:
                        new_graph.add_edge(j[k - 1].item, j[k].item)

        # Calculate Dominators
        all_v = copy.deepcopy(new_graph.get_vertices())
        dom = new_graph.compute_dominators(self._vertices[start[0]])
        semians = set()
        for i in dom:
            dom[i].discard(i)
            semians = semians.union(dom[i])

        # Remove non-Dominators
        for v in all_v:
            vertex = all_v[v]
            if vertex not in semians:
                for i in vertex.prev:
                    i.after.discard(vertex)
                for i in vertex.after:
                    i.prev.discard(vertex)
                del new_graph._vertices[v]

        # Remove start node
        del new_graph._vertices[start[0]]

        return new_graph.get_vertices()

    # Dom & Sub D=
    def compute_dominators(self, start_node: _Vertex) -> dict[_Vertex, set[_Vertex]]:
        dominators = {
            node: {node for node in self._vertices.values()}
            for node in self._vertices.values()
        }  # Initialize all nodes as dominators
        dominators[start_node] = {
            start_node
        }  # The dominator of the start node is itself

        changes = True
        while changes:
            changes = False
            for v in self._vertices.values():
                if v != start_node:
                    pred_doms = [dominators[pred] for pred in v.prev]
                    new_dom = {v} | (pred_doms[0] if pred_doms else set())
                    for pred_dom in pred_doms[1:]:
                        new_dom &= pred_dom
                    if dominators[v] != new_dom:
                        dominators[v] = new_dom
                        changes = True

        return dominators

    def dijkstra(self, start: list[Any], end: list[Any]) -> list[list[list[_Vertex]]]:
        """
        Finding the shortest path with the highest rating connected the start vertices and the end vertices
        """
        # Initialization
        distances: dict[_Vertex, float | int] = {
            self._vertices[v]: float("inf") for v in self._vertices
        }
        predecessors: dict[_Vertex, list[_Vertex]] = {
            self._vertices[v]: [] for v in self._vertices
        }

        # Generate a really big start vertex XD
        start_vertex: _Vertex = _Vertex(start[0], set(), set())
        for i in start:
            if i in self._vertices:
                start_vertex.after = start_vertex.after.union(self._vertices[i].after)
            else:
                raise ValueError("Do not find the start vertex!")
        self._vertices[start[0]] = start_vertex

        ans: list[list[list[_Vertex]]] = []

        # Main body
        for item in end:

            if item not in self._vertices:
                raise ValueError("Do not find the end vertex!")

            # Find the shortest Path(Dijkstra)
            distances[start_vertex] = 0
            visited: set[_Vertex] = set()
            heap: list[tuple[int | float, _Vertex]] = [(0, start_vertex)]
            while heap:
                current_node: _Vertex
                (current_distance, current_node) = heapq.heappop(heap)
                if current_node in visited:
                    continue
                visited.add(current_node)
                for neighbor in current_node.after:
                    distance = current_distance + 1
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        predecessors[neighbor] = [current_node]  # update predecessors
                        heapq.heappush(heap, (distance, neighbor))
                    elif distance == distances[neighbor]:
                        predecessors[neighbor].append(current_node)  # add a new path

            # Reconstruct Path
            all_paths: list[list[_Vertex]] = []
            current = self._vertices[item]
            self.construct_paths(
                predecessors, start_vertex, current, [current], all_paths
            )
            ans.append([list(reversed(i)) for i in all_paths])

        return ans

    def construct_paths(
        self,
        predecessors: dict,
        start: _Vertex,
        end: _Vertex,
        current_path: list[_Vertex],
        all_paths: list[list[_Vertex]],
    ) -> None:
        """
        Helper func for reconstructing paths
        """
        if start == end:
            all_paths.append(list(current_path))
            return
        for predecessor in predecessors[end]:
            current_path.append(predecessor)
            self.construct_paths(
                predecessors, start, predecessor, current_path, all_paths
            )
            current_path.pop()

    def see_pre(self, item: Any):
        """
        Return all the prerequisites of the given course
        """
        if item not in self._vertices:
            return "Course Not Found"
        else:
            return [x.item for x in self._vertices[item].prev]

    def to_networkx(self, max_vertices: int = 50000) -> nx.DiGraph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.DiGraph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.item[-1])

            for u in v.after:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.item[-1])

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(u.item, v.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx
