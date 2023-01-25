import time
import tkinter as tk
from game.config import config
from game.app import canv

views = config.checker_views
cell_size = config.cell_size


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
