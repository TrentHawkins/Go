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

	def __init__(self, size: int = 9):
		"""Build board."""
		self.size = size
		self.range = range(-self.size, self.size + 1)

	#	Initialize empty board.
		super().__init__(
			[
				[
					Stone(
						Point(
							file,
							rank, size=self.size
						),
						color=Color.empty,
					) for file in range(-self.size, self.size + 1)
				] for rank in range(-self.size, self.size + 1)
			]
		)

	#	Provide board context for stone liberty depiction.
		def stone_liberty(stone: Stone, point: Point) -> bool:
			f"""{stone.liberty.__doc__}"""
			return stone.__class__.liberty(stone, point) and self[point].color == Color.empty

		for stone in self:
			stone.liberty = MethodType(stone_liberty, stone)

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

	def __len__(self):
		"""Area of the board."""
		return super().__len__() ** 2

	def __getitem__(self, point: Point | tuple[int, int]):
		"""Set stone of color on point."""
		point = Point(*point, size=self.size) if isinstance(point, tuple) else point
		return super().__getitem__(point.rank + self.size).__getitem__(point.file + self.size)

	def __setitem__(self, point: Point | tuple[int, int], color: Color | str):
		"""Set stone of color on point."""
		color = Color[color] if isinstance(color, str) else color
		self[point].color = color

	def __delitem__(self, point: tuple[int, int]):
		"""Set stone of color on intersection."""
		self[point].color = "empty"

	def __iter__(self):
		"""Iterate through all points on the board."""
		for rank in super().__iter__():
			for point in rank:
				yield point
