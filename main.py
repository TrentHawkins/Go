"""Main Go."""


from src.board import Board
from src.go import Go

if __name__ == "__main__":
	new_game = Go(board=Board(size=2))

	while True:
		new_game.turn()
