"""Custom graph implementation.

Contains:
	nodes: A set of elements of some hashable type.
	edges: A set of pairs of nodes with optional weight of hashable type.

An undirected graph is one that for all x and y nodes, both (x,y) and (y,x) are edges with the same weight.
It is a directed graph otherwise.

There are various ways to represent a graph:
-	adjacency matrix: A #nodes * #nodes matrix with 1 for every edge pair and 0 otherwise.
	Takes much space.
-	adjucency dictionary: A dictionary with #nodes keys and sets of nodes for values.
	Takes much time.
-	straight-forward: A set of nodes, and a set of edges as an ordered pair of nodes (tuples).

This implementation will follow the dictionary of sets logic.

Graphs are simply dictionary of dictionaries with keys of the same type for both layers and both key and value types hashable.

Use one key to get the neighborhood of a node object (all the nodes it connects to).
Use two keys to get the edge object connecting two nodes.

By default the graph defined as is is directed.
Undirected graph requires overriding some methods to account for symmetric edges.
"""


from typing import Callable, Hashable

Node = Hashable  # Node type to be hashable to be used as keys.
Nodes = frozenset[Node]  # A cluster of nodes.
Clusters = set[Nodes]  # A collection of clusters.
Neighborhood = set[Node]  # The neighborhood of a node. Forms edges given the node.

Edge = tuple[Node, Node]  # An edge is a pair of nodes.
Condition = Callable[[Node], bool]
Edges = frozenset[Edge]  # An edge list.

Graph = dict[Node, Neighborhood]  # A graph as sets of neighborhoods keyed by their node.


class Directed(Graph):
	"""Directed graph.

	Implements dictionary methods on graph-level and set methods on node and neighborhood levels.

	Neighborhood set operations on nodes:
		| : Unite graph with another.
		- : Subtract graph from current.
		& : Intersect graph with another.
		^ : Complement graph union with graph intersection.

	Neighborhood set comparisons and their strict counterparts on nodes:
		<= :  If current a subgraph of the other.
		>= :  If current a supergraph of the other.

	Alternative graph constructors:
		fromkeys: Make graph from node iterable and given default neighborhood.
		from_adgacency_matrix: Make graph from matrix marking connected nodes.
		from_edge_list: Make graph from list of pairs of (connected) nodes.

	Fundamental methods for operations:
		setdefault: Redefine `dict.setdefault` with empty neighborhood as default.
		get: Redefine `dict.get` with empty empty neighborhood as default.
		add: Add or update node with neighborhood.
		clear: Clear unused (disconnected) nodes.

	Backend methods for operations:
		union/update: Unite graph with another.
		difference/difference update: Subtract graph from current.
		intersection/intersection_update: Intersect graph with another.
		symmetric_difference/symmetric_difference_update: Complement graph union with graph intersection.
		issubset:  If current a subgraph of the other.
		issuperset:  If current a supergraph of the other.

	Graph special methods:
		edge_list: List edges in graph as pairs of connected nodes.
		adjacency_matrix: Form matrix with marking connected nodes.
		clusters: List sets of nodes that are connected internally but disconnected with one another.
	"""

	def __init__(self, *args, **kwargs):
		"""Update graph by removing self-edges."""
		super().__init__(*args, **kwargs)

	#	Remove self-edges.
		for node in self:
			self.__getitem__(node).discard(node)

	def __setitem__(self, node: Node, neighborhood: Neighborhood | None = None):
		"""Add node with a neighborhood of nodes by removing possible self-edge."""
		neighborhood = neighborhood or Neighborhood()

	#	Remove self-edge.
		neighborhood.discard(node)

	#	Remove hanging edges if any and add new missing symmetric ones if necessary (undirected graphs).
		self.pop(node)
		self.add(node, neighborhood)

	"""Neighborhood set operations on nodes:
		| : Unite graph with another.
		- : Subtract graph from current.
		& : Intersect graph with another.
		^ : Complement graph union with graph intersection.
	"""

	def __ior__(self, other: Graph):
		"""Unite graph with another in-place."""
		self.update(other)

	def __or__(self, other: Graph):
		"""Unite graph with another."""
		return self.union(other)

	def __isub__(self, other: Graph):
		"""Subtract graph from current in-place."""
		self.difference_update(other)

	def __sub__(self, other: Graph):
		"""Subtract graph from current."""
		return self.difference(other)

	def __iand__(self, other: Graph):
		"""Intersect graph with another in-place."""
		self.intersection_update(other)

	def __and__(self, other: Graph):
		"""Intersect graph with another."""
		return self.intersection(other)

	def __ixor__(self, other: Graph):
		"""Complement graph union with graph intersection in-place."""
		self.symmetric_difference_update(other)

	def __xor__(self, other: Graph):
		"""Complement graph union with graph intersection."""
		return self.symmetric_difference(other)

	"""Neighborhood set comparisons and their strict counterparts on nodes:
		<= : If current a subgraph of the other.
		>= : If current a supergraph of the other.
	"""

	def __le__(self, other: Graph):
		"""Is current a subgraph of the other."""
		return self.issubset(other)

	def __ge__(self, other: Graph):
		"""Is current a supergraph of the other."""
		return self.issuperset(other)

	def __lt__(self, other: Graph):
		"""Is current a strict subgraph of the other."""
		return self <= other and self != other

	def __gt__(self, other: Graph):
		"""Is current a strict supergraph of the other."""
		return self >= other and self != other

	"""Alternative graph constructors:
		fromkeys: Make graph from node iterable and given default neighborhood.
		from_edge_list: Make graph from list of pairs of (connected) nodes.
	"""

	@classmethod
	def fromkeys(cls, nodes: Neighborhood, neighborhood: Neighborhood | None = None):
		"""Make graph from node iterable and given default neighborhood."""
		return cls(Graph.fromkeys(nodes, neighborhood or Neighborhood()))

	@classmethod
	def from_edge_list(cls, edge_list: Edges):
		"""Make graph from list of pairs of (connected) nodes."""
		graph = cls()

	#	Add edges one by one to the corresponding neighborhood.
		for node, adjacent_node in edge_list:
			graph.update({node: {adjacent_node}})

		return graph

	"""Fundamental methods for operations:
		setdefault: Redefine `dict.setdefault` with empty neighborhood as default.
		get: Redefine `dict.get` with empty empty neighborhood as default.
		add: Add or update node with neighborhood.
		clear: Clear unused (disconnected) nodes.
	"""

	def setdefault(self, node: Node, default_neighborhood: Neighborhood | None = None) -> Neighborhood:
		"""Redefine dictionary `dict.setdefault` with empty neighborhood as default."""
		return super().setdefault(node, default_neighborhood or Neighborhood())

	def get(self, node: Node, default_neighborhood: Neighborhood | None = None) -> Neighborhood:
		"""Redefine `get` with empty empty neighborhood as default."""
		return super().get(node, default_neighborhood or Neighborhood())

	def add(self, node: Node, neighbohood: Neighborhood):
		"""Add or update node with neighborhood."""
		self.setdefault(node).update(neighbohood)

	def clear(self):
		"""Clear unused (disconnected) nodes."""
		for node in self.copy():
			if not self.__getitem__(node):
				super().__delitem__(node)

	"""Backend methods for operations:
		union/update: Unite graph with another.
		difference/difference update: Subtract graph from current.
		intersection/intersection_update: Intersect graph with another.
		symmetric_difference/symmetric_difference_update: Complement graph union with graph intersection.
		issubset:  If current a subgraph of the other.
		issuperset:  If current a supergraph of the other.
	"""

	def update(self, other: Graph):
		"""Unite graph with another in-place."""
		for node, neighbohood in other.items():
			self.add(node, neighbohood)  # Add node with neighborhood, symmetrically.

	def union(self, other: Graph):
		"""Unite graph with another."""
		undirected = self.__class__(self.copy())
		undirected.update(other)

		return undirected

	def difference_update(self, other: Graph):
		"""Subtract graph from current in-place."""
		for node, neighbohood in other.items():
			self.pop(node, neighbohood)  # Add node with neighborhood, symmetrically.

	def difference(self, other: Graph):
		"""Subtract graph from current."""
		undirected = self.__class__(self.copy())
		undirected.difference_update(other)

		return undirected

	def intersection_update(self, other: Graph):
		"""Intersect graph with another in-place in-place."""
		self.difference_update(self.difference(other))

	def intersection(self, other: Graph):
		"""Intersect graph with another in-place."""
		return self.difference(self.difference(other))

	def symmetric_difference_update(self, other: Graph):
		"""Complement graph union with graph intersection in-place."""
		self.update(other)
		self.difference_update(self.intersection(other))

	def symmetric_difference(self, other: Graph):
		"""Complement graph union with graph intersection."""
		return self.union(other).difference(self.intersection(other))

	def issubset(self, other: Graph):
		"""Check if the current graph is a subgraph of the other graph."""
		return Neighborhood(self.keys()).issubset(Neighborhood(other.keys())) \
			and all(self.__getitem__(node).issubset(other.__getitem__(node)) for node in other)

	def issuperset(self, other: Graph):
		"""Check if the current graph is a supergraph of the other graph."""
		return Neighborhood(self.keys()).issuperset(Neighborhood(other.keys())) \
			and all(self.__getitem__(node).issuperset(other.__getitem__(node)) for node in self)

	"""Graph special methods:
		edge_list: List edges in graph as pairs of connected nodes.
		cluster: Get cluster node belong to matching condition.
		clusters: List disjoint clusters of inter-connected nodes matching condition.
		Boundary: Collect all nodes not in the cluster but connected to it.
	"""

	@property
	def edge_list(self) -> Edges:
		"""List edges in graph as pairs of connected nodes."""
		return Edges((node, adjacent_node) for node in self for adjacent_node in self.__getitem__(node))

	def cluster(self, node: Node, condition: Condition = lambda _: True) -> Nodes:
		"""Get cluster node belong to."""
		neighborhood = self.pop(node)
		nodes = {node}

	#	Propagate through neighbors.
		for adjacent_node in neighborhood:
			if condition(adjacent_node):
				nodes.update(self.cluster(adjacent_node, condition))

	#	Stich graph back up when done (back-propagation).
		self.add(node, neighborhood)

		return Nodes(nodes)

	def clusters(self, condition: Condition = lambda _: True) -> Clusters:
		"""List disjoint subgraphs of inter-connected nodes, matching condition."""
		return Clusters(self.cluster(node, condition) for node in self.copy())

	def boundary(self, cluster: Nodes) -> Nodes:
		"""Get all nodes not in the cluster but connected to it, matching condition."""
		return Nodes().union(*(self.__getitem__(node) for node in cluster)).difference(cluster)


class Undirected(Directed):
	"""Undirected graph.

	Implement `Directed` methods to include symmetric edge operations where necessary.
	"""

	def __init__(self, *args, **kwargs):
		"""Update graph with missing symmetric edges and by removing self-edges."""
		super().__init__(*args, **kwargs)

	#	Add missing symmetric edges.
		self.update(self.copy())

	def __delitem__(self, node: Node):
		"""Delete node with its neighborhood of nodes and all symmetric edges. Node has exist."""
		self.pop(node)

	"""Fundamental methods for operations:
		add: Add or update node with neighborhood and symmetric edges.
		pop: Delete node with neighborhood and symmetric edges and return neighborhood.
	"""

	def add(self, node: Node, neighbohood: Neighborhood):
		"""Add or update node with neighborhood and symmetric edges."""
		self.setdefault(node).update(neighbohood)

	#	Add symmetric edges.
		for adjacent_node in neighbohood:
			self.setdefault(adjacent_node).add(node)

	def pop(self, node: Node, default_neighborhood: Neighborhood | None = None) -> Neighborhood:  # type: ignore
		"""Delete node with neighborhood and symmetric edges and return neighborhood."""
		neighborhood = super().pop(node, default_neighborhood or Neighborhood())

	#	Remove symmetric edges.
		for adjacent_node in neighborhood:
			super().__getitem__(adjacent_node).discard(node)  # Remove traces of node in adjacent nodes.

		return neighborhood

	def popitem(self) -> tuple[Node, Neighborhood]:
		"""Delete last added node and neighborhood and return them."""
		node, neighborhood = super().popitem()

		return node, self.pop(node, neighborhood)  # Remove traces of popped node from adjacent nodes.
