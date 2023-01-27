# "Corners" game (Игра "Уголки")

## Rules

Player who finished moving his checkers to opposite corner is winner.

## Algorithm for choosing best move ("bot" mode)

- Find all possible paths for all checkers which can make a move.
- Find farest empty cell (FEC) within "winner cells".
- Count distance up to FEC for all avaliable checkers. Count an average.
- Calculate parts (relative to the average) sizes.
- Prioritize parts by using a target (part size relative to q-ty of avaliable checkers).
- Choose checker for move:
  - Most behind in prioritized checkers.
  - Checker with longest (most productive) path. Before find "the best" path by calculation a distance up to FEC for each cell in path.

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
