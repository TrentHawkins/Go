"""Go is played on a plane grid of 19 horizontal and 19 vertical lines, called a board.

A point on the board where a horizontal line meets a vertical line is called an intersection. Two intersections are said to be
adjacent if they are distinct and connected by a horizontal or vertical line with no other intersections between them.
"""


from .graph import Undirected
from .intersection import Intersection
from .stone import Stone


class Board(Undirected):
    """Go board.

    The condition that the intersections be "distinct" is included to ensure that an intersection is not considered to be adjacent
    to itself.

    Intersections are also called points.

    There are 361 points on a regular 19×19 board.

    Though 19×19 boards are standard, go can be played on another size board. Particularly common sizes for quick games are 9×9 and
    13×13.
    """

    neighbors: set[Intersection] = {
        Intersection(+1, 00),  # east
        Intersection(00, +1),  # north
        Intersection(-1, 00),  # west
        Intersection(00, -1),  # south
    }

    def __init__(self, size: int = 9):
        """Build board."""
        self.size = size
        self.range = range(-self.size, self.size + 1)

        self.stones = [
            [
                Stone(
                    file,
                    rank,
                ) for rank in self.range
            ] for file in self.range
        ]

    #   Build neighborhoods.
        super(Board, self).__init__(
            {
                node: {
                    node + neighbor for neighbor in self.neighbors
                } for rank in self.stones for node in rank
            }
        )

    def __repr__(self):
        """Draw a board."""
        return \
            "\n    -9-8-7-6-5-4-3-2-1 0+1+2+3+4+5+6+7+8+9    \n\n" + \
            "\n".join(
                f"{rank:+2d}  " + "".join(
                    repr(self.stones[rank][file]) for file in self.range
                ) + f"  {rank:+2d}" for rank in self.range
            ) + \
            "\n\n    -9-8-7-6-5-4-3-2-1 0+1+2+3+4+5+6+7+8+9    \n"
