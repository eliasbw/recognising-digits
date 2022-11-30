"""
Takes a distorted pattern and uses Hopfield Network dynamics to iterate over
the bits in the pattern to converge to a local minima.
"""

import numpy as np
from numba import njit
from typing import List
from data_for_stored_patterns import ZERO, ONE, TWO, THREE, FOUR


def flatten(pattern: List | List[List]):
    """
    Flatten a list of list

    :param pattern: List
    :return:
    flattened_lists: np.ndarray
    Returns a numpy array of flattened lists
    """

    if len(np.shape(pattern)) == 1:
        return np.array(pattern)

    flattened_lists = []

    for element in pattern:
        # Decide whether list of lists / list of (lists of list)

        if type(element[0]) != list:
            return np.array([bit for element in pattern for bit in element])

        _temp = []
        for bit in element:
            _temp += bit

        flattened_lists += np.ndarray([_temp])
    return np.array(flattened_lists)


@njit
def dot_product_without_index(
    digit: np.ndarray, distorted_pattern: np.ndarray, removed_bit: int
):
    """
    Function to 'manually' compute the dot product except for a given bit -
    with a njit decorator to increase computational speed

    :param digit: List
        Bit-values for a given digit

    :param distorted_pattern: np.ndarray
        Bit-values for the distorted digit

    :param removed_bit: int
    The bit index to disregard

    :return:
    digit: List
    A list of the gradient to the weight vector
    """
    normalising_constant = len(digit)

    dot_product_except_index = sum(
        [
            bit_1 * bit_2
            for index, (bit_1, bit_2) in enumerate(zip(digit, distorted_pattern))
            if index != removed_bit
        ]
    )
    return digit[removed_bit] * dot_product_except_index / normalising_constant


def array_to_string_format(pattern: np.ndarray) -> str:
    """
    This function takes a input pattern and returns a string object that can
    easily be stored in the data folder

    :param pattern:
    The pattern to turn into a string object
    :return:
    matrix: str
    String object of an array that can easily be stored in data

    """
    pattern = np.reshape(pattern, (16, 10))
    matrix = "[["
    for rx, row in enumerate(pattern):

        matrix += ", ".join([str(ix) for ix in row])
        if rx != 15:
            matrix += "],["
        else:
            matrix += "]]"
    return matrix


def train(distorted_pattern: List) -> np.ndarray:
    """
    Train a Hopfield network to recognise a distorted pattern

    :param distorted_pattern: List
    List of bit values in the distorted pattern

    :return:
    distorted_pattern: np.ndarray
    The reshaped pattern after converging to a pattern

    """
    DIGITS = [flatten(pattern=digit) for digit in [ZERO, ONE, TWO, THREE, FOUR]]
    distorted_pattern = flatten(distorted_pattern)
    iterate = True
    iteration_nr = 0

    while iterate:
        iterate = False
        iteration_nr += 1

        for bit in range(len(distorted_pattern)):
            previous_pattern = distorted_pattern.copy()
            distorted_pattern[bit] = 0

            for dx, digit in enumerate(DIGITS):
                distorted_pattern[bit] += dot_product_without_index(
                    DIGITS[dx], previous_pattern, bit
                )

            distorted_pattern[bit] = 1 if distorted_pattern[bit] >= 0 else -1

            if distorted_pattern[bit] != previous_pattern[bit]:
                iterate = True

    return np.reshape(distorted_pattern, (16, 10), "A")
