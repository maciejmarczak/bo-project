import random


def from_file(path):
    start_squares = set()
    start_board = [[None] * 9 for _ in range(9)]
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line.split()):
                if char.isdigit():
                    start_squares.add((i, j))
                    start_board[i][j] = int(char)
    return start_board, start_squares


def free_digits(taken_digits):
    leftover_digits = [digit for digit in range(1, 10)
                       if digit not in taken_digits]
    random.shuffle(leftover_digits)
    yield from leftover_digits


def fill_with_unique_blks(board):
    for blk in range(9):
        x = (blk // 3) * 3
        y = (blk % 3) * 3
        taken_digits = [board[row][col]
                        for row in range(x, x+3)
                        for col in range(y, y+3)
                        if board[row][col]]
        digits = free_digits(taken_digits)
        for row in range(x, x+3):
            for col in range(y, y+3):
                if not board[row][col]:
                    board[row][col] = next(digits)


def count_digits_repetition_num(it):
    digits = [-1] * 10
    for digit in it:
        digits[digit] += 1
    return sum(digit_num for digit_num in digits if digit_num > 0)


def calc_penalty(board):
    penalty = 0
    for i in range(9):
        row = board[i]
        col = (board[j][i] for j in range(9))
        for it in (row, col):
            penalty += count_digits_repetition_num(it)
    return penalty


def calc_fitness(board):
    return 1 / (1 + calc_penalty(board))
