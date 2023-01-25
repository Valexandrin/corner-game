import tkinter as tk
from game.config import config

side_size = config.side_size

def create_canv():
    root = tk.Tk()
    root.title()
    root.resizable(0, 0)
    canv = tk.Canvas(
        root,
        width=side_size,
        height=side_size,
        highlightthickness = 0,
    )
    canv.pack()
    return canv

canv = create_canv()
