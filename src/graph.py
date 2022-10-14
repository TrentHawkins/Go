"""Custom graph implementation.

Contains:
    nodes: A set of elements of some hashable type.
    edges: A set of pairs of nodes with optional weight of hashable type.

An undirected graph is one that for all x and y nodes, both (x,y) and (y,x) are edges with the same weight.
It is a directed graph otherwise.

There are various ways to represent a graph:
-   adjacency matrix: A #nodes * #nodes matrix with 1 for every edge pair and 0 otherwise.
    Takes much space.
-   adjucency dictionary: A dictionary with #nodes keys and sets of nodes for values.
    Takes much time.
-   straight-forward: A set of nodes, and a set of edges as an ordered pair of nodes (tuples).

This implementation will follow the dictionary of sets logic.

Graphs are simply dictionary of dictionaries with keys of the same type for both layers and both key and value types hashable.

Use one key to get the neighborhood of a node object (all the nodes it connects to).
Use two keys to get the edge object connecting two nodes.

By default the graph defined as is is directed.
Undirected graph requires overriding some methods to account for symmetric edges.
"""


from dataclasses import dataclass
from typing import Hashable, Iterable

Node = Hashable  # The nodes. Have to be hashable to be used as keys.
Neighborhood = set[Node]  # A connectible neiborhood lacking an origin. Forms edges with a given origin.
Graph = dict[Node, Neighborhood]  # The form of a graph, generally directed.


class Directed(Graph):
    """Directed graph."""

    def __init__(self, *args, **kwargs):
        """Update graph by removing self-edges."""
        super(Directed, self).__init__(*args, **kwargs)

    #   Remove self-edges.
        for node in self:
            self[node].discard(node)

    def __setitem__(self, node: Node, neighborhood: Neighborhood | None = None):
        """Just remove the self-edge if any."""
        if neighborhood is None:
            return

    #   Remove self-edge.
        neighborhood.discard(node)

        super(Directed, self).__setitem__(node, neighborhood)

    @classmethod
    def fromkeys(cls, nodes: Iterable[Node], neighborhood: Neighborhood | None = None):
        """Make graph from node iterable and given default neighborhood."""
        if neighborhood is None:
            neighborhood = Neighborhood()

        return Directed(Graph.fromkeys(nodes, neighborhood))


class Undirected(Directed):
    """Undirected graph."""

    def __init__(self, *args, **kwargs):
        """Update graph with missing symmetric edges and by removing self-edges."""
        super(Undirected, self).__init__(*args, **kwargs)

    #   Add missing symmetric edges.
        self.update(self.copy())

        pass

    def __setitem__(self, node: Node, neighborhood: Neighborhood | None = None):
        """Add node with a neighborhood of nodes by adding the missing symmetric edges and removing possible self-edge."""
        if neighborhood is None:
            return

    #   Remove self-edge.
        neighborhood.discard(node)

    #   Remove hanging edges if any and add new missing symmetric ones.
        self.pop(node, neighborhood)
        self.add(node, neighborhood)

    def __delitem__(self, node: Node):
        """Delete node with its neighborhood of nodes and all symmetric edges. Node has to be there."""
        self.pop(node)

    @classmethod
    def fromkeys(cls, nodes: Iterable[Node], neighborhood: Neighborhood | None = None):
        """Make graph from node iterable and given default neighborhood. Add the missing symmetric edges."""
        if neighborhood is None:
            return {}

        return Undirected(super(Undirected, cls).fromkeys(nodes, neighborhood))

    def setdefault(self, node: Node, neighborhood: Neighborhood | None = None) -> Neighborhood:
        """Redefine `setdefault` with empty set value default."""
        if neighborhood is None:
            neighborhood = Neighborhood()

        return super(Undirected, self).setdefault(node, neighborhood)

    def add(self, node: Node, neighbohood: Neighborhood):
        """Add to node or make from scratch if not in graph."""
        self.setdefault(node).update(neighbohood)

    #   Add symmetric edges.
        for adjacent_node in neighbohood:
            self.setdefault(adjacent_node).add(node)

    def update(self, graph: Graph):
        """Update the update method to update undirected graph symmetrically."""
        for node, neighbohood in graph.items():
            self.add(node, neighbohood)  # Add node with neighborhood, symmetrically.

    def get(self, node: Node, neighborhood: Neighborhood | None = None) -> Neighborhood:
        """Redefine `get` with empty set value default."""
        if neighborhood is None:
            neighborhood = Neighborhood()

        return super(Undirected, self).get(node, neighborhood)

    def pop(self, node: Node, neighborhood: Neighborhood | None = None) -> Neighborhood:
        """Delete node with neighborhood and return neighborhood."""
        if neighborhood is None:
            neighborhood = Neighborhood()

        neighborhood = super(Undirected, self).pop(node, neighborhood)

    #   Remove symmetric edges.
        for adjacent_node in neighborhood:  # type: ignore
            self[adjacent_node].discard(node)  # Remove traces of node in adjacent nodes.

        #   If node is drained of neighbors, destroy it.
            if not self[adjacent_node]:
                super(Undirected, self).pop(adjacent_node)

        return neighborhood  # type: ignore

    def popitem(self) -> tuple[Node, Neighborhood]:
        """Delete last added node and neighborhood and return them."""
        node, neighborhood = super(Undirected, self).popitem()

        return node, self.pop(node, neighborhood)  # Remove traces of popped node from adjacent nodes.
