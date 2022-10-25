"""Main Go."""


from src.go import Go

if __name__ == "__main__":
	new_game = Go()

	while True:
		new_game.turn()
