# AoC 22 Day 9
#
# Note for those reading this code:
# - It's as straightforward as possible, mimicking a physics simulation
# - It's not meant to be robust
import sys
from typing import NamedTuple


class Position(NamedTuple):
    """Simple posiiton class
    """
    x: int
    y: int


class Rope:
    """Rope simulator. Rope starts heaped in a single position.

    Note that length is "head-included"
    """
    def __init__(self, initial: Position, length: int) -> None:
        self.head = initial
        self.tails = [initial for _ in range(0, length - 1)]
        # Positions visited by tail: the use of set allows us
        # to have built-in exclusion of twice-visited locations
        self.tail_pos = set()

    def _diff_to_move(self, diff: int) -> int:
        """Given a position difference, return movement (never higher than one, absolute)
        """
        if diff < 0:
            return -1
        elif diff > 0:
            return 1
        return 0

    def _move_tail(self, head: Position, tail: Position) -> Position:
        """Calculate the next position of a tail compared to its head (knot compared to previous)
        """
        x_diff = head.x - tail.x
        y_diff = head.y - tail.y
        # If length is higher than one in any direction
        if max(abs(x_diff), abs(y_diff)) > 1:
            # Move
            to = Position(
                tail.x + self._diff_to_move(x_diff),
                tail.y + self._diff_to_move(y_diff)
            )
            return to
        return tail

    def move(self, direction: str) -> None:
        """Move the head in the given direction by one
        """
        # Gets next head position
        if direction == 'U':
            to = Position(self.head.x, self.head.y + 1)
        elif direction == 'R':
            to = Position(self.head.x + 1, self.head.y)
        elif direction == 'D':
            to = Position(self.head.x, self.head.y - 1)
        else:
            to = Position(self.head.x - 1, self.head.y)
        # Set it
        self.head = to
        prev = self.head
        # Now cascade effect on all knots, each knot has its previous as head
        for i in range(0, len(self.tails)):
            head = prev
            tail = self.tails[i]
            self.tails[i] = self._move_tail(head, tail)
            prev = self.tails[i]
        # Add the very last position to the set
        self.tail_pos.add(self.tails[-1])

    def tail_visited(self) -> int:
        """Print length of tracking position set
        """
        return len(self.tail_pos)


if __name__ == '__main__':
    rope = Rope(Position(0, 0), 10)
    with open(sys.argv[1], 'r') as stream:
        for move in stream:
            dir, step = move.rstrip('\n').split(' ')
            for _ in range(0, int(step)):
                rope.move(dir)
    print(f'Tail visited {rope.tail_visited()} positions')
