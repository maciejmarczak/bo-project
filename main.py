import heapq
import pprint
import random
from copy import deepcopy


class Counter:
    def __init__(self, num=0):
        self.num = num

    def next(self):
        self.num += 1
        return self.num - 1

counter = Counter()


def read_sud(path):
    start_squares = set()
    sudoku = [[None] * 9 for _ in range(9)]
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line.split()):
                if char.isdigit():
                    start_squares.add((i, j))
                    sudoku[i][j] = int(char)
    return sudoku, start_squares


def free_digits(x, y, sudoku):
    start_digits = tuple(sudoku[i][j]
                         for i in range(x, x+3)
                         for j in range(y, y+3)
                         if sudoku[i][j])
    leftover_digits = [digit for digit in range(1, 10)
                       if digit not in start_digits]
    random.shuffle(leftover_digits)
    yield from leftover_digits


def fill_sud(start_board):
    sudoku = deepcopy(start_board)
    for blk in range(9):
        x = (blk // 3) * 3
        y = (blk % 3) * 3
        digits = free_digits(x, y, sudoku)
        for i in range(x, x+3):
            for j in range(y, y+3):
                if not sudoku[i][j]:
                    sudoku[i][j] = next(digits)
    return sudoku


def count_repetition(it):
    digits = [0] * 10
    for digit in it:
        digits[digit] += 1
    return sum(digit_num - 1 for digit_num in digits if digit_num > 1)


def calc_fitness(sudoku):
    fitness = 0
    for i in range(9):
        row = sudoku[i]
        col = (sudoku[j][i] for j in range(9))
        fitness += count_repetition(row) + count_repetition(col)
    return fitness


def find_neighbor_solution(sudoku, start_squares):
    new_sudoku = deepcopy(sudoku)
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
    new_sudoku[a][b], new_sudoku[c][d] = new_sudoku[c][d], new_sudoku[a][b]
    return new_sudoku


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
        sol = fill_sud(start_board)
        fitness = calc_fitness(sol)
        heapq.heappush(solutions, (fitness, counter.next(), sol))


def forage(start_board, start_squares, max_iterations,
           sites_to_visit, sites_to_select, bees):

    iteration = 0
    solutions = []
    scout_bees = sites_to_visit - sites_to_select
    random_search(start_board, sites_to_visit, solutions)
    best_fitness, _, best_sol = heapq.nsmallest(1, solutions)[0]

    while iteration < max_iterations and best_fitness != 0:
        best_solutions = heapq.nsmallest(sites_to_select, solutions)
        fitness_sum = sum(1 / (1 + item[0]) for item in best_solutions)

        solutions = []
        for fitness, _, sol in best_solutions:
            onlooker_bees = int(bees * (1 / (1 + fitness)) / fitness_sum)
            new_fitness, new_sol = search_neighborhood(sol, start_squares,
                                                       onlooker_bees)
            heapq.heappush(solutions, (new_fitness, counter.next(), new_sol))
        random_search(start_board, scout_bees, solutions)

        best_new_fitness, _, best_new_sol = heapq.nsmallest(1, solutions)[0]
        if best_new_fitness < best_fitness:
            print(best_new_fitness)
            best_fitness = best_new_fitness
            best_sol = best_new_sol

    return best_sol, best_fitness


def main(*, path):
    max_iterations = 300
    sites_to_visit = 100
    sites_to_select = 40
    bees = 1000
    start_board, start_squares = read_sud(path)
    result, fitness = forage(start_board, start_squares, max_iterations,
                             sites_to_visit, sites_to_select, bees)

    print('Success: ' if fitness == 0 else 'Failure(fitness=): '.format(fitness))
    pprint.pprint(result)


if __name__ == "__main__":
    main(path='./sudoku.txt')


# def main(path_name='./zad3/input2.txt',
#          temp=ann.gen_temp(10, 10e-2, 0.99999),
#          save=True, name='', display=True):
#
#     sud = [[['x', True] for _ in range(9)] for _ in range(9)]
#     read_sud(path_name, sud)
#     if display:
#         print_board(sud)
#         print("\n")
#
#     fill_sud(sud)
#     if display:
#         print_board(sud)
#         print("\nFirst solution cost: %d\n" % calc_cost(sud))
#
#     best_sol, best_cost, energy = ann.anneal(sud,
#                                              swap_digits,
#                                              calc_cost,
#                                              ann.acceptance_probability,
#                                              temp)
#     if display:
#         print_board(best_sol)
#         print("\nBest solution cost: %d\nIs sudoku solved: %s\n" %
#               (best_cost, best_cost == 0))
#
#     plt.plot(range(len(energy)), energy)
#     plt.xlabel('Iteration')
#     plt.ylabel('Cost')
#     if save:
#         plt.savefig('./zad3/' + name + '_s_' if best_cost == 0 else '_ns' + 'e')
#     if display:
#         plt.show()
#
#
# if __name__ == "__main__":
#     main()
