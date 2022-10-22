"""Go is a game between two players, called Black and White.

The choice of black or white is traditionally done by chance between players of even strength. The method of selection is called
nigiri. One player, whom we will call Player A, takes a handful of white stones; Player B then places either one or two black
stones on the board, indicating "even" or "odd". Player A counts the number stones in their hand to determine whether there is an
odd or even number. If the number of stones matches the other player's selection of "even" or "odd", Player B will play the black
stones; if not, they will take the white stones.

When players are of different strengths, the weaker player takes black. Black may also pre-place several handicap stones before
play begins, to compensate for the difference in strength.
"""


from dataclasses import dataclass, field

from .board import Base, Bases, Board
from .stone import Color, Stone


@dataclass
class Player:
	"""A player.

	Contains the clusters of the board graph belonging to the player.
	Via mutability tricks, the clusters still have access to neighborhoods on the whole board to use as liberties.

	Attributes:
		name: Of player.
		color: Of player's stones.
		board: The player is playing on.
	"""

	name: str = field(default_factory=input)

	color: Color | str = field(default=Color.empty)
	board: Board = field(default_factory=Board)

	def __post_init__(self):
		"""Translate player's color name to color."""
		self.color = Color[self.color] if isinstance(self.color, str) else self.color
		self.color_similarity = lambda stone: stone.color == self.color

	def base(self, stone: Stone) -> Base:
		"""Get base stone belongs to."""
		return self.board.cluster(stone, condition=self.color_similarity)

	@property
	def bases(self) -> Bases:
		"""Get bases belonging to player."""
		return self.board.clusters(condition=self.color_similarity)

	def kill(self):
		"""Kill captured bases of player."""
		for base in self.bases:
			if not self.board.liberties(base):
				for stone in base:
					del stone.color
					del self.board[stone]
