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
        self.farest_win_point: Tuple[int] = gm.curr_player.farest_point

    @staticmethod
    def count_distance(pt1: Tuple[int], pt2: Tuple[int]) -> float:
        dx = abs(pt1[0] - pt2[0])
        dy = abs(pt1[1] - pt2[1])
        dist = (dx**2 + dy**2)**0.5
        return dist

    @staticmethod
    def get_fars(distances: Dict[float, Checker]) -> Dict[float, Checker]:
        far_checkers = {}
        values = list(distances.keys())
        average = sum(values)/len(values)

        for val in values:
            if val >= average:
                checker = (distances[val])
                far_checkers[val] = checker

        return far_checkers

    def clean(self):
        self.avaliable_checkers = {}
        self.winners = set()

    def make_move(self):
        self.get_farest_win_point()
        self.get_avaliable_checkers()

        self.board.selected_cell, path = self.choose_checker()
        self.board.paths = [path]
        end_cell = path[-1]
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

    def update_avaliables_checkers(self):
        if len(self.avaliable_checkers.keys() - self.winners) > 0:
            for item in self.winners:
                if item in self.avaliable_checkers.keys():
                    self.avaliable_checkers.pop(item)

    def choose_checker(self) -> Tuple[Cell, List[Cell]]:
        chosen_cell, path = self.get_win_step()
        if chosen_cell and path:
            return chosen_cell, path

        self.update_avaliables_checkers()

        far_checkers = self.get_fars(self.get_win_distances())
        if len(far_checkers) < 3:
            checker, path = self.find_lost(far_checkers)
        else:
            checker, path = self.get_best()

        chosen_cell = self.gm.board.field[checker.x][checker.y]
        return chosen_cell, path

    def get_win_step(self) -> Tuple[Cell, List[Cell]]:
        fr_pt = self.gm.curr_player.farest_point
        for checker, paths in self.avaliable_checkers.items():
            for path in paths:
                for ind, cell in enumerate(path):
                    if (cell.x, cell.y) == self.farest_win_point:
                        ch_x, ch_y = checker.x, checker.y
                        curr_pt = self.count_distance((ch_x, ch_y), fr_pt)
                        new_pt = self.count_distance((cell.x, cell.y), fr_pt)
                        if new_pt > curr_pt:
                            continue
                        chosen_cell = self.gm.board.field[ch_x][ch_y]
                        return chosen_cell, path[:ind+1]
        return None, None

    def get_farest_win_point(self):
        dist = float('inf')
        for x, y in self.gm.curr_player.win_coords:
            cell = self.board.field[x][y]
            if cell.color != None:
                continue

            new_dist = self.count_distance((x, y), self.gm.curr_player.farest_point)
            if new_dist < dist:
                dist = new_dist
                self.farest_win_point = (x, y)

    def get_win_distances(self):
        distances: Dict[float, Checker] = {}
        for checker in self.avaliable_checkers:
            distance = self.count_distance((checker.x, checker.y), self.farest_win_point)
            distances[distance] = checker
        return distances

    def get_best_path(self, checker: Checker, paths: List[List[Cell]]) -> List[Cell]:
        goal_cell = self.farest_win_point
        shortest = self.count_distance((checker.x, checker.y), goal_cell)
        best_path = []

        for path in paths:
            for ind, cell in enumerate(path):
                dist = self.count_distance((cell.x, cell.y), goal_cell)
                if shortest > dist:
                    shortest = dist
                    best_path = path[:ind+1]
                if shortest == dist:
                    if len(path[:ind+1]) < len(best_path):
                        best_path = path[:ind+1]

        if not best_path:
            paths = sorted(paths, key=len)
            return paths[0]
        return best_path

    def find_lost(self, checkers: Dict[float, Checker]) -> Dict[Checker, List[Cell]]:
        lost_behind: Checker = None
        dist = 0

        for new_dist, checker in checkers.items():
            if new_dist > dist:
                dist = new_dist
                lost_behind = checker

        paths = self.avaliable_checkers[lost_behind]
        return lost_behind, self.get_best_path(lost_behind, paths)

    def get_best(self) -> Dict[Checker, List[Cell]]:
        longest: int = 0
        checkers: Dict[Checker, List[Cell]] = {}

        for checker, paths in self.avaliable_checkers.items():
            best_path = self.get_best_path(checker, paths)
            checkers[checker] = best_path

            if len(best_path) > longest:
                longest = len(best_path)

        best_checkers: Dict[Checker, List[Cell]] = {}
        for checker, path in checkers.items():
            if len(path) == longest:
                best_checkers[checker] = path

        best_checker = choice(list(best_checkers.keys()))
        best_path = best_checkers[best_checker]

        return best_checker, best_path
