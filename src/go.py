"""Go is an abstract strategy board game for two players in which the aim is to surround more territory than the opponent.

The playing pieces are called stones. One player uses the white stones and the other, black. The players take turns placing the
stones on the vacant intersections (points) of a board. Once placed on the board, stones may not be moved, but stones are removed
from the board if the stone (or group of stones) is surrounded by opposing stones on all orthogonally adjacent points, in which
case the stone or group is captured. The game proceeds until neither player wishes to make another move. When a game concludes, the
winner is determined by counting each player's surrounded territory along with captured stones and komi (points added to the score
of the player with the white stones as compensation for playing second). Games may also be terminated by resignation.

The standard Go board has a 19×19 grid of lines, containing 361 points. Beginners often play on smaller 9×9 and 13×13 boards.

Go is an adversarial game with the objective of surrounding a larger total area of the board with one's stones than the opponent.
As the game progresses, the players position stones on the board to map out formations and potential territories. Contests between
opposing formations are often extremely complex and may result in the expansion, reduction, or wholesale capture and loss of
formation stones.

A basic principle of Go is that a group of stones must have at least one open point bordering the group, known as a liberty, to
remain on the board. One or more liberties enclosed within a group is called an eye, and a group with two or more eyes cannot be
captured, even if surrounded.  Such groups are said to be unconditionally alive.

The general strategy is to expand one's territory, attack the opponent's weak groups (groups that can be killed), and always stay
mindful of the life status of one's own groups. The liberties of groups are countable. Situations where mutually opposing groups
must capture each other or die are called capturing races, or semeai. In a capturing race, the group with more liberties will
ultimately be able to capture the opponent's stones. Capturing races and the elements of life or death are the primary challenges
of Go.

Players may pass rather than place a stone if they think there are no further opportunities for profitable play. The game ends when
both players pass or when one player resigns. In general, to score the game, each player counts the number of unoccupied points
surrounded by their stones and then subtracts the number of stones that were captured by the opponent. The player with the greater
score (after adjusting for komi) wins the game.

In the opening stages of the game, players typically establish positions (or bases) in the corners and around the sides of the
board. These bases help to quickly develop strong shapes which have many options for life (self-viability for a group of stones
that prevents capture) and establish formations for potential territory. Players usually start in the corners because establishing
territory is easier with the aid of two edges of the board. Established corner opening sequences are called joseki and are often
studied independently.

Dame are points that lie in between the boundary walls of black and white, and as such are considered to be of no value to either
side. Seki are mutually alive pairs of white and black groups where neither has two eyes. A ko (Chinese and Japanese: 劫) is a
repeated-position shape that may be contested by making forcing moves elsewhere. After the forcing move is played, the ko may be
"taken back" and returned to its original position. Some ko fights may be important and decide the life of a large group, while
others may be worth just one or two points. Some ko fights are referred to as picnic kos when only one side has a lot to lose. The
Japanese call it a hanami (flower-viewing) ko.
"""


from dataclasses import dataclass, field
from datetime import datetime
from itertools import cycle

from .board import Board
from .player import Player
from .stone import Stone


@dataclass
class Go:
	"""A game of Go.

	Players: Go is a game between two players, called Black and White.

	Board: Go is played on a plain grid of 19 horizontal and 19 vertical lines, called a board.
	-	Intersection: A point on the board where a horizontal line meets a vertical line is called an intersection.
	-	Adjacent: Two intersections are said to be adjacent if they are connected by a horizontal or vertical line with no other
		intersections between them.

	Stones: Go is played with playing tokens known as stones. Each player has at their disposal an adequate supply (usually 180) of
	stones of the same color.

	Positions: At any time in the game, each intersection on the board is in one and only one of the following three states:
	-	empty;
	-	occupied by a black stone; or
	-	occupied by a white stone.
	A position consists of an indication of the state of each intersection.
	-	Connected: Two placed stones of the same color (or two empty intersections) are said to be connected if it is possible to
		draw a path from one intersection to the other by passing through adjacent intersections of the same state (empty, occupied
		by white, or occupied by black).
	-	Liberty: In a given position, a liberty of a stone is an empty intersection adjacent to that stone or adjacent to a stone
		which is connected to that stone.

	Initial position: At the beginning of the game, the board is empty.

	Turns: Black moves first. The players alternate thereafter.

	Moving: When it is their turn, a player may either pass (by announcing "pass" and performing no action) or play. A play
	consists of the following steps (performed in the prescribed order):
	-	Playing a stone: Placing a stone of their color on an empty intersection (chosen subject to Rule 8 and, if it is in effect,
		to Optional Rule 7A). It can never be moved to another intersection after being played.
	-	Capture: Removing from the board any stones of their opponent's color that have no liberties.
	-	Self-capture: Removing from the board any stones of their own color that have no liberties.

	Prohibition of repetition: A play is illegal if it would have the effect (after all steps of the play have been completed) of
	creating a position that has occurred previously in the game.

	End: The game ends when both players have passed consecutively. The final position is the position on the board at the time the
	players pass consecutively.
	-	Territory: In the final position, an empty intersection is said to belong to a player's territory if all stones adjacent to
		it or to an empty intersection connected to it are of that player's color.
	-	Area: In the final position, an intersection is said to belong to a player's area if either:
		-	it belongs to that player's territory; or
		-	it is occupied by a stone of that player's color.
		Score: A player's score is the number of intersections in their area in the final position.

	Winner: If one player has a higher score than the other, then that player wins. Otherwise, the game is a draw.
	"""

#	Board linked to the game.
	board: Board = field(default_factory=Board)

#	Players of the game.
	black: Player = field(default=Player(board=board, color="black", name="Foo"))
	white: Player = field(default=Player(board=board, color="white", name="Bar"))

	players: cycle = field(init=False)

	def __post_init__(self):
		"""Set player cycle."""
		self.players = cycle(
			[
				self.black,
				self.white,
			]
		)

	def __str__(self):
		"""Display current game state."""
		return f"\033[H\033[J{self.__class__.__name__}: {datetime.today().replace(microsecond=0)}\n{self.board}"

	def turn(self):
		"""Play a turn."""
		current: Player = next(self.players)

	#	Print game state.
		print(self)

	#	Read next move.
		current.move()

		if self.black.passed and self.white.passed:
			exit("GAME OVER")
