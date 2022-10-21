"""Go is played on a plane grid of 19 horizontal and 19 vertical lines, called a board.

A point on the board where a horizontal line meets a vertical line is called an intersection. Two intersections are said to be
adjacent if they are distinct and connected by a horizontal or vertical line with no other intersections between them.

The board file format starts with a board descriptor line, followed by a flag.
"""


from operator import attrgetter
from typing import Callable

from .graph import Neighborhood, Undirected
from .stone import Color, Stone


class Board(Undirected):
	"""Go board.

	The condition that the intersections be "distinct" is included to ensure that an intersection is not considered to be adjacent
	to itself.

	Intersections are also called points.

	There are 361 points on a regular 19×19 board.

	Though 19×19 boards are standard, go can be played on another size board. Particularly common sizes for quick games are 9×9 and
	13×13.
	"""

	def __init__(self, size: int = 9, color: Callable[[], str] = lambda: "empty"):
		"""Build board."""
		self.size: int = size
		self.range: range = range(-self.size, self.size + 1)

	#	Initialize empty board.
		super().__init__()

		for rank in self.range:
			for file in self.range:
				stone = Stone(
					rank,
					file,
					size=self.size, color=color()
				)
				neighborhood = Neighborhood()

				for adjacent_stone in stone.adjacencies:
					neighbor = stone + adjacent_stone

					if neighbor:
						neighborhood.add(neighbor)

				self[stone] = neighborhood

	def __str__(self) -> str:
		"""Draw a board."""
		return "\n" + "".join(str(stone) for stone in sorted(self, key=attrgetter("rank", "file"))) + "\n"

	@classmethod
	def load(cls, filename: str):
		"""Load board state from file."""
		with open(filename, mode="rt", encoding="utf-8") as board:
			return cls(size=int(board.read(2).strip()), color=lambda: Color(board.read(1).strip()).name or "empty")

	def save(self, filename: str):
		"""Save board state to file."""
		with open(filename, mode="wt", encoding="utf-8") as board:
			board.write(f"{self.size} ")
			board.write(str(self).replace("\n", ""))
