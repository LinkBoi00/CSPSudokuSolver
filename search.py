# Import GRID_SIZE from sudoku_problem
from config import GRID_SIZE

def backtracking_search(csp):
    """
    Initializes a backtracking search algorithm to solve the given CSP.

    Keyword arguments:
    csp -- an instance of a SudokuCSP problem used as the problem to be solved.
    """
    assignment = csp.get_initial_sudoku()
    return recursive_backtracking(assignment, csp)


def recursive_backtracking(assignment, csp):
    """
    A recursive backtracking search algorithm that uses the given assignment and CSP to solve.

    Keyword arguments:
    assignment -- an instance of a Sudoku representing the assignments to each entry in a CSP.
    csp -- an instance of a SudokuCSP problem used as the problem to be solved.
    """
    if csp.is_complete_assignment(assignment):
        return assignment

    var_pos = csp.get_next_variable(assignment)

    for asgn in csp.get_successors(assignment, var_pos):
        try:
            result = recursive_backtracking(asgn, csp)
            return result
        except ValueError as err:
            if str(err) == "Search Failure.":
                continue
            else:
                raise

    raise ValueError("Search Failure.")


def arc_consistency_3(assignment, initial_arcs):
    """
    This is an implementation of the ac-3 arc consistency: constraint propagation algorithm.

    This algorithm removes all of the inconsistent possible values in the assignment in order to reduce the number
    of possibilities, and in turn increase efficiency by reducing the number of nodes to expand.

    Keyword arguments:
    assignment -- an instance of a Sudoku representing the assignments to each entry in a CSP.
    """
    arc_queue = initial_arcs

    while len(arc_queue) > 0:
        head, tail = arc_queue.pop(0)
        tr, tc = tail
        if remove_inconsistent_values(assignment, head, tail) and len(assignment.get_possible_values(tr, tc)) == 1:
            for pos in assignment.get_neighbors(tail[0], tail[1]):
                arc_queue.append((tail, pos))


def remove_inconsistent_values(assignment, head, tail):
    """
    Removes inconsistent values from the tail that do not agree with values in the head.

    Returns a boolean indicating whether any values were removed.

    Keyword arguments:
    assignment -- an instance of a Sudoku representing the assignments to each entry in a CSP.
    head -- a tuple containing the row and column of the head of the consistency arc to be evaluated.
    tail -- a tuple containing the row and column of the tail of the consistency arc to be evaluated.
    """
    removed = False

    hr, hc = head
    tr, tc = tail

    possible_tail_values = assignment.get_possible_values(tr, tc)
    possible_head_values = assignment.get_possible_values(hr, hc)

    if len(possible_head_values) == 1 and (possible_head_values[0] in possible_tail_values):
        possible_tail_values.remove(possible_head_values[0])
        removed = True
        if len(possible_tail_values) == 1:
            assignment.set_element(tr, tc, possible_tail_values[0])

    return removed


def mrv_next_var_heuristic(assignment):
    """
    Determines the next variable in the assignment to be expanded in order of least number of possible values.

    Returns a tuple containing the row and column of the next variable to be expanded.

    Keyword arguments:
    assignment -- an instance of a Sudoku representing the assignments to each entry in this CSP.
    """

    pos_list = []
    num_possible_list = []
    for r in range(0, GRID_SIZE):
        for c in range(0, GRID_SIZE):
            if assignment.get_entry(r, c) == 0:
                pos = (r, c)
                pos_list.append(pos)
                num_possible_list.append(len(assignment.get_possible_values(r, c)))

    if len(pos_list) > 0:
        return pos_list[num_possible_list.index(min(num_possible_list))]
    else:
        raise ValueError("Assignment is already complete.")


def trivial_next_var_heuristic(assignment):
    """
    Returns the first variable that has not yet been expanded.

    Returns a tuple containing the row and column of the next variable to be expanded.

    Keyword arguments:
    assignment -- an instance of a Sudoku representing the assignments to each entry in this CSP.
    """

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if assignment.get_entry(r, c) == 0:
                pos = (r, c)
                return pos

    raise ValueError("Assignment is already complete.")