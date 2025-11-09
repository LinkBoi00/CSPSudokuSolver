# Import GRID_SIZE from sudoku_problem
from config import GRID_SIZE

class SudokuCSP:
    def __init__(self, initial_sudoku, next_var_heuristic):
        """
        Initializes an instance of a SudokuCSP.

        Keyword arguments:
        initial_sudoku -- an instance of a Sudoku object representing the initial state of the sudoku to be solved.
        next_var_heuristic -- an optional argument that is a function that takes in an instance of a Sudoku and
        returns the next node to be expanded. Default is lpv_next_var_heuristic.
        """
        self.initial_sudoku = initial_sudoku
        self.next_var_heuristic = next_var_heuristic
        self.expanded_nodes = 0

    def get_num_expanded(self):
        """
        Returns the number of nodes this CSP has expanded.
        """
        return self.expanded_nodes

    def get_initial_sudoku(self):
        """
        Gets the initial state of this sudoku csp problem.

        Returns the initial state by calling the get_state() method on the initial_sudoku of this csp.
        """
        return self.initial_sudoku.deep_copy()

    def is_complete_assignment(self, assignment):
        """
        Determines if the given assignment of values to a sudoku is a valid solution to this SudokuCSP.

        Keyword arguments:
        assignment -- an instance of a Sudoku representing the assignments to each entry in this CSP.
        """

        for r in range(0, GRID_SIZE):
            for c in range(0, GRID_SIZE):
                entry = self.initial_sudoku.get_entry(r, c)
                if entry != 0 and entry != assignment.get_entry(r, c):
                    raise ValueError("Assignment does not match initial state values.")

        return assignment.is_complete() and assignment.is_valid()

    def get_next_variable(self, assignment):
        """
        Determines the next variable in the assignment to be expanded.

        Returns a tuple containing the row and column of the next variable to be expanded.

        Keyword arguments:
        assignment -- an instance of a Sudoku representing the assignments to each entry in this CSP.
        """

        return self.next_var_heuristic(assignment)

    def get_successors(self, assignment, variable_pos):
        """
        Gets all of the valid successors of the given assignment in regards to the variable position.

        Keyword arguments:
        assignment -- an instance of a Sudoku representing the assignments to each entry in this CSP.
        variable_pos -- a tuple containing the row and column of the variable to be expanded.
        """
        r, c = variable_pos
        if assignment.get_entry(r, c) != 0:
            raise ValueError("Variable position is already filled.")
        else:
            successors = []
            for n in range(1, GRID_SIZE + 1):
                new_state = assignment.deep_copy()
                new_state.set_element(r, c, n)
                if new_state.is_valid():
                    successors.append(new_state)

            self.expanded_nodes += 1
            if self.expanded_nodes % 500 == 0:
                print("Nodes expanded: " + str(self.expanded_nodes))
            return successors