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
        self.farest_empty_win_point: Tuple[int] = tuple()
        self.avaliable_checkers: Dict[Checker, List[List[Cell]]] = {}

    @staticmethod
    def count_distance(pt1: Tuple[int], pt2: Tuple[int]) -> float:
        dx = abs(pt1[0] - pt2[0])
        dy = abs(pt1[1] - pt2[1])
        dist = (dx**2 + dy**2)**0.5
        return dist

    def clean(self):
        self.avaliable_checkers = {}
        self.farest_empty_cell = None

    def make_move(self):
        self.get_avaliable_checkers()
        self.get_farest_win_point()

        start_cell, path = self.choose_checker()
        end_cell = path[-1]

        self.board.selected_cell = start_cell
        self.board.paths = [path]

        self.gm.make_move(end_cell)
        self.clean()

    def get_avaliable_checkers(self) -> None:
        checkers = self.gm.curr_player.checkers
        for checker_id in checkers.keys():
            checker = checkers[checker_id]
            cell = self.board.field[checker.x][checker.y]
            self.board.get_paths(cell)
            paths = self.board.paths
            if paths:
                # best_path = self.get_best_path(paths)
                self.avaliable_checkers[checker] = paths
                self.board.clean()

    def get_farest_win_point(self):
        win_cells = self.gm.curr_player.win_coords
        farest_cell = self.gm.curr_player.farest_point
        dist = None
        for x, y in win_cells:
            cell: Cell = self.board.field[x][y]
            if cell.color == self.gm.curr_player.color:
                continue
            new_dist = self.count_distance((x, y), farest_cell)
            if not dist:
                dist = new_dist
                self.farest_empty_win_point = (x, y)
            if new_dist < dist:
                dist = new_dist
                self.farest_empty_win_point = (x, y)

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
        for path in self.avaliable_checkers.values():
            if len(path) > longest:
                longest = len(path)

        best_checkers: List[Checker] = []
        for checker_id, path in self.avaliable_checkers.items():
            if len(path) == longest:
                best_checkers.append(self.checkers[checker_id])

        # lost_behind = self.find_lost(best_checkers)
        lost_behind = choice(best_checkers)
        x, y = lost_behind.x, lost_behind.y
        chosen_cell = self.gm.board.field[x][y]
        checker_id = chosen_cell.checker_id
        path = self.avaliable_checkers[checker_id]

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
