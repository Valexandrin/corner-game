from typing import Dict, List, Tuple

from game.cell import Cell
from game.checker import Checker


class Player:
    def __init__(self, mode: str='man', color: str='white') -> None:
        self.mode = mode
        self.color = color
        self.checkers: Dict[str, Checker] = {}
        self.checkers_coords = set()
        self.win_coords = set()
        self.farest_point = Tuple[int]

    def add_checker(self, cell: Cell):
        x, y = cell.x, cell.y
        checker = Checker(x, y, self.color)
        self.checkers[checker.id] = checker
        self.checkers_coords.add((x, y))

        cell.checker_id = checker.id
        cell.color = self.color

    def move_checker(self, cell: Cell, path: List[Cell]):
        checker = self.checkers[cell.checker_id]
        for step in path:
            checker.move(step.x, step.y)

    def update_coords(self, start: Cell, end: Cell):
        self.checkers_coords.remove((start.x, start.y))
        self.checkers_coords.add((end.x, end.y))

    def check_win(self):
        res = self.win_coords - self.checkers_coords
