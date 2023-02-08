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

city|tours|trip
:-:|:-:|:-:
![Alt-текст](https://github.com/gettrip/backend/blob/main/images/index.png?raw=true) | ![Alt-текст](https://github.com/gettrip/backend/blob/main/images/city_tour.png?raw=true) | ![Alt-текст](https://github.com/gettrip/backend/blob/main/images/trip.png?raw=true)

## Project structure

The service consists on two parts: backend and frontend. For running on localhost both need to be cloned:

```bash
git clone https://github.com/gettrip/backend.git
git clone https://github.com/gettrip/frontend.git
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

### Configure environment

Create .env file by using .env.default.

### Create database (backend)

```bash
make db.run
make db.create
```

## Usage

```bash
make run
```

## Resources used

```bash
PostgreSQL - database management system (DBMS)
psycopg2-binary - lib. Work with PostgreSQL (multi-threaded applications)
sqlalchemy - lib. Work with different DBMS
pydantic - lib. Data validation and settings management
```
