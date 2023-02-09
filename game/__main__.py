import time
from game.gm import GameManager
from game.app import canv
from game.bot import Bot

def main():
    mode1 = 'bot'
    mode2 = 'bot'

    gm = GameManager()
    gm.create_board()
    gm.create_players(mode1, mode2)
    gm.fill_board()

    if 'bot' in [mode1, mode2]:
        bot = Bot(gm)

    while not gm.win_status:
        if gm.curr_player.mode == 'man':
            canv.bind("<Button-1>", gm.click)
        else:
            bot.make_move()

        canv.update()
        time.sleep(0.03)


if __name__ == '__main__':
    main()
