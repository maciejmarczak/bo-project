import pprint
import random
from copy import deepcopy
from operator import attrgetter
from collections import namedtuple

from sudoku import from_file, calc_fitness, fill_with_unique_blks as fill


PATH = './puzzles/sudoku_easy.txt'
MAX_ITERATIONS = 100000
EMPLOYED_BEES = 100
ONLOOKER_BEES = 200
SCOUT_BEES = EMPLOYED_BEES // 10
SEARCHED_FITNESS = 1


Solution = namedtuple("Solution", ["fitness", "board"])


def search_neighborhood(sol, solutions, start_squares):
    fitness = calc_fitness(sol)
    neighbor_sol = sol
    while neighbor_sol is sol:
        neighbor_sol = random.choice(solutions)[3]

    new_sol = deepcopy(sol)
    blk = random.randint(0, 8)
    x = (blk // 3) * 3
    y = (blk % 3) * 3
    blk_squares = [(i, j) for i in range(x, x+3) for j in range(y, y+3)]
    taken = [idx for idx in blk_squares if idx in start_squares]
    available = [idx for idx in blk_squares if idx not in taken]

    a, b = random.choice(available)
    val = sol[a][b]
    new_val = round(val + random.random() * (val - neighbor_sol[a][b]))
    if new_val > 9:
        new_val %= 9
    elif new_val < 0:
        new_val *= -1
    elif new_val in (0, val):
        return Solution(fitness, sol)

    for i, j in blk_squares:
        if new_sol[i][j] == new_val:
            if (i, j) not in taken:
                new_sol[a][b], new_sol[i][j] = new_sol[i][j], new_sol[a][b]
                break
            else:
                return Solution(fitness, sol)

    new_fitness = calc_fitness(new_sol)
    return Solution(new_fitness, new_sol) if new_fitness > fitness else Solution(fitness, sol)


def search_neighborhoods(sol, solutions, start_squares, onlooker_bees):
    best_sol, best_fitness = sol, calc_fitness(sol)
    for _ in range(onlooker_bees):
        new_fitness, new_sol = search_neighborhood(sol, solutions,
                                                   start_squares)
        if new_fitness > best_fitness:
            best_sol = new_sol
            best_fitness = new_fitness
    return Solution(best_fitness, best_sol)


def random_search(start_board):
    sol = deepcopy(start_board)
    fill(sol)
    return Solution(fitness=calc_fitness(sol), board=sol)


def forage(start_board, start_squares):

    iteration = 0
    solutions = [random_search(start_board) for _ in EMPLOYED_BEES]
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
