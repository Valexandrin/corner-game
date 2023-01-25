cell_size = 100
cells_number = 8
limit = range(cells_number)
side_size = cell_size * cells_number
views = {
    'white': "game/images/white.png",
    'black': "game/images/black.png",
}
corner_size = [4, 3]


class GameConfig:
    def __init__(self) -> None:
        self.cell_size = cell_size
        self.cells_number = cells_number
        self.side_size = cell_size * cells_number
        self.checker_views = views
        self.corner_size = corner_size

config = GameConfig()
