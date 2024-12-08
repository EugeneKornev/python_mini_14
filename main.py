import numpy as np
from time import perf_counter
import re
import matplotlib.pyplot as plt
from ptable import format_table

# boards = ["Cross.txt", "Snark loop.txt", "4x Snark loop.txt"]
boards = ['4x Snark loop.txt']


def numpy_neighbors(board: np.ndarray, x: int, y: int) -> int:
    k = 0
    for i in range(max(x - 1, 0), min(x + 2, board.shape[0])):
        for j in range(max(y - 1, 0), min(y + 2, board.shape[1])):
            if i == x and j == y:
                continue
            if board[i, j]:
                k += 1
    return k


def numpy_step(board: np.ndarray) -> np.ndarray:
    tmp = np.zeros_like(board, dtype=bool)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            k = numpy_neighbors(board, i, j)
            if board[i, j]:
                match k:
                    case 2 | 3:
                        tmp[i, j] = True
                    case _:
                        tmp[i, j] = False
            else:
                match k:
                    case 3:
                        tmp[i, j] = True
                    case _:
                        tmp[i, j] = False
    return tmp


def numpy_game(board: np.ndarray, steps: int) -> np.ndarray:
    for i in range(steps):
        board = numpy_step(board)
    return board


def list_neighbors(board: list, x: int, y: int) -> int:
    k = 0
    for i in range(max(x - 1, 0), min(x + 2, len(board))):
        for j in range(max(y - 1, 0), min(y + 2, len(board[0]))):
            if i == x and j == y:
                continue
            if board[i][j]:
                k += 1
    return k


def list_step(board: list) -> list:
    tmp = [row[:] for row in board]
    for i in range(len(board)):
        for j in range(len(board[0])):
            k = list_neighbors(board, i, j)
            if board[i][j]:
                match k:
                    case 2 | 3:
                        tmp[i][j] = True
                    case _:
                        tmp[i][j] = False
            else:
                match k:
                    case 3:
                        tmp[i][j] = True
                    case _:
                        tmp[i][j] = False
    return tmp


def list_game(board: list, steps: int) -> list:
    for i in range(steps):
        board = list_step(board)
    return board


def get_board(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as file:
        first_row = file.readline().rstrip('\n').split(",")
        x, y, *z = map(lambda k: re.match(pattern=r".*?(\d+).*?", string=k).groups()[0], first_row)
        x, y = int(x), int(y)
        board = [[False for _ in range(x)] for _ in range(y)]
        data = file.read()
        i = 0
        r, c = 0, 0
        j = -1
        while True:
            if data[i] == "!":
                break
            elif data[i] == "$":
                c = 0
                i += 1
                if j > 0:
                    k = 0
                    while k < j:
                        r += 1
                        k += 1
                    j = -1
                else:
                    r += 1
            elif data[i].isdigit():
                j = int(data[i])
                i += 1
                while data[i].isdigit():
                    j = 10 * j + int(data[i])
                    i += 1
            elif data[i] == 'o':
                if j > 0:
                    k = 0
                    while k < j:
                        board[r][c] = True
                        c += 1
                        k += 1
                    j = -1
                else:
                    board[r][c] = True
                    c += 1
                i += 1
            elif data[i] == 'b':
                if j > 0:
                    c += j
                    j = -1
                else:
                    c += 1
                i += 1
            elif data[i] == "\n":
                i += 1
            else:
                print("Error: ", data[i])
    return board


def compare(board: list, steps: int) -> (float, float):
    board_for_list = board.copy()
    board_for_numpy = np.array(board, dtype=bool)
    list_start = perf_counter()
    list_game(board_for_list, steps)
    list_end = perf_counter()
    numpy_start = perf_counter()
    numpy_game(board_for_numpy, steps)
    numpy_end = perf_counter()
    return list_end - list_start, numpy_end - numpy_start


def main():
    TESTS_COUNT = 10
    STEPS = 128
    for filename in boards:
        board = get_board(filename)
        benchmarks = [f"Attempt №{i}" for i in range(TESTS_COUNT)]
        algos = ["List", "Numpy"]
        results = []
        for i in range(TESTS_COUNT):
            results.append(compare(board, STEPS))
        print(format_table(benchmarks, algos, results))
        print()
        result = numpy_game(np.array(board, dtype=bool), STEPS)
        plt.imshow(result, cmap="gray_r", interpolation="nearest")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    main()

