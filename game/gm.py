from random import shuffle
from game.config import config
from game.board import Board
from game.player import Player

cells_number = config.cells_number
cell_size = config.cell_size
corner_size = config.corner_size
views = config.checker_views


class GameManager:
    def __init__(self):
        self.curr_player = None

    def create_board(self):
        self.board = Board(cells_number, corner_size)

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
