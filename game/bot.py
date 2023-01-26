from random import choice
from typing import Dict, List, Tuple

from game.board import Board
from game.cell import Cell
from game.checker import Checker
from game.gm import GameManager


class Bot:
    def __init__(self, gm: GameManager) -> None:
        self.gm = gm
        self.board: Board = gm.board
        self.checkers: Dict[str, Checker] = {}
        self.paths: Dict[str, List[Cell]] = {}

    @staticmethod
    def count_distance(pt1: Tuple[int], pt2: Tuple[int]) -> float:
        dx = abs(pt1[0] - pt2[0])
        dy = abs(pt1[1] - pt2[1])
        dist = (dx**2 + dy**2)**0.5
        return dist

    def make_move(self):
        self.checkers = self.gm.curr_player.checkers
        self.write_paths()

        start_cell, path = self.choose_checker()
        end_cell = path[-1]

        self.board.selected_cell = start_cell
        self.board.paths = [path]

        self.gm.make_move(end_cell)
        self.clean()

    def write_paths(self) -> None:
        for checker_id in self.checkers.keys():
            checker = self.checkers[checker_id]
            cell = self.board.field[checker.x][checker.y]
            self.board.get_paths(cell)
            paths = self.board.paths
            if paths:
                best_path = self.get_best_path(paths)
                self.paths[checker_id] = best_path
                self.board.clean()

    def get_best_path(self, paths: List[List[Cell]]) -> List[Cell]:
        shortest = res = None
        goal_cell = self.gm.curr_player.farest_point

        for path in paths:
            for ind, cell in enumerate(path):
                x, y = cell.x, cell.y
                dist = self.count_distance((x, y), goal_cell)
                if not shortest:
                    shortest = dist
                    res = path[0:ind+1]
                if shortest > dist:
                    shortest = dist
                    res = path[0:ind+1]
        return res

    def choose_checker(self) -> Tuple[Cell, List[Cell]]:
        longest: int = 0
        for path in self.paths.values():
            if len(path) > longest:
                longest = len(path)

        best_checkers: List[Checker] = []
        for checker_id, path in self.paths.items():
            if len(path) == longest:
                best_checkers.append(self.checkers[checker_id])

        # lost_behind = self.find_lost(best_checkers)
        lost_behind = choice(best_checkers)
        x, y = lost_behind.x, lost_behind.y
        chosen_cell = self.gm.board.field[x][y]
        checker_id = chosen_cell.checker_id
        path = self.paths[checker_id]

        return chosen_cell, path

    def find_lost(self, checkers) -> Checker:
        goal_cell = self.gm.curr_player.farest_point
        lost_behind: Checker = None
        dist = None
        for checker in checkers:
            x, y = checker.x, checker.y
            new_dist = self.count_distance((x, y), goal_cell)
            if not dist:
                dist = new_dist
                lost_behind = checker
            if new_dist < dist:
                dist = new_dist
                lost_behind = checker

        return lost_behind

    def clean(self):
        self.paths = {}
