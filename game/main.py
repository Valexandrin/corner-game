import time
import tkinter as tk
from random import shuffle

cell_size = 100
cells_number = 8
limit = range(cells_number)
side_size = cell_size * cells_number
views = {
    'white': "game/images/white.png",
    'black': "game/images/black.png",
}
corner_size = [4, 3]

root = tk.Tk()
root.title("Уголки")
root.resizable(0, 0)
canv = tk.Canvas(
    root,
    width=side_size,
    height=side_size,
    highlightthickness = 0,
)
canv.pack()


class Board:
    def __init__(self, size) -> None:
        self.checked_cells = set()
        self.selected_cell = None
        self.paths = []
        self.field = [[Cell(i, j) for j in range(0, size)] for i in range(0, size)]
        self.top = {
            'x': range(cells_number - corner_size[0], cells_number),
            'y': range(0, corner_size[1]),
        }
        self.bottom = {
            'x': range(0, corner_size[0]),
            'y': range(cells_number - corner_size[1], cells_number)}

    def put_checkers(self, p1, p2):
        for row in self.field:
            for cell in row:
                x, y = cell.x, cell.y
                if x in self.top['x'] and y in self.top['y']:
                    p2.add_checker(cell)
                    p1.win_coords.add((x, y))
                if cell.x in self.bottom['x'] and cell.y in self.bottom['y']:
                    p1.add_checker(cell)
                    p2.win_coords.add((x, y))

    def select_cells(self, chosen_cell):
        if self.selected_cell:
            self.clean()
        self.grip(chosen_cell)
        self.get_paths(chosen_cell)
        self.show_paths()

    def update_cells(self, new_pos):
        new_pos.color = self.selected_cell.color
        new_pos.checker_id = self.selected_cell.checker_id
        self.selected_cell.clean()

    @staticmethod
    def is_out_of(val):
        if val not in limit:
            return True

    def is_valid(self, cell):
        if cell.color != None:
            return
        if cell in self.checked_cells:
            return
        return True

    def get_paths(self, cell, level=1):
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

    def choose_path(self, cell):
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

    def grip(self, cell):
        cell.select("green")
        self.selected_cell = cell


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None
        self.checker_id = None
        self.id = canv.create_rectangle(
            (x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size),
            fill = "#FFD39B",
        )

    def select(self, color):
        canv.itemconfig(self.id, outline=color, width=3)

    def released(self):
        canv.itemconfig(self.id, outline="black", width=1)

    def clean(self):
        self.color = self.checker_id = None


class Player:
    def __init__(self, mode, color) -> None:
        self.mode = mode
        self.color = color
        self.checkers = {}
        self.checkers_coords = set()
        self.win_coords = set()

    def add_checker(self, cell):
        x, y = cell.x, cell.y
        checker = Checker(x, y, self.color)
        self.checkers[checker.id] = checker
        self.checkers_coords.add((x, y))

        cell.checker_id = checker.id
        cell.color = self.color

    def move_checker(self, cell, path):
        checker = self.checkers[cell.checker_id]
        for step in path:
            checker.move(step.x, step.y)

    def update_coords(self, start, end):
        self.checkers_coords.remove((start.x, start.y))
        self.checkers_coords.add((end.x, end.y))

    def check_win(self):
        res = self.win_coords - self.checkers_coords
        print(len(res))


class Checker:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.img = tk.PhotoImage(file=views[color])
        self.id = canv.create_image(x*cell_size, y*cell_size, image=self.img, anchor=tk.NW)

    def move(self, *new_position):
        old_x, old_y = self.x, self.y
        self.x, self.y = new_position
        step_x = self.x - old_x
        step_y = self.y - old_y
        for i in range(26):
            canv.coords(
                self.id,
                (old_x + step_x * i * 0.04) * cell_size,
                (old_y + step_y * i * 0.04) * cell_size,
            )
            canv.update()
            time.sleep(0.01)


class GameManager:
    def __init__(self):
        self.curr_player = None

    def create_board(self):
        self.board = Board(cells_number)

    def fill_board(self):
        self.board.put_checkers(self.p1, self.p2)

    def create_players(self, mode1, mode2):
        colors = list(views.keys())
        shuffle(colors)
        color1, color2 = colors
        self.p1 = Player(mode1, color1)
        self.p2 = Player(mode2, color2)
        self.curr_player = self.p1 if self.p1.color == 'white' else self.p2

    def change_player(self):
        self.curr_player = self.p1 if self.curr_player == self.p2 else self.p2

    def make_selection(self, clicked_cell):
        self.board.select_cells(clicked_cell)
        self.show_info('Selected', clicked_cell)

    def make_move(self, clicked_cell):
        path = self.board.choose_path(clicked_cell)
        if not path:
            return
        start, end = self.board.selected_cell, clicked_cell
        self.curr_player.move_checker(start, path)
        self.curr_player.update_coords(start, end)
        self.curr_player.check_win()
        self.board.update_cells(end)
        self.board.clean()
        self.change_player()
        self.show_info('Destination', end)

    def click(self, event):
        i = event.x // cell_size
        j = event.y // cell_size
        clicked_cell = self.board.field[i][j]

        if clicked_cell.color == self.curr_player.color:
            self.make_selection(clicked_cell)

        elif self.board.paths:
            self.make_move(clicked_cell)

    @staticmethod
    def show_info(name, cell):
        print('{name} x={x}, y={y}'.format(
            name = name,
            x = cell.x,
            y = cell.y,
        ))


def main():
    gm = GameManager()
    gm.create_board()
    gm.create_players('man', 'man')
    gm.fill_board()

    while True:
        if gm.curr_player.mode == 'man':
            canv.bind("<Button-1>", gm.click)
        else:
            canv.bind("<Button-1>", gm.click)

        canv.update()
        time.sleep(0.03)


if __name__ == '__main__':
    main()
