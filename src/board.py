"""Go is played on a plane grid of 19 horizontal and 19 vertical lines, called a board.

A point on the board where a horizontal line meets a vertical line is called an intersection. Two intersections are said to be
adjacent if they are distinct and connected by a horizontal or vertical line with no other intersections between them.
"""


from types import MethodType

from .graph import Undirected
from .point import Point
from .stone import Color, Stone


class Board(list[list[Stone]]):
	"""Go board.

	The condition that the intersections be "distinct" is included to ensure that an intersection is not considered to be adjacent
	to itself.

	Intersections are also called points.

	There are 361 points on a regular 19×19 board.

	Though 19×19 boards are standard, go can be played on another size board. Particularly common sizes for quick games are 9×9 and
	13×13.
	"""

	adjacent: set[Point] = {
		Point(+1, 00),  # east
		Point(00, +1),  # north
		Point(-1, 00),  # west
		Point(00, -1),  # south
	}

	def __init__(self, size: int = 9):
		"""Build board."""
		self.size = size
		self.range = range(-self.size, self.size + 1)

		super(Board, self).__init__(
			[
				[
					Stone(
						Point(
							file,
							rank, size=self.size
						)
					) for file in self.range
				] for rank in self.range
			]
		)

	def __getitem__(self, point: tuple[int, int]):
		"""Set stone of color on point."""
		file, rank = point

		return super(Board, self).__getitem__(rank).__getitem__(file)

	def __setitem__(self, point: tuple[int, int], color_name: str):
		"""Set stone of color on point."""
		self[point].color = Color[color_name]

	def __delitem__(self, point: tuple[int, int]):
		"""Set stone of color on intersection."""
		self[point].color = Color.empty

	def __iter__(self):
		"""Iterate through all points on the board."""
		for rank in super(Board, self).__iter__():
			for point in rank:
				yield point

	def __repr__(self):
		"""Draw a board."""
		return \
			f"\n    {''.join(f'{file:+2d}' for file in self.range)}    \n\n" + \
			"\n".join(
				f"{rank:+2d}  " + "".join(
					repr(self[file, rank]) for file in self.range
				) + f"  {rank:+2d}" for rank in self.range
			) + \
			f"\n\n    {''.join(f'{file:+2d}' for file in self.range)}    \n"
