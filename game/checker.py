import time
import tkinter as tk

from game.app import canv
from game.config import config

views = config.checker_views
cell_size = config.cell_size
speed = config.speed


class Checker:
    def __init__(self, x: int, y: int, color: str='white'):
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

        shot = 1 / speed
        for i in range(speed+1):
            canv.coords(
                self.id,
                (old_x + step_x * i * shot) * cell_size,
                (old_y + step_y * i * shot) * cell_size,
            )
            canv.update()
            time.sleep(0.01)
