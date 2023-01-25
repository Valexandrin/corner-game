from game.checker import Checker


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
