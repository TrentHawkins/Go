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
from re import Pattern, compile
from typing import Callable

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

#	Player's name.
	name: str = field(default_factory=input)

#	Player's color and board plus board state two turns ago (ko rule).
	color: Color | str = field(default=Color.empty)

#	The board plus board state two turns ago (ko rule).
	board: Board = field(default_factory=Board)
	state: Board = field(init=False)

#	Legal moves based on linked board.
	moves: Pattern = field(init=False)

#	Pass and allegiance flags.
	passed: bool = field(init=False)
	color_similarity: Callable[[Stone], bool] = field(init=False)

	def __post_init__(self):
		"""Translate player's color name to color."""
		self.state = Board(self.board.copy())
		self.color = Color[self.color] if isinstance(self.color, str) else self.color
		self.moves = compile(f"([-+][0-{self.board.size}])([-+][0-{self.board.size}])")
		self.passed = False

		self.color_similarity = lambda stone: stone.color == self.color

	def base(self, stone: Stone) -> Base:
		"""Get base stone belongs to."""
		return self.board.cluster(stone, condition=self.color_similarity)

	@property
	def bases(self) -> Bases:
		"""Get bases belonging to player."""
		return self.board.clusters(condition=self.color_similarity)

	def move(self):
		"""Read move from standard input."""
		message = "your turn"

	#	Reset pass status.
		self.passed = False

		while True:
			entry = input(f"{self.name}, {message}: ")

			if entry == "pass":
				self.passed = True

				return

			move = self.moves.match(entry)

		#	If move is a legit move (proper format and room on the board).
			if move:
				stone = Stone(*map(int, move.groups()), size=self.board.size, color=self.color)

			#	If stone is placed on an empty intersection.
				if self.board[stone].empty:
					self.board.put(stone)

				#	Prevent suicide and ko.
					if not self.board.liberties(self.base(stone)) or (self.state and self.board == self.state):
						self.board.remove(stone)

					else:
						self.state = Board(self.board.copy())

						return

			message = "\033[Atry again"

	def kill(self):
		"""Kill captured bases of player."""
		for base in self.bases:
			if not self.board.liberties(base):
				for stone in base:
					del stone.color
					del self.board[stone]
