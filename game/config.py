title = "Уголки"
game_speed = 20

corner_size = [4, 3]

cell_size = 100
cells_number = 8
cell_imgs = {
    'white': "game/images/white.png",
    'black': "game/images/black.png",
}


class GameConfig:
    def __init__(self) -> None:
        self.title = title
        self.speed = game_speed
        self.cell_size = cell_size
        self.cells_number = cells_number
        self.side_size = cell_size * cells_number
        self.checker_views = cell_imgs
        self.corner_size = corner_size

config = GameConfig()
