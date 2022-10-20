"""Go is played with playing tokens known as stones. Each player has at their disposal an adequate supply of stones of their color.

Traditionally, Black is given 181 stones, and White, 180, to start the game. This is almost always sufficient, but if it turns out
to be insufficient, extra stones will be used.
"""


from dataclasses import dataclass
from enum import IntFlag, unique

from .point import Point


@unique
class Color(IntFlag):
	"""Color of an intersection."""

	black = +1
	empty = 00
	white = -1

	def __repr__(self) -> str:
		"""Each color is actually a puc."""
		return {
			+1: "\U000026AB",
			00: "\U0001F7E4",
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

	point: Point
	color: Color = Color.empty

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
