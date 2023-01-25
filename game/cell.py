from game.app import canv
from game.config import config

cell_size = config.cell_size


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = None
        self.checker_id = None
        self.id = canv.create_rectangle(
            (
                x * cell_size,
                y * cell_size,
                (x + 1) * cell_size,
                (y + 1) * cell_size,
            ),
            fill = "#FFD39B",
        )

    def change_view(self, color: str="black", width: int=1):
        canv.itemconfig(self.id, outline=color, width=width)

    def select(self, color: str="yellow"):
        self.change_view(color, width=3)

    def released(self):
        self.change_view("black", width=1)

    def clean(self):
        self.color = self.checker_id = None
