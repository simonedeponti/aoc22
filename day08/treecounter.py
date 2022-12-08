# AoC 22 Day 8
#
# Note for those reading this code:
# - It's as straightforward as possible, making the functions more generic
#   without adding heuristic optimizations
# - It's not meant to be robust

import sys
from typing import Iterable, NamedTuple


class LOS(NamedTuple):
    """Line of sight object.

    Keeps iterable of trees (heights) visible from up, right, left and down
    """
    up: Iterable[int]
    right: Iterable[int]
    down: Iterable[int]
    left: Iterable[int]


class TreeGrid:
    """Main utility class.

    Trees are kept in a monodimensional array
    """
    def __init__(self, trees: list[int], width: int, height: int) -> None:
        self.trees = trees
        self.width = width
        self.height = height

    def up_pos(self, x: int, y: int) -> Iterable[int]:
        """Returns positions in the array looking up (not trees), in order from the tree
        """
        for i in range(y - 1, -1, -1):
            yield (i * self.width) + x

    def down_pos(self, x: int, y: int) -> Iterable[int]:
        """Returns positions in the array looking down (not trees), in order from the tree
        """
        for i in range(y + 1, self.height):
            yield (i * self.width) + x

    def right_pos(self, x: int, y: int) -> Iterable[int]:
        """Returns positions in the array looking right (not trees), in order from the tree
        """
        for i in range(x + 1, self.width):
            yield (y * self.width) + i

    def left_pos(self, x: int, y: int) -> Iterable[int]:
        """Returns positions in the array looking left (not trees), in order from the tree
        """
        for i in range(x - 1, -1, -1):
            yield (y * self.width) + i

    def get_los(self, x: int, y: int) -> LOS:
        """Returns trees in LOS
        """
        return LOS(
            (self.trees[i] for i in self.up_pos(x, y)),
            (self.trees[i] for i in self.right_pos(x, y)),
            (self.trees[i] for i in self.down_pos(x, y)),
            (self.trees[i] for i in self.left_pos(x, y))
        )

    def __str__(self) -> str:
        return f'TreeGrid({self.trees}, {self.width}, {self.height})'

    def visible_trees(self) -> int:
        """Calculates visible trees
        """
        visible_trees = 0
        for x in range(0, self.width):
            for y in range(0, self.height):
                los = self.get_los(x, y)
                los_up = max(los.up, default=-1)
                los_right = max(los.right, default=-1)
                los_down = max(los.down, default=-1)
                los_left = max(los.left, default=-1)
                tree_h = self.trees[(y * self.width) + x]
                if tree_h > los_up or tree_h > los_right or tree_h > los_down or tree_h > los_left:
                    visible_trees += 1
        return visible_trees

    def viewing_score(self, x: int, y: int) -> int:
        """Calculates viewing score for a tree
        """
        los = self.get_los(x, y)
        tree_h = self.trees[(y * self.width) + x]
        total_score = 1
        for dir in los:
            dir_score = 0
            for t in dir:
                dir_score += 1
                if t >= tree_h:
                    break
            total_score = total_score * dir_score
        return total_score

    def max_score(self) -> int:
        """Calculates max score for all trees
        """
        max_score = 0
        for x in range(0, self.width):
            for y in range(0, self.height):
                tree_score = self.viewing_score(x, y)
                max_score = max(max_score, tree_score)
        return max_score

    @staticmethod
    def make(file: str):
        """Deserialization from txt to object
        """
        trees = []
        width = 1
        height = 1
        with open(file, 'r') as stream:
            for ln, line in enumerate(stream):
                height = ln + 1
                for cn, char in enumerate(line.rstrip('\n')):
                    width = cn + 1
                    trees.append(int(char))
        return TreeGrid(trees, width, height)


if __name__ == '__main__':
    trees = TreeGrid.make(sys.argv[1])
    print('Visible trees: ', trees.visible_trees())
    print('Max score: ', trees.max_score())
