"""Go is played on a plane grid of 19 horizontal and 19 vertical lines, called a board.

A point on the board where a horizontal line meets a vertical line is called an intersection. Two intersections are said to be
adjacent if they are distinct and connected by a horizontal or vertical line with no other intersections between them.
"""


from .graph import Neighborhood, Undirected
from .stone import Stone


class Board(Undirected):
	"""Go board.

	The condition that the intersections be "distinct" is included to ensure that an intersection is not considered to be adjacent
	to itself.

	Intersections are also called points.

	There are 361 points on a regular 19×19 board.

	Though 19×19 boards are standard, go can be played on another size board. Particularly common sizes for quick games are 9×9 and
	13×13.
	"""

	def __init__(self, size: int = 9):
		"""Build board."""
		self.size: int = size
		self.range: range = range(-self.size, self.size + 1)

	#	Initialize empty board.
		super().__init__()

		for rank in self.range:
			for file in self.range:
				stone = Stone(
					file,
					rank, size=self.size
				)
				neighborhood = Neighborhood()

				for adjacent_stone in stone.adjacencies:
					neighbor = stone + adjacent_stone

					if neighbor:
						neighborhood.add(neighbor)

				self[stone] = neighborhood

	def __repr__(self) -> str:
		"""Draw a board."""
		files = "\n    " + "".join(f"{file:+2d}" for file in self.range) + "\n"

		return files + "\n" + "".join(repr(stone) for stone in self) + files
