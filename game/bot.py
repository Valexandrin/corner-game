from random import choice
from typing import Dict, List, Tuple, Set

from game.board import Board
from game.cell import Cell
from game.checker import Checker
from game.gm import GameManager


class Bot:
    def __init__(self, gm: GameManager) -> None:
        self.gm = gm
        self.board: Board = gm.board
        self.avaliable_checkers: Dict[Checker, List[List[Cell]]] = {}
        self.winners: Set[Checker] = set()
        self.farest_win_point: Tuple[int] = None

    @staticmethod
    def count_distance(pt1: Tuple[int], pt2: Tuple[int]) -> float:
        dx = abs(pt1[0] - pt2[0])
        dy = abs(pt1[1] - pt2[1])
        dist = (dx**2 + dy**2)**0.5
        return dist

    def clean(self):
        self.avaliable_checkers = {}
        self.winners = set()
        self.farest_win_point = None

    def make_move(self):
        self.get_farest_win_point()
        self.get_avaliable_checkers()
        win_distances = self.get_win_distances()
        target_ratio = 0.3
        start_cell, path = self.choose_checker(win_distances, target_ratio)
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
            if (cell.x, cell.y) in self.gm.curr_player.win_coords:
                self.winners.add(checker)
            self.board.get_paths(cell)
            paths = self.board.paths
            if paths:
                self.avaliable_checkers[checker] = paths
                self.board.clean()

        if len(self.avaliable_checkers.keys() - self.winners) > 0:
            for item in self.winners:
                if item in self.avaliable_checkers.keys():
                    self.avaliable_checkers.pop(item)

    def get_farest_win_point(self):
        win_cells = self.gm.curr_player.win_coords
        farest_cell = self.gm.curr_player.farest_point
        dist = -1
        for x, y in win_cells:
            cell: Cell = self.board.field[x][y]
            if cell.color == self.gm.curr_player.color:
                continue

            new_dist = self.count_distance((x, y), farest_cell)
            if dist == -1:
                dist = new_dist
                self.farest_win_point = (x, y)
            if new_dist < dist:
                dist = new_dist
                self.farest_win_point = (x, y)

    def get_win_distances(self):
        distances: Dict[float, Checker] = {}
        for checker in self.avaliable_checkers:
            x, y = checker.x, checker.y
            distance = self.count_distance((x, y), self.farest_win_point)
            distances[distance] = checker
        return distances

    def get_parts(self, distances):
        far_checkers, near_checkers = {}, {}
        values = list(distances.keys())
        average = sum(values)/len(values)
        for val in values:
            checker = (distances[val])
            if val > average:
                far_checkers[checker] = val
            else:
                near_checkers[checker] = val

        return far_checkers, near_checkers

    def get_best_path(self, checker, paths: List[List[Cell]]) -> List[Cell]:
        goal_cell = self.farest_win_point

        x, y = checker.x, checker.y
        shortest = self.count_distance((x, y), goal_cell)
        best_path = []

        for path in paths:
            for ind, cell in enumerate(path):
                x, y = cell.x, cell.y
                dist = self.count_distance((x, y), goal_cell)
                if shortest > dist:
                    shortest = dist
                    best_path = path[0:ind+1]
                if shortest == dist:
                    best_path = path[0:ind+1] if len(path[0:ind+1]) < len(best_path) else best_path

        if not best_path:
            return paths[0]
        return best_path

    def choose_checker(self, win_distances, ratio) -> Tuple[Cell, List[Cell]]:
        far_checkers, near_checkers = self.get_parts(win_distances)
        far_size = len(far_checkers.keys())
        near_size = len(near_checkers.keys())
        if far_size/near_size < ratio:
            print('lost_behind', far_size/near_size)
            lost_behind = self.find_lost(far_checkers)
            checker, path = lost_behind
        else:
            print('best_checkers', far_size/near_size)
            best_checker = self.get_best_checker()
            checker, path = best_checker

        x, y = checker.x, checker.y
        chosen_cell = self.gm.board.field[x][y]

        return chosen_cell, path

    def find_lost(self, checkers: Dict[Checker, float]) -> Dict[Checker, List[Cell]]:
        lost_behind: Checker = choice(list(checkers.keys()))
        dist = 0
        for checker, new_dist in checkers.items():
            if new_dist > dist:
                dist = new_dist
                lost_behind = checker

        checker_paths = self.avaliable_checkers[lost_behind]
        checker_paths = sorted(checker_paths, key=len)
        best_path = checker_paths[0]

        return lost_behind, best_path

    def get_best_checker(self) -> Dict[Checker, List[Cell]]:
        longest: int = 0
        checkers: Dict[Checker, List[Cell]] = {}
        for checker, paths in self.avaliable_checkers.items():
            best_path = self.get_best_path(checker, paths)
            checkers[checker] = best_path

        for path in checkers.values():
            if len(path) > longest:
                longest = len(path)

        best_checkers: Dict[Checker, List[Cell]] = {}
        for checker, path in checkers.items():
            if len(path) == longest:
                best_checkers[checker] = path

        best_checker = choice(list(best_checkers.keys()))
        best_path = best_checkers[best_checker]

        return best_checker, best_path
