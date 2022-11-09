#!/usr/bin/env python3

import os
from random import choice

from shutil import get_terminal_size
from time import sleep

max_cols, max_rows = get_terminal_size()
CLEAR_COMMAND = 'clear' if os.name == 'posix' else 'cls'

'''
The current probability of spawning a living cell is 0.5.
If you change the variables ALIVE or DEAD, then the probability will change
'''

ALIVE = '#'
DEAD = ' '

grid = [[choice(DEAD + ALIVE) for _ in range(max_cols)] for _ in range(max_rows)]


def show_grid():
    os.system(CLEAR_COMMAND)
    for g in grid:
        print(''.join(g))


def get_indexes(index, max_value):
    return [(index + i) % max_value for i in range(-1, 2)]


def get_neighbours_rows(index):
    row_indexes = get_indexes(index, max_rows)
    return [grid[row_index] for row_index in row_indexes]


def get_neighbours_cols(index, rows):
    col_indexes = get_indexes(index, max_cols)
    return [[row[col_index] for col_index in col_indexes] for row in rows]


def alive_counter(neighbours: list[list[str]]):
    summa = 0
    for row in neighbours:
        summa += row.count(ALIVE)
    return summa


def still_alive(neighbours: list[list[str]]):
    alive_count = alive_counter(neighbours) - 1
    return alive_count in (2, 3)


def can_respawn(neighbours):
    alive_count = alive_counter(neighbours)
    return alive_count == 3


def cell_value(neighbours):
    if neighbours[1][1] == ALIVE:
        return ALIVE if still_alive(neighbours) else DEAD
    return ALIVE if can_respawn(neighbours) else DEAD


def update_grid():
    result = []
    for row_index, row in enumerate(grid):
        buffer = []
        rows = get_neighbours_rows(row_index)
        for col_index, col in enumerate(row):
            neighbours = get_neighbours_cols(col_index, rows)
            buffer.append(cell_value(neighbours))
        result.append(buffer)
    return result


def main():
    global grid
    while True:
        show_grid()
        grid = update_grid()
        sleep(0.1)


if __name__ == '__main__':
    main()
