#!/usr/bin/env python
# coding: utf-8

"""
#==============================#
| FizzBuzz - Fulll hiring test |
#==============================#
> Thomas Rigole
---------------
> Advanced version :
Choice of custom & scalable rules, via command-line argument parser.
If required on a larger scale, use a ruleset
JSON file to create the fizzbuzz_map dict.
"""

# Imports --------------------------------------------------------------------
import argparse


# Functions ------------------------------------------------------------------
def parse_arguments():
    """
    Parse command-line arguments : upper bound 'n' of the FizzBuzz program
    and optional custom rules.

    Returns
    -------
    Namespace
        Parsed arguments : upper bound n (+ ruleset)
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Custom FizzBuzz program"
    )

    # Positional argument for upper bound n
    parser.add_argument('n', type=int, help="FizzBuzz sequence upper bound")
    # Optional arguement for custom rules
    parser.add_argument('--rules', type=str, nargs='+',
                        help="FizzBuzz custom rules as 'divisor:word' \
                             (e.g., 3:Fizz 5:Buzz).")

    return parser.parse_args()


def format_rules(rules_string):
    """
    Convert the custom rules string to a dictionary.

    Parameters
    ----------
    rules_string : str
        Rule(s) passed as 'divisor:word'

    Returns
    -------
    rules_dict : dict
    """
    try:
        return {int(divisor): word for divisor, word
                in (rule.split(':') for rule in rules_string)}
    except ValueError:
        print("Invalid custom rules format. Please enter a valid ruleset:\n \
            > 'divisor:word' (e.g., --rules 3:Fizz 5:Buzz)")
        return False


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


# main -----------------------------------------------------------------------
def main():
    args = parse_arguments()
    if args.rules:
        fizzbuzz_map = format_rules(args.rules)
        if not fizzbuzz_map:
            return  # Exit if error (custom rules format)
    else:
        fizzbuzz_map = {3: 'Fizz', 5: 'Buzz'}

    for sequence in fizzbuzz_generator(args.n, fizzbuzz_map):
        print(sequence)


if __name__ == "__main__":
    main()
