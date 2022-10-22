"""Tests for Go engine."""


class TestPlayer:
	"""Test player status control."""

	def test_bases(self):
		"""Test monitoring of a player's bases."""
		from src.board import Base, Bases, Board
		from src.player import Player

	#	A random board.
		board = Board.random(
			size=2,
			board_seed=2,
			emptiness=2,
		)

	#	The players.
		black = Player(
			name="Foo",
			color="black",
			board=board,
		)
		empty = Player(
			name="Huh",
			color="empty",
			board=board,
		)
		white = Player(
			name="Bar",
			color="white",
			board=board,
		)

	#	Assert specific bases:
		assert black.bases == Bases(
			{
				Base(
					{
						board[-1, +0],
						board[-2, +0],
					}
				),
				Base(
					{
						board[+1, +0],
						board[+1, +1],
					}
				),
				Base(
					{
						board[-1, +2],
						board[-2, +2],
					}
				),
			}
		)
		assert empty.bases == Bases(
			{
				Base(
					{
						board[+1, -2],
						board[+2, -2],
						board[+2, -1],
						board[+2, +0],
						board[+2, +1],
						board[+2, +2],
						board[+1, +2],
						board[+0, +2],
						board[+0, +1],
						board[+0, +0],
						board[+0, -1],
						board[-1, -1],
						board[-2, -1],
					}
				),
			}
		)
		assert white.bases == Bases(
			{
				Base(
					{
						board[-2, -2],
						board[-1, -2],
						board[+0, -2],
					}
				),
				Base(
					{
						board[+1, -1],
					}
				),
				Base(
					{
						board[-1, +1],
						board[-2, +1],
					}
				),
			}
		)

	#	Assert bases are separate.
		assert black.bases.isdisjoint(empty.bases)
		assert empty.bases.isdisjoint(white.bases)
		assert white.bases.isdisjoint(black.bases)

	def test_capture(self):
		"""Test the elimination of captured bases from the board."""
		from src.board import Base, Bases, Board
		from src.player import Player

	#	A random board.
		board = Board.random(
			size=2,
			board_seed=0,
			emptiness=1,
		)

	#	The players.
		black = Player(
			name="Foo",
			color="black",
			board=board,
		)

	#	Assert black originally has base in the corner.
		assert Base(
			{
				board[-2, +2],
				board[-1, +2],
			}
		) in black.bases

	#	Remove base in the corner.
		black.kill()

	#	Assert black no longer has base in the corner.
		assert Base(
			{
				board[-2, +2],
				board[-1, +2],
			}
		) not in black.bases


class TestBoard:
	"""Test board creation and handling."""

	def test_init(self):
		"""Test board creation."""
		from src.board import Board

	#	Assert generated sizes match board spec.
		for size in range(10):
			assert len(Board(size=size)) == (2 * size + 1) ** 2

	def test_io(self):
		"""Test saving the board state."""
		from src.board import Board
		from src.stone import Color

	#	A random board.
		board = Board.random(
			size=9,
			board_seed=9,
			emptiness=2,
		)

	#	Save random board.
		board.save("test.board")

	#	Reload saved board and assert it is the same one as the one here.
		assert board == Board.load("test.board")

	def test_liberty(self):
		"""Test liberties on board saved by this class."""
		from src.board import Board, Stones
		from src.stone import Stone

	#	A random board.
		board = Board.random(
			size=2,
			board_seed=2,
			emptiness=2,
		)

	#	Check central stone:
		assert board.liberties(
			Stones(
				{
					board[0, 0],
				}
			)
		) == Stones(
			{
				board[0, -1],
				board[0, +1],
			}
		)


class TestIntersection:
	"""Test intersection operations."""

	def test_init(self):
		"""Test proper generation of intersections."""
		from src.point import Point

	#	Assert size does stay positive.
		assert Point(0, 0, -9).size == 9

	#	Boundary checks inside board limits.
		assert Point(-1, +1, 1)

	#	Boundary checks outside board limits.
		assert not Point(-2, +1, 1)
		assert not Point(-1, +2, 1)

	def test_operations(self):
		"""Test intersection vector operations."""
		from src.point import Point

	#	Binary operations:
		assert Point(-1, +2, 0) + Point(-3, +4, 0) == Point(-4, +6, 0)
		assert Point(-1, +2, 0) - Point(-3, +4, 0) == Point(+2, -2, 0)

	#	Multiplication:
		assert Point(-1, +2, 0) * 2 == Point(-2, +4, 0)
		assert 2 * Point(-3, +4, 0) == Point(-6, +8, 0)

	#	Unary operations:
		assert +Point(-1, +2, 0) == Point(-1, +2, 0)
		assert -Point(-3, +4, 0) == Point(+3, -4, 0)


class TestUndirected:
	"""Test (undirected) Graph objects."""

	def test_init(self):
		"""Test graph creation."""
		from src.graph import Neighborhood, Undirected

		graph = Undirected.fromkeys(
			{
				1,
				2,
				3,
			}
		)

	#	Assert graph with isolated nodes is built.
		for node in graph:
			assert graph[node] == Neighborhood()

	#	Graph will be empty after clearing, as no pair of nodes is connected.
		graph.clear()

		assert graph == Undirected()

	#	Graph should be reproducible from its own edgelist.
		assert graph == Undirected.from_edge_list(graph.edge_list)

	def test_set(self):
		"""Test setting and updating methods."""
		from src.graph import Neighborhood, Undirected

		graph = Undirected(
			{
				1: {
					1,  # self-reference
					2,  # includes symmetric
				},
				2: {
					1,  # includes symmetric
					4,  # misses symmetric with node missing
				},
				3: {
					1,  # misses symmetric but node included
					3,  # self-reference
				},
			}
		)
		should_be = {
			1: {
				2,
				3,
			},
			2: {
				1,
				4,
			},
			3: {
				1,
			},
			4: {
				2,
			}
		}

	#	Test undirected graph creation which fills missing symmetric edges.
		assert graph == should_be

	#	Test if other methods for altering the graph are affected by the symmetric setter.
		graph.update({1: {5}})  # Try and update graph. This also tests adding.
		should_be.update({1: should_be[1] | {5}, 5: {1}})  # The graph should contain both edge directions.

		assert graph == should_be
		assert graph.setdefault(1, {4}) == {
			2,
			3,
			5,  # Added just before.
		}  # Node 1 exists, so get its proper neighborhood.
		assert graph.setdefault(6, {4}) == {4}  # Node 6 does not exist, so set the default {4}.
		assert graph.setdefault(7) == Neighborhood()  # Node 7 does not exist, so set the default empty set.

	def test_get(self):
		"""Test getting methods."""
		from src.graph import Undirected

		graph = Undirected(
			{
				1: {
					1,  # self-reference
					2,  # includes symmetric
				},
				2: {
					1,  # includes symmetric
					4,  # misses symmetric with node missing
				},
				3: {
					1,  # misses symmetric but node included
					3,  # self-reference
				},
			}
		)

	#	Test how normal key access returns neighborhoods.
		assert graph[1] == {
			2,
			3,
		}
		assert 1 in graph[2]
		assert 1 in graph[3]

	#	Test how the `get` method with default value works.
		assert graph.get(1, {4}) == {
			2,
			3,
		}  # Node 1 exists, so get its proper neighborhood.
		assert graph.get(5, {4}) == {4}  # Node 5 does not exist, so get the default {4}.

	def test_del(self):
		"""Test deleting methods."""
		from src.graph import Undirected

		graph = Undirected(
			{
				1: {
					2,
					3,
				},
				2: {
					1,
					4,
				},
				3: {
					1,
				},
				4: {
					2,
				}
			}
		)

	#	Plain-delete node 4 and connected edges.
		del graph[4]

		assert 4 not in graph
		assert 4 not in graph[2]  # The symmetric edge should be missing too.

	#	Popping should be using deletion.
		assert graph.pop(4, {1, 2, 3}) == {1, 2, 3}  # 4 is no longer a node so return the default given.
		assert graph.pop(3) == {1}  # pop returns the popped value
		assert 3 not in graph
		assert 3 not in graph[1]  # The symmetric edge should be missing too. NOTE: It does not, because it is written in C.

	#	Popping item should be using pop?
		assert graph.popitem() == (2, {1})  # popitems returns the popped items (key and value)
		assert 2 not in graph[1]  # The symmetric edge should be missing too. NOTE: It does not, because it is written in C.

	#	Clear isolated nodes.
		graph.clear()

		assert graph == Undirected()

	def test_special(self):
		"""Test methods related to clustering and edge listing."""
		from src.graph import Clusters, Edges, Neighborhood, Nodes, Undirected

		graph = Undirected(
			{
				1: {
					2,
					3,
					4,
				},
				5: {
					6,
					7,
				},
				8: {
					9,
				},
				0: Neighborhood()
			}
		)

	#	Assert disconnected nodes are allowed.
		assert graph[0] == Neighborhood()

	#	Assert clusters are as indicated by the directed initialization of this undirected graph.
		assert graph.clusters() == Clusters(
			{
				Nodes(
					{
						1,
						2,
						3,
						4,
					}
				),
				Nodes(
					{
						5,
						6,
						7,
					}
				),
				Nodes(
					{
						8,
						9,
					}
				),
				Nodes(
					{
						0,
					}
				),
			}
		)

	#	Assert nodes belong to their clusters.
	#	for node in graph:
	#		assert node in graph.cluster(node)

	#	If condition evaluates to false, no clusters are given.
		assert graph.clusters(lambda _: False) == Clusters()

	#	Check edgelist.
		assert graph.edge_list == Edges(
			{
				(1, 2), (2, 1),
				(1, 3), (3, 1),
				(1, 4), (4, 1),
				(5, 6), (6, 5),
				(5, 7), (7, 5),
				(8, 9), (9, 8),
			}
		)

	#	Check edgelist is the same even after clearing isolated nodes.
		graph.clear()

		assert 0 not in graph
		assert graph.edge_list == Edges(
			{
				(1, 2), (2, 1),
				(1, 3), (3, 1),
				(1, 4), (4, 1),
				(5, 6), (6, 5),
				(5, 7), (7, 5),
				(8, 9), (9, 8),
			}
		)
