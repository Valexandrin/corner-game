import time
from game.gm import GameManager
from game.app import canv


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
