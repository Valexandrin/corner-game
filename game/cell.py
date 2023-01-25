from game.app import canv
from game.config import config

cell_size = config.cell_size


class Cell:
    def __init__(self, x, y):
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

    def select(self, color):
        canv.itemconfig(self.id, outline=color, width=3)

    def released(self):
        canv.itemconfig(self.id, outline="black", width=1)

    def clean(self):
        self.color = self.checker_id = None
