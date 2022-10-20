"""Go is played with playing tokens known as stones. Each player has at their disposal an adequate supply of stones of their color.

Traditionally, Black is given 181 stones, and White, 180, to start the game. This is almost always sufficient, but if it turns out
to be insufficient, extra stones will be used.
"""


from dataclasses import dataclass
from enum import IntFlag, unique
from typing import ClassVar

from .point import Point


@unique
class Color(IntFlag):
	"""Color of an intersection."""

	black = +1
	empty = +0
	white = -1

	def __repr__(self) -> str:
		"""Each color is actually a puc."""
		return {
			+1: "\U000026AB",
			+0: "\U0001F7E4",
			-1: "\U000026AA",
		}[self]

	def __ne__(self, other) -> bool:
		"""Empty squares are foes with one another."""
		return abs(self - other) == 2


@dataclass(repr=False, eq=False)
class Stone:
	"""A stone.

	Go is played with playing tokens known as stones.
	Each player has at their disposal an adequate supply of stones of their color.

	Attributes:
		color: Allegiance of stone.
		point: Intersection the stone is on (irrelevant on which board.
	"""

	adjacencies: ClassVar[set[Point]] = {
		Point(+1, +0),  # east
		Point(+0, +1),  # north
		Point(-1, +0),  # west
		Point(+0, -1),  # south
	}

	point: Point | tuple[int, int]
	color: Color | str = Color.empty

	def __post_init__(self):
		"""Translate semantic input to actual attributes."""
		self.point = Point(*self.point) if isinstance(self.point, tuple) else self.point
		self.color = Color[self.color] if isinstance(self.color, str) else self.color

	def __repr__(self):
		"""Assume color appearance."""
		return repr(self.color)

	def __hash__(self):
		"""Hash only based on intersection."""
		return hash(self.point)

	def __eq__(self, other):
		"""Compare based on allegiance only."""
		return self.color == other.color

	def __ne__(self, other):
		"""Compare based on allegiance only."""
		return self.color != other.color

	def liberty(self, point: Point) -> bool:
		"""Is point a liberty of stone."""
		return bool(point)

	@property
	def liberties(self):
		"""Adjacent points."""
		liberties = set[Point]()

		for adjacent in self.adjacencies:
			point = self.point + adjacent  # type: ignore

			if self.liberty(point):
				liberties.add(point)

		return liberties
