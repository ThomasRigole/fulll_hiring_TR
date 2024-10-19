#!/usr/bin/env python
# coding: utf-8

"""
#==============================#
| FizzBuzz - Fulll hiring test |
#==============================#
> Thomas Rigole
---------------
"""


def fizzbuzz_generator(n, fizzbuzz_map):
    """
    Generates sequences of values/FizzBuzz
    based on a custom ruleset: fizzbuzz_map.

    Parameters
    ----------
    n : int
        Upper bound of the FizzBuzz algorithm
    fizzbuzz_map : dict
        Ruleset composed of divisor(s) and associated word(s)

    Yields
    ------
    str
        The number itself or the FizzBuzz translation
    """
    for i in range(1, n + 1):
        sequence = ''.join([word for divisor, word in fizzbuzz_map.items()
                           if i % divisor == 0])
        yield sequence or str(i)


def main():
    # Input N
    try:
        n = int(input("Enter the upper bound N: "))
        if n <= 0:
            raise ValueError("The number must be positive")
    except ValueError as e:
        print(f"Invalid input format: {e}. Please enter a positive integer.")
        return   # Exit if error (invalid format)

    # FizzBuzz ruleset
    fizzbuzz_map = {3: 'Fizz', 5: 'Buzz'}

    # Sequence generation
    for sequence in fizzbuzz_generator(n, fizzbuzz_map):
        print(sequence)


if __name__ == "__main__":
    main()
