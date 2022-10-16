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
        neighborhood = neighborhood or Neighborhood()

    #   Remove self-edge.
        neighborhood.discard(node)

        super(Directed, self).__setitem__(node, neighborhood)

    @classmethod
    def fromkeys(cls, nodes: Iterable[Node], neighborhood: Neighborhood | None = None):
        """Make graph from node iterable and given default neighborhood."""
        return Directed(Graph.fromkeys(nodes, neighborhood or Neighborhood()))

    @classmethod
    def from_adjacency_matrix(cls, edges: Iterable[Iterable[Node]]):
        """Make graph from adjacency matrix."""
        return Undirected({node: Neighborhood(neighborhood)} for node, neighborhood in enumerate(edges))

    @classmethod
    def from_edge_list(cls, edges: Iterable[tuple[Node, Node]]):
        """Make graph from edge lsit."""
        undirected = Undirected()

        for node, adjacent_node in edges:
            undirected.update({node: {adjacent_node}})

    def setdefault(self, node: Node, default_neighborhood: Neighborhood | None = None) -> Neighborhood:
        """Redefine `setdefault` with empty set value default."""
        return super(Directed, self).setdefault(node, default_neighborhood or Neighborhood())

    def get(self, node: Node, default_neighborhood: Neighborhood | None = None) -> Neighborhood:
        """Redefine `get` with empty set value default."""
        return super(Directed, self).get(node, default_neighborhood or Neighborhood())


class Undirected(Directed):
    """Undirected graph."""

    def __init__(self, *args, **kwargs):
        """Update graph with missing symmetric edges and by removing self-edges."""
        super(Undirected, self).__init__(*args, **kwargs)

    #   Add missing symmetric edges.
        self.update(self.copy())

    def __setitem__(self, node: Node, neighborhood: Neighborhood | None = None):
        """Add node with a neighborhood of nodes by adding the missing symmetric edges and removing possible self-edge."""
        neighborhood = neighborhood or Neighborhood()

    #   Remove self-edge.
        neighborhood.discard(node)

    #   Remove hanging edges if any and add new missing symmetric ones.
        self.pop(node, neighborhood)
        self.add(node, neighborhood)

    def __delitem__(self, node: Node):
        """Delete node with its neighborhood of nodes and all symmetric edges. Node has to be there."""
        self.pop(node)

    def __ior__(self, other):
        """Unite graph with another."""
        self.update(other)

    def __or__(self, other):
        """Unite graph with another."""
        return self.union(other)

    def __isub__(self, other):
        """Subtract graph from this one."""
        self.difference_update(other)

    def __sub__(self, other):
        """Subtract graph from this one."""
        return self.difference(other)

    def __iand__(self, other):
        """Intersect graph with another."""
        self.intersection_update(other)

    def __and__(self, other):
        """Intersect graph with another."""
        return self.intersection(other)

    def __ixor__(self, other):
        """Complement union with intersection."""
        self.symmetric_difference_update(other)

    def __xor__(self, other):
        """Complement union with intersection."""
        return self.symmetric_difference(other)

    def __le__(self, other):
        """Is current a subgraph of the other."""
        return self.issubset(other)

    def __ge__(self, other):
        """Is current a supergraph of the other."""
        return self.issuperset(other)

    def __lt__(self, other):
        """Is current a subgraph of the other."""
        return self <= other and self != other

    def __gt__(self, other):
        """Is current a supergraph of the other."""
        return self >= other and self != other

    @classmethod
    def fromkeys(cls, nodes: Iterable[Node], default_neighborhood: Neighborhood | None = None):
        """Make graph from node iterable and given default neighborhood. Add the missing symmetric edges."""
        return Undirected(super(Undirected, cls).fromkeys(nodes, default_neighborhood or Neighborhood()))

    def add(self, node: Node, neighbohood: Neighborhood):
        """Add to node or make from scratch if not in graph."""
        self.setdefault(node).update(neighbohood)

    #   Add symmetric edges.
        for adjacent_node in neighbohood:
            self.setdefault(adjacent_node).add(node)

    def pop(self, node: Node, default_neighborhood: Neighborhood | None = None) -> Neighborhood:  # type: ignore
        """Delete node with neighborhood and return neighborhood."""
        neighborhood = super(Undirected, self).pop(node, default_neighborhood or Neighborhood())

    #   Remove symmetric edges.
        for adjacent_node in neighborhood:
            self[adjacent_node].discard(node)  # Remove traces of node in adjacent nodes.

        return neighborhood

    def popitem(self) -> tuple[Node, Neighborhood]:
        """Delete last added node and neighborhood and return them."""
        node, neighborhood = super(Undirected, self).popitem()

        return node, self.pop(node, neighborhood)  # Remove traces of popped node from adjacent nodes.

    def update(self, other):
        """Unite graph with another."""
        for node, neighbohood in other.items():
            self.add(node, neighbohood)  # Add node with neighborhood, symmetrically.

    def union(self, other):
        """Unite graph with another."""
        undirected = Undirected(self.copy())
        undirected.update(other)

        return undirected

    def difference_update(self, other):
        """Subtract graph from this one."""
        for node, neighbohood in other.items():
            self.pop(node, neighbohood)  # Add node with neighborhood, symmetrically.

    def difference(self, other):
        """Subtract graph from this one."""
        undirected = Undirected(self.copy())
        undirected.difference_update(other)

        return undirected

    def intersection_update(self, other):
        """Intersect graph with another."""
        self.difference_update(self.difference(other))

    def intersection(self, other):
        """Intersect graph with another."""
        return self.difference(self.difference(other))

    def symmetric_difference_update(self, other):
        """Complement union with intersection."""
        self.update(other)
        self.difference_update(self.intersection(other))

    def symmetric_difference(self, other):
        """Complement union with intersection."""
        return self.union(other).difference(self.intersection(other))

    def clear(self):
        """Clear unused (isolated) nodes."""
        for node in self:
            if not self[node]:
                del self[node]

    def issubset(self, other):
        """Check if the current graph is a subgraph of the other graph."""
        return Neighborhood(self.keys()).issubset(Neighborhood(other.keys())) \
            and all(self.get(node).issubset(other[node]) for node in other)

    def issuperset(self, other):
        """Check if the current graph is a supergraph of the other graph."""
        return Neighborhood(self.keys()).issuperset(Neighborhood(other.keys())) \
            and all(self[node].issuperset(other.get(node)) for node in self)
