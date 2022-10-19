"""Go is a game between two players, called Black and White.

The choice of black or white is traditionally done by chance between players of even strength. The method of selection is called
nigiri. One player, whom we will call Player A, takes a handful of white stones; Player B then places either one or two black
stones on the board, indicating "even" or "odd". Player A counts the number stones in their hand to determine whether there is an
odd or even number. If the number of stones matches the other player's selection of "even" or "odd", Player B will play the black
stones; if not, they will take the white stones.

When players are of different strengths, the weaker player takes black. Black may also pre-place several handicap stones before
play begins, to compensate for the difference in strength.
"""


class Player:
    """A player.

    Contains the clusters of the board graph belonging to the player.
    Via mutability tricks, the clusters still have access to neighborhoods on the whole board to use as liberties.
    """

    ...
