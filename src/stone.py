"""Go is played with playing tokens known as stones. Each player has at their disposal an adequate supply of stones of their color.

Traditionally, Black is given 181 stones, and White, 180, to start the game. This is almost always sufficient, but if it turns out
to be insufficient, extra stones will be used.
"""


from dataclasses import dataclass, field
from enum import IntEnum, unique
from typing import ClassVar

from .point import Point


@unique
class Color(IntEnum):
	"""Color of an intersection."""

	black = +1
	empty = +0
	white = -1

	def __str__(self) -> str:
		"""Each color is actually a puc."""
		return {
			self.black: "\U000026AB",
			self.empty: "\U0001F7E4",
			self.white: "\U000026AA",
		}[self]

	def __ne__(self, other) -> bool:
		"""Empty squares are foes with one another."""
		return abs(self - other) == 2

	@classmethod
	def _missing_(cls, _):
		return cls.empty


@dataclass(eq=False)
class Stone(Point):
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

	color: Color | str = field(default=Color.empty)

	def __post_init__(self):
		"""Translate color name to color."""
		self.color = Color[self.color] if isinstance(self.color, str) else self.color

	def __str__(self):
		"""Assume color appearance."""
		return str(self.color) + "\n" if self.file == self.size else str(self.color)
