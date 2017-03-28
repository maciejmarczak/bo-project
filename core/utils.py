import random


def free_digits(taken_digits):
    leftover_digits = [digit for digit in range(1, 10)
                       if digit not in taken_digits]
    random.shuffle(leftover_digits)
    yield from leftover_digits


def count_digits_repetition_num(it):
    digits = [-1] * 10
    for digit in it:
        digits[digit] += 1
    return sum(digit_num for digit_num in digits if digit_num > 0)


class Counter:
    def __init__(self, num=0):
        self.num = num

    def next(self):
        self.num += 1
        return self.num - 1
