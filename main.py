import math
import pprint
import random
from copy import deepcopy
from operator import attrgetter
from collections import namedtuple
from itertools import chain

from sudoku import from_file, calc_fitness, fill_with_unique_blks as fill


PATH = './puzzles/sudoku_easy.txt'
MAX_ITERATIONS = 1000
EMPLOYED_BEES = 100
ONLOOKER_BEES = 200
SCOUT_BEES = EMPLOYED_BEES // 10
SEARCHED_FITNESS = 1


Solution = namedtuple("Solution", ["fitness", "board"])


def search_neighborhood(sol, solutions, start_squares):
    new_board = deepcopy(sol.board)
    neighbor_sol = sol
    while neighbor_sol is sol:
        neighbor_sol = random.choice(solutions)

    blk = random.randint(0, 8)
    x, y = (blk // 3) * 3, (blk % 3) * 3
    blk_squares = [(i, j) for i in range(x, x+3) for j in range(y, y+3)]
    taken = [idx for idx in blk_squares if idx in start_squares]
    available = [idx for idx in blk_squares if idx not in taken]

    a, b = random.choice(available)
    val = sol.board[a][b]
    new_val = math.ceil(val + random.random() * random.choice([1, -1]) * abs(val - neighbor_sol.board[a][b]))
    if new_val > 9:
        new_val = (new_val % 9) + 1
    elif new_val == val:
        return sol

    for i, j in blk_squares:
        if new_board[i][j] == new_val:
            if (i, j) not in taken:
                new_board[a][b], new_board[i][j] = new_board[i][j], new_board[a][b]
                break
            else:
                return sol

    new_sol = Solution(fitness=calc_fitness(new_board), board=new_board)
    return new_sol if new_sol.fitness > sol.fitness else sol


def search_neighborhoods(sol, solutions, start_squares, onlooker_bees):
    onlooker_solutions = (search_neighborhood(sol, solutions, start_squares)
                          for _ in range(onlooker_bees))
    return max(chain([sol], onlooker_solutions), key=attrgetter('fitness'))


def random_search(start_board):
    sol = deepcopy(start_board)
    fill(sol)
    return Solution(fitness=calc_fitness(sol), board=sol)


def forage(start_board, start_squares):

    iteration = 0
    #initialize population
    solutions = [random_search(start_board) for _ in range(EMPLOYED_BEES)]
    # evaluate population
    best_sol = max(solutions, key=attrgetter('fitness'))

    while iteration < MAX_ITERATIONS and best_sol.fitness != SEARCHED_FITNESS:
        iteration += 1
        # every employed bee search its neighborhood
        solutions = [search_neighborhood(sol, solutions, start_squares)
                     for sol in solutions]

        # every employed bee with onlooker bess search given neighborhood
        factor = ONLOOKER_BEES / sum(sol.fitness for sol in solutions)
        solutions = [search_neighborhoods(sol, solutions, start_squares,
                                          int(factor * sol.fitness))
                     for sol in solutions]

        # replace abandoned solutions if any
        solutions.sort(key=attrgetter('fitness'))
        for i in range(SCOUT_BEES):
            sol = solutions[i]
            new_sol = random_search(start_board)
            if new_sol.fitness > sol.fitness:
                solutions[i] = new_sol

        best_new_sol = max(solutions, key=attrgetter('fitness'))
        if best_new_sol.fitness > best_sol.fitness:
            print(best_new_sol.fitness)
            best_sol = best_new_sol

    return best_sol


def main():
    start_board, start_squares = from_file(PATH)
    final_result = forage(start_board, start_squares)
    print('Fitness: ', final_result.fitness)
    pprint.pprint(final_result.board)


if __name__ == "__main__":
    main()
