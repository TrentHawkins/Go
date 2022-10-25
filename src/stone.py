"""Go is played with playing tokens known as stones. Each player has at their disposal an adequate supply of stones of their color.

Traditionally, Black is given 181 stones, and White, 180, to start the game. This is almost always sufficient, but if it turns out
to be insufficient, extra stones will be used.
"""


from dataclasses import dataclass, field
from enum import Enum, unique
from typing import ClassVar

from .point import Point


@unique
class Color(Enum):
	"""Color of an intersection."""

	black = "\U000026AB"
	empty = "\U0001F7E4"
	white = "\U000026AA"

	def __str__(self) -> str:
		"""Each color is actually a puc."""
		return self.value

	def __bool__(self):
		"""Is false if empty."""
		return self != self.empty

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
			default: Empty.
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

	def __bool__(self) -> bool:
		"""Stone must be within board boundaries and empty."""
		return super().__bool__()

	def __add__(self, other: Point):
		f"""Shift stone by intersection."""
		return self.__class__(
			self.file + other.file,
			self.rank + other.rank, size=self.size, color=self.color
		)

	def __sub__(self, other: Point):
		f"""Shift stone by intersection."""
		return self.__class__(
			self.file - other.file,
			self.rank - other.rank, size=self.size, color=self.color
		)

	@property
	def empty(self):
		"""Is intersection empty."""
		return self.color == Color.empty
