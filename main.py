import heapq
import pprint
import random
from copy import deepcopy

from sudoku import from_file, calc_fitness, fill_with_unique_blks as fill
from utils import Counter


PATH = './sudoku.txt'
MAX_ITERATIONS = 100000
ONLOOKER_BEES = 300
EMPLOYED_BEES = 100
SCOUT_BEES = EMPLOYED_BEES // 5
FERTILITY = 30


counter = Counter()


def find_neighbor_solution(board, start_squares):
    new_board = deepcopy(board)
    blk = random.randint(0, 8)
    x = (blk // 3) * 3
    y = (blk % 3) * 3
    available = [(i, j)
                 for i in range(x, x+3)
                 for j in range(y, y+3)
                 if (i, j) not in start_squares]
    a, b = random.choice(available)
    available.remove((a, b))
    c, d = random.choice(available)
    new_board[a][b], new_board[c][d] = new_board[c][d], new_board[a][b]
    return new_board


def search_neighborhood(sol, start_squares, workers):
    best_sol, best_fitness = sol, calc_fitness(sol)
    for _ in range(workers):
        sol = find_neighbor_solution(sol, start_squares)
        fitness = calc_fitness(sol)
        if fitness < best_fitness:
            best_sol = sol
            best_fitness = fitness
    return best_fitness, best_sol


def random_search(start_board, sites_to_search, solutions):
    for _ in range(sites_to_search):
        sol = deepcopy(start_board)
        fill(sol)
        heapq.heappush(solutions, (calc_fitness(sol), counter.next(),
                                   FERTILITY, sol))


def prob(fitness):
    return 1 / (1 + fitness)


def forage(start_board, start_squares):

    iteration = 0
    solutions = []
    random_search(start_board, EMPLOYED_BEES, solutions)
    best_fitness, _, _, best_sol = heapq.nsmallest(1, solutions)[0]

    while iteration < MAX_ITERATIONS and best_fitness != 0:
        iteration += 1

        new_solutions = []
        scout_bees = SCOUT_BEES
        factor = ONLOOKER_BEES / sum(prob(item[0]) for item in solutions)
        for fitness, _, fertility, sol in solutions:
            worker_bees = int(factor * prob(fitness))
            new_fitness, new_sol = search_neighborhood(sol, start_squares,
                                                       worker_bees)
            if new_sol == sol:
                fertility -= 1
                if fertility == 0:
                    scout_bees += 1
                else:
                    heapq.heappush(new_solutions, (new_fitness, counter.next(),
                                                   fertility, new_sol))
            else:
                heapq.heappush(new_solutions, (new_fitness, counter.next(),
                                               FERTILITY, new_sol))

        random_search(start_board, scout_bees, new_solutions)
        solutions = heapq.nsmallest(EMPLOYED_BEES, new_solutions)
        heapq.heapify(solutions)

        best_new_fitness, _, _, best_new_sol = heapq.nsmallest(1, solutions)[0]
        if best_new_fitness < best_fitness:
            print(best_new_fitness)
            best_fitness, best_sol = best_new_fitness, best_new_sol

    return best_fitness, best_sol


def main():
    final_fitness, final_result = forage(*from_file(PATH))
    print('Fitness: ', final_fitness)
    pprint.pprint(final_result)


if __name__ == "__main__":
    main()
