from itertools import product
from time import perf_counter

from core.abc import forage
from core.sudoku_utils import from_file


LOG_FILE = './perf.log'
BOARDS = ('../examples/sudoku_easy.txt',
          '../examples/sudoku_medium.txt',
          '../examples/sudoku_hard.txt',
          '../examples/sudoku.txt')

TRIES_NUM = 50
ITERATIONS = (10, 50, 100, 200, 300, 500, 1000, 10000)
EMPLOYED_BEES = (10, 20, 30, 50, 70, 100, 200)
ONLOOKER_BEES = (10, 20, 40, 60, 80, 100, 300)
SCOUT_BEES = (2, 3, 5, 10, 20, 30, 50)


def compute(f, board, squares, it_num, eb, ob, sb):
    log = '{it_max};{eb};{ob};{sb};{{fit}};{{iteration}};' \
          '{{time}}\n'.format(it_max=it_num, eb=eb, ob=ob, sb=sb)
    gen = forage(board, squares, max_iterations=it_num,
                 employed_bees=eb, onlooker_bees=ob,
                 scout_bees=sb, yield_after=it_num + 1)

    start = perf_counter()
    try:
        next(gen)
    except StopIteration as ex:
        end = perf_counter()
        sol, iteration = ex.value
        f.write(log.format(fit=sol.fitness, iteration=iteration,
                           time=end-start))


def main():
    for board in BOARDS:
        with open(LOG_FILE, 'w+') as f:
            f.write(board + '\n\n')
            start_board, start_squares = from_file(board)
            for it_num, eb, ob, sb in product(ITERATIONS, EMPLOYED_BEES,
                                              ONLOOKER_BEES, SCOUT_BEES):
                if sb < eb:
                    for i in range(TRIES_NUM):
                        f.write('{};'.format(i))
                        compute(f, start_board, start_squares,
                                it_num, eb, ob, sb)
                    f.write('\n')


if __name__ == "__main__":
    main()
