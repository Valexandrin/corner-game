from typing import List

from game.cell import Cell
from game.player import Player


class Board:
    def __init__(self, cells_number: int=8, corner_size: List[int]=[3, 3]) -> None:
        self.checked_cells = set()
        self.selected_cell = None
        self.paths = []
        self.cells_number = cells_number
        self.field = [[Cell(i, j) for j in range(0, cells_number)] for i in range(0, cells_number)]
        self.top = {
            'x': range(cells_number - corner_size[0], cells_number),
            'y': range(0, corner_size[1]),
        }
        self.bottom = {
            'x': range(0, corner_size[0]),
            'y': range(cells_number - corner_size[1], cells_number)}

    def put_checkers(self, p1: Player, p2: Player):
        for row in self.field:
            for cell in row:
                x, y = cell.x, cell.y
                if x in self.top['x'] and y in self.top['y']:
                    p2.add_checker(cell)
                    p1.win_coords.add((x, y))
                if cell.x in self.bottom['x'] and cell.y in self.bottom['y']:
                    p1.add_checker(cell)
                    p2.win_coords.add((x, y))

    def select_cells(self, chosen_cell: Cell):
        if self.selected_cell:
            self.clean()
        self.grip(chosen_cell)
        self.get_paths(chosen_cell)
        self.show_paths()

    def update_cells(self, new_pos: Cell):
        new_pos.color = self.selected_cell.color
        new_pos.checker_id = self.selected_cell.checker_id
        self.selected_cell.clean()

    def is_out_of(self, val: int):
        limit = range(self.cells_number)
        if val not in limit:
            return True

    def is_valid(self, cell: Cell):
        if cell.color != None:
            return
        if cell in self.checked_cells:
            return
        return True

    def get_paths(self, cell: Cell, level=1):
        steps = [
            [cell.x+1, cell.y],
            [cell.x-1, cell.y],
            [cell.x, cell.y+1],
            [cell.x, cell.y-1],
        ]
        jumps = [
            [cell.x+2, cell.y],
            [cell.x-2, cell.y],
            [cell.x, cell.y+2],
            [cell.x, cell.y-2],
        ]
        for pos in range(len(steps)):
            i, j = steps[pos]
            if self.is_out_of(i) or self.is_out_of(j):
                continue

            next_cell = self.field[i][j]
            if next_cell.color == None:
                if level == 1:
                    self.paths.append([next_cell])
                continue

            i, j = jumps[pos]
            if self.is_out_of(i) or self.is_out_of(j):
                continue

            next_cell = self.field[i][j]
            if not self.is_valid(next_cell):
                continue
            self.checked_cells.add(cell)

            last_path = []

            if self.paths and self.paths[-1][-1] == cell:
                [last_path.append(cell) for cell in self.paths[-1]]
                self.paths[-1].append(next_cell)
            else:
                self.paths.append([next_cell])

            self.get_paths(next_cell, level+1)

            if last_path:
                if last_path not in self.paths:
                    self.paths.append(last_path)

    def choose_path(self, cell: Cell):
        valid_path = []
        for path in self.paths:
            if path[-1] != cell:
                continue
            if not valid_path:
                valid_path = path
            if len(path) < len(valid_path):
                valid_path = path

        return valid_path

    def show_paths(self):
        for path in self.paths:
            for cell in path:
                cell.select("yellow")

    def clean(self):
        self.selected_cell.released()
        for path in self.paths:
            for cell in path:
                cell.released()

        self.paths = []
        self.checked_cells = set()
        self.selected_cell = None

    def grip(self, cell: Cell):
        cell.select("green")
        self.selected_cell = cell
