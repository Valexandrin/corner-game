# "Corners" game (Игра "Уголки")

## Rules

Player who finished moving his checkers to opposite corner is winner.

## Algorithm for choosing best move ("bot" mode)

- Find farest empty cell (FEC) within "winner cells".
- Find all avaliable checkers for making a move.
- Choose checker for move:
  - Check if any checker can occupate FEC.
  - Count distance up to FEC for all avaliable checkers. Count an average.
  - Prioritize by a target ("far checkers" q-ty relative to all checkers q-ty).
  - Calculate "the best" path based on a distance up to FEC for each cell in path for chosen checkers.
- Make a move

## Images

![Alt-текст](https://github.com/Valexandrin/corner-game/blob/main/game/images/game_view.png?raw=true)

## Project structure

For running on localhost:

```bash
git clone https://github.com/Valexandrin/corner-game
```

## Start up

### One-time action (if not poetry)

```bash
pip install poetry
poetry config virtualenvs.in-project true
source .env\Scripts\activate
```

### Install dependecies

```bash
poetry init
poetry install
```

### Configure

Change configurations in game/config.py

## Usage

```bash
make run
```
