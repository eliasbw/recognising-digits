import numpy as np
from typing import List, Union
from numba import njit
from data import *

BITS = 160
PATTERNS = 5



def flatten(pattern: Union[List[List[int]], List[List[List[int]]]]):
    # Function to flatten a list of lists, or
    # a list of (list of lists)

    if len(np.shape(pattern)) == 1:
        return pattern

    flattened_lists = []

    for element in pattern:
        # Decide whether list of lists / list of (lists of list)

        if type(element[0]) != list:
            return [bit for element in pattern for bit in element]

        _temp = []
        for bit in element:
            _temp += bit

        flattened_lists += [_temp]
    return flattened_lists


def dot_product_without_index(digits, distorted, digit, removed_index):
    dot_product_except_index = sum(
        [
            bit_1 * bit_2 for index, (bit_1, bit_2) in enumerate(zip(digits[digit], distorted)) if index != removed_index
        ]
    )
    return digits[digit][removed_index] * dot_product_except_index / BITS


def matcher(distorted):

    count = {k: 0 for k in range(0, 2 * len(DIGITS) + 1)}

    for px, pattern in enumerate(DIGITS):
        if pattern == distorted:
            count[px] += 1
            break
        if pattern == [-ix for ix in distorted]:
            count[5 + px] += 1
    else:
        count[2 * len(DIGITS)] += 1

    return [(k, v) for k, v in count.items()]


def to_matrix(pattern):
    pattern = np.reshape(pattern, (16, 10))
    matrix = "[["
    for rx, row in enumerate(pattern):

        matrix += ", ".join([str(ix) for ix in row])
        if rx != 15:
            matrix += "],["
        else:
            matrix += "]]"
    return matrix


def train(distorted_pattern: List):
    DIGITS = [flatten(pattern=digit) for digit in [ZERO, ONE, TWO, THREE, FOUR]]
    distorted_pattern = flatten(distorted_pattern)
    iterate = True
    iteration_nr = 0

    while iterate:
        iterate = False
        iteration_nr += 1

        for bit in range(BITS):
            previous_pattern = distorted_pattern.copy()
            distorted_pattern[bit] = 0

            for dx, digit in enumerate(DIGITS):
                distorted_pattern[bit] += dot_product_without_index(DIGITS, previous_pattern, dx, bit)

            distorted_pattern[bit] = 1 if distorted_pattern[bit] >= 0 else -1

            if distorted_pattern[bit] != previous_pattern[bit]:
                iterate = True

    return np.reshape(distorted_pattern, (16, 10), "A")

