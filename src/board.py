"""Go is played on a plane grid of 19 horizontal and 19 vertical lines, called a board.

A point on the board where a horizontal line meets a vertical line is called an intersection. Two intersections are said to be
adjacent if they are distinct and connected by a horizontal or vertical line with no other intersections between them.

The board file format starts with a board descriptor line, followed by a flag.
"""


from operator import attrgetter
from random import choice, seed
from typing import Callable

from .graph import Graph, Neighborhood, Undirected
from .point import Point
from .stone import Color, Stone

Stones = frozenset[Stone]
Base = Stones
Bases = set[Base]


class Board(Undirected):
	"""Go board.

	The condition that the intersections be "distinct" is included to ensure that an intersection is not considered to be adjacent
	to itself.

	Intersections are also called points.

	There are 361 points on a regular 19×19 board.

	Though 19×19 boards are standard, go can be played on another size board. Particularly common sizes for quick games are 9×9 and
	13×13.

	Attributes:
		size: Half of the board.
		range: The whole board.
	"""

	def __init__(self, other: Graph | None = None, size: int = 9, color: Callable[[], str] = lambda: "empty"):
		"""Build board."""
		self.size: int = size
		self.range: range = range(-self.size, self.size + 1)

	#	Initialize empty board.
		super(Board, self).__init__(other) if other else super(Board, self).__init__()

	#	First add the nodes blank.
		for rank in self.range:
			for file in self.range:
				stone = Stone(
					file,
					rank,
					size=self.size, color=color()
				)

				super(Board, self).__setitem__(stone)

	#	Then set their neighborhoods, so that they are up to date.
		for stone in super(Board, self).copy():
			neighborhood = Neighborhood()

			for adjacent_point in stone.adjacencies:
				neighbor = stone + adjacent_point

				if neighbor:
					neighborhood.add(self[neighbor])

			super(Board, self).__setitem__(stone, neighborhood)

	def __str__(self) -> str:
		"""Draw a board."""
		return "\n" + "".join(str(stone) for stone in sorted(self, key=attrgetter("rank", "file")))

	def __setitem__(self, point: Point | tuple[int, int], stone: Stone | str = "empty"):
		"""Place stone on the board. Changing the graph is meaningless at user level."""
		point = Point(*point) if isinstance(point, tuple) else point
		stone = Stone(**vars(point), color=stone) if isinstance(stone, str) else stone

		super(Board, self).__setitem__(stone, super(Board, self).__getitem__(point))

	def __getitem__(self, point: Point | tuple[int, int]) -> Stone:
		"""Get color of stone. Getting its graph neighbothood is meaningless at user level."""
		point = Point(*point) if isinstance(point, tuple) else point

		for stone in self:
			if point == stone:
				return stone

		else:
			raise KeyError("Stone is not on the board.")

	def __delitem__(self, point: Point | tuple[int, int]):
		"""Remove stone from the board. Deletting it from the graph is meaningless at user level."""
		point = Point(*point) if isinstance(point, tuple) else point

		self.__setitem__(point)

	def __eq__(self, other):
		"""Is necessary since stones are indistinguishable."""
		return super(Board, self).__eq__(other) and all(stone.color == other[stone].color for stone in self)

	def put(self, stone: Stone):
		"""More meaningful setter."""
		super(Board, self).__setitem__(stone, super(Board, self).__getitem__(stone))

	def remove(self, stone: Stone):
		"""More meaningful deleter."""
		self.__getitem__(stone).color = Color.empty

	@classmethod
	def random(cls, size: int = 9, board_seed: int | None = None, emptiness: int = 1):
		"""Get a random board."""
		seed(board_seed)

		return cls(
			size=size,
			color=lambda: Color[choice(["white", *["empty"] * emptiness, "black"])].name)

	@classmethod
	def load(cls, filename: str):
		"""Load board state from file."""
		with open(filename, mode="rt", encoding="utf-8") as board:
			def read_strip(size: int | None = None) -> str:
				output = board.read(size)

				return output if not output.isspace() else read_strip(size)

			return cls(size=int(read_strip(1)), color=lambda: Color(read_strip(1)).name)

	def copy(self):
		"""Return a copy of the board."""
		color = (stone.color for stone in self)
		return self.__class__(size=self.size, color=lambda: next(color))

	def save(self, filename: str):
		"""Save board state to file."""
		with open(filename, mode="wt", encoding="utf-8") as board:
			board.write(f"{self.size}\n{self}")

	def liberties(self, base: Base) -> Stones:
		"""Get all empty intersections at the boundary of cluster (base)."""
		return Stones(stone for stone in self.boundary(base) if not stone.color)
