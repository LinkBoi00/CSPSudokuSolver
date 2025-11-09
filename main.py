import config
import sudoku_CSP
import sudoku_problem
import search
import time
import sys

# Import global configuration
from config import GRID_SIZE, SUBGRID_SIZE

# 4x4 Sudoku puzzles (0 represents empty cells)
easy_sudoku_state = [[1, 0, 0, 2],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [2, 0, 0, 1]]

medium_sudoku_state = [[0, 0, 0, 2],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0],
                       [2, 0, 0, 0]]

hard_sudoku_state = [[0, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]

# Custom 4x4 sudoky puzzle
custom_sudoku_state = [[0, 0, 0, 0],
                       [0, 0, 0, 3],
                       [0, 0, 3, 0],
                       [0, 3, 0, 0]]

def parse_sudoku(sudoku_str):
    """
    Parses a string into a representation of a sudoku state as a GRID_SIZE x GRID_SIZE list of integers.

    Keyword arguments:
    str -- a string consisting of GRID_SIZE^2 integers between 0 and GRID_SIZE representing the values of the entries of a sudoku.
    """
    sudoku = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    counter = 0
    total_cells = GRID_SIZE * GRID_SIZE
    
    for char in sudoku_str:
        if counter >= total_cells:
            break

        try:
            val = int(char)
            row = counter // GRID_SIZE
            col = counter % GRID_SIZE
            sudoku[row][col] = val
            counter += 1
        except ValueError:
            continue

    if counter < total_cells - 1:
        raise ValueError("Not enough integer values in sudoku string input.")
    else:
        return sudoku


def print_initial_and_solution(init_state, sol_state):
    """
    Prints the given initial and solution state of a sudoku side by side.

    Keyword arguments:
    init_state -- a GRID_SIZE x GRID_SIZE list of lists of integers representing the starting state of the solution
    sol_state -- a GRID_SIZE x GRID_SIZE list of lists of integers representing the solution state of the solution
    """
    output_string = "\nInitial state:       Solution state:\n"
    for row in range(GRID_SIZE):
        for init_col in range(GRID_SIZE):
            output_string += str(init_state[row][init_col]) + " "

        output_string += " " * 5

        for sol_col in range(GRID_SIZE):
            output_string += str(sol_state[row][sol_col]) + " "

        output_string += "\n"

    print(output_string)


def main():
    """
    Runs the sudoku solver using the given command line arguments as input.

    The command line syntax is as follows:

        $ python main.py

    Adding the --help or --h tag to the command line arguments shows a
    help page for how to initialize this program:

        $python main.py --h

    You can add the -sudoku or -s argument followed by easy, medium,
    hard, or a the name of a .txt file in the same directory
    to specify a sudoku to solve. The default sudoku is easy.

        $ python main.py -sudoku medium
        $ python main.py -s sudoku.txt

    The easy, medium, and hard keywords correspond to 3 different built in 
    sudokus of varying difficulty that can be used to solve (size depends on GRID_SIZE).

    If you use the file input option then the program will use the first GRID_SIZE^2
    digits it finds in the .txt file as the values for the sudoku.

    In order to choose which next variable heuristic to use, the -next_var
    or -nv tag can be added followed by either trivial, or mrv which
    correspond to the trivial and minimum remaining values heuristics.
    The default heuristic is the MRV heuristic.

        $ python main.py -next_var mrv
        $ python main.py -nv trivial"""
    sudoku_state = easy_sudoku_state
    next_var = search.mrv_next_var_heuristic
    sudoku_dict = {"easy": easy_sudoku_state,
                   "medium": medium_sudoku_state,
                   "hard": hard_sudoku_state,
                   "custom": custom_sudoku_state}
    next_var_dict = {"trivial": search.trivial_next_var_heuristic,
                     "mrv": search.mrv_next_var_heuristic}

    for i, arg in enumerate(sys.argv):
        if arg == "--help" or arg == "--h":
            print("\n" + "-" * 75),
            print(main.__doc__)
            print("-" * 75 + "\n")
            sys.exit(0)
        if arg == "-sudoku" or arg == "-s":
            if sys.argv[i + 1] in sudoku_dict:
                sudoku_state = sudoku_dict[sys.argv[i + 1]]
            else:
                try:
                    sudoku_file = open(sys.argv[i + 1], "r")
                    sudoku_state = parse_sudoku(sudoku_file.read())
                except FileNotFoundError:
                    raise ValueError("Given argument for sudoku input \"-s\" is invalid.")
        if arg == "-next_var" or arg == "-nv":
            if sys.argv[i + 1] in next_var_dict:
                next_var = next_var_dict[sys.argv[i + 1]]
            else:
                ValueError("Given argument for next_var input \"-nv\" is invalid.")

    initial_sudoku = sudoku_problem.Sudoku(sudoku_state)
    csp = sudoku_CSP.SudokuCSP(initial_sudoku, next_var_heuristic=next_var)

    start = time.time()
    solution = search.backtracking_search(csp)
    end = time.time()

    print_initial_and_solution(sudoku_state, solution.get_state())

    print("Time elapsed: " + str(end - start) + " seconds.")
    print("Number of nodes expanded: " + str(csp.get_num_expanded()) + "\n")


if __name__ == "__main__":
    main()