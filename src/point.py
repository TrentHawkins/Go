"""Intersections are also called points.

A point on the board where a horizontal line meets a vertical line is called an intersection. Two intersections are said to be
adjacent if they are distinct and connected by a horizontal or vertical line with no other intersections between them.
"""


from dataclasses import dataclass


@dataclass
class Point:
	"""An intersection (point).

	A point on the board where a horizontal line meets a vertical line is called an intersection. Two intersections are said to be
	adjacent if they are distinct and connected by a horizontal or vertical line with no other intersections between them. Points
	act as dsiplacements too, so operations between them is well defined.

	Attributes:
		file: The position of the intersection horizontally.
		rank: The position of the intersection vertically.
		size: Factor to size the board from -size to +size.
			default: The standard Go board size.
	"""

	file: int  # Ranges from -size to +size.
	rank: int  # Ranges from -size to +size.
	size: int = 9  # True size of the board is always an odd number (2 * size + 1).

	def __post_init__(self):
		"""Size must be positive."""
		object.__setattr__(self, 'size', abs(self.size))

	def __hash__(self):
		"""Hash by rank and file."""
		return hash(
			(
				self.file + self.size,
				self.rank + self.size,
			)
		)  # HACK: Avoid CPython's `hash(-2) == hash(-1)`!

	def __eq__(self, other):
		"""Equate by rank and file only."""
		return (
			self.file == other.file and
			self.rank == other.rank and
			self.size == other.size
		)

	def __ne__(self, other):
		"""Equate by rank and file only."""
		return (
			self.file != other.file or
			self.rank != other.rank or
			self.size != other.size
		)

	def __bool__(self) -> bool:
		"""Intersection must be within board boundaries."""
		return (
			-self.size <= self.file <= +self.size and
			-self.size <= self.rank <= +self.size
		)

	def __add__(self, other):
		"""Shift intersection by intersection."""
		return self.__class__(
			self.file + other.file,
			self.rank + other.rank, size=self.size
		)

	def __pos__(self):
		"""Identity of intersection."""
		return self.__class__(
			+self.file,
			+self.rank, size=self.size
		)

	def __sub__(self, other):
		"""Shift intersection by intersection."""
		return self.__class__(
			self.file - other.file,
			self.rank - other.rank, size=self.size
		)

	def __neg__(self):
		"""Opposite of intersection."""
		return self.__class__(
			-self.file,
			-self.rank, size=self.size
		)

	def __mul__(self, times: int):
		"""Propagate intersection times."""
		return self.__class__(
			self.file * times,
			self.rank * times, size=self.size
		)

	def __rmul__(self, times: int):
		"""Propagate intersection times."""
		return self.__class__(
			times * self.file,
			times * self.rank, size=self.size
		)
