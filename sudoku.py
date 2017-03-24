from utils import free_digits, count_digits_repetition_num


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


def fill_with_unique_rows(board):
    for row in range(9):
        digits = free_digits(digit for digit in board[row] if digit)
        for col in range(9):
            if not row[col]:
                row[col] = next(digits)


def fill_with_unique_cols(board):
    for col in range(9):
        digits = free_digits(board[row][col]
                             for row in range(9)
                             if board[row][col])
        for row in range(9):
            if not board[row][col]:
                board[row][col] = next(digits)


def fill_with_unique_blks(board):
    for blk in range(9):
        x = (blk // 3) * 3
        y = (blk % 3) * 3
        digits = free_digits(board[row][col]
                             for row in range(x, x+3)
                             for col in range(y, y+3)
                             if board[row][col])
        for row in range(x, x+3):
            for col in range(y, y+3):
                if not board[row][col]:
                    board[row][col] = next(digits)


def calc_fitness(board):
    fitness = 0
    for i in range(9):
        row = board[i]
        col = (board[j][i] for j in range(9))

        x, y = (i // 3) * 3, (i % 3) * 3
        blk = (board[j][k] for j in range(x, x+3) for k in range(y, y+3))

        for it in (row, col, blk):
            fitness += count_digits_repetition_num(it)
    return fitness
