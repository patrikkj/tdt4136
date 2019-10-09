import copy
from assignment_base import CSPBase


class CSPOneLine(CSPBase):
    '''
    CSP solver implementing 'Backtrack Search' and 
    'AC-3' using a single line of code per algorithm.
    '''

    def backtrack(self, assignment, default_order=False):
        return assignment if all(len(domain) == 1 for domain in assignment.values()) else (lambda u_var: next((_ for _ in ((lambda assignment_copy: self.backtrack(assignment_copy, default_order=default_order) if self.inference(assignment_copy, list((j, u_var) for j in self.constraints[u_var].keys())) else False)({k:(v if k != u_var else [value]) for k, v in copy.deepcopy(assignment).items()}) for value in (assignment[u_var] if default_order else list(zip(*sorted((lambda neighbours_legals: {k : neighbours_legals.count(k) for k in assignment[u_var]})([v for neighbour in self.constraints[u_var].keys() for v in assignment[neighbour]]).items(), key=lambda tup: tup[1])))[0])) if _), {}))(min(tup for tup in ((len(domain), var) for var, domain in assignment.items()) if tup[0] > 1)[1])
    
    def inference(self, assignment, queue):
        return next((e for e in (queue.extend((_j, i) for _j in (self.constraints[i].keys() - {j})) if assignment[i] else False for i, j in queue if any(list(zip(*[(False, None) if any((x, y) in self.constraints[i][j] for y in assignment[j]) else (True, assignment[i].remove(x)) for x in assignment[i]]))[0])) if e == False), True)


class CSPFiveLines(CSPBase):
    '''
    CSP solver implementing 'Backtrack Search' and 
    'AC-3' using a single line of code per method.
    '''

    def backtrack(self, assignment, default_order=False):
        return assignment if all(len(domain) == 1 for domain in assignment.values()) else (lambda u_var: next((_ for _ in ((lambda assignment_copy: self.backtrack(assignment_copy, default_order=default_order) if self.inference(assignment_copy, list((j, u_var) for j in self.constraints[u_var].keys())) else False)({k:(v if k != u_var else [value]) for k, v in copy.deepcopy(assignment).items()}) for value in self.order_legal_values(assignment, u_var, default_order=default_order)) if _), {}))(self.select_unassigned_variable(assignment))

    def order_legal_values(self, assignment, variable, default_order=False):
        return assignment[variable] if default_order else list(zip(*sorted((lambda neighbours_legals: {k : neighbours_legals.count(k) for k in assignment[variable]})([v for neighbour in self.constraints[variable].keys() for v in assignment[neighbour]]).items(), key=lambda tup: tup[1])))[0]

    def select_unassigned_variable(self, assignment):
        return min(tup for tup in ((len(domain), var) for var, domain in assignment.items()) if tup[0] > 1)[1]

    def inference(self, assignment, queue):
        return next((e for e in (queue.extend((_j, i) for _j in (self.constraints[i].keys() - {j})) if assignment[i] else False for i, j in queue if self.revise(assignment, i, j)) if e == False), True)

    def revise(self, assignment, i, j):
        return any(list(zip(*[(False, None) if any((x, y) in self.constraints[i][j] for y in assignment[j]) else (True, assignment[i].remove(x)) for x in assignment[i]]))[0])


# Static method signatures from base class
def create_map_coloring_csp(cls):
    return CSPBase.create_map_coloring_csp(cls())

def create_sudoku_csp(filename, cls):
    return CSPBase.create_sudoku_csp(filename, cls())

def print_sudoku_solution(solution):
    CSPBase.print_sudoku_solution(solution)


def solve_and_print(cls, all_orders=False, all_puzzles=False):
    orders = (False, True) if all_orders else (False, )
    puzzles = ["easy", "medium", "hard", "veryhard"]
    if all_puzzles:
        puzzles.extend(["extreme", "worldshardest"])

    for filename in puzzles:
        print(f"\n --- Solving {filename.capitalize()} using {cls.__name__} --- ")
        for default_order in orders:
            csp = create_sudoku_csp(f"{filename}.txt", cls)
            solution = csp.backtracking_search(default_order)
            if all_orders:
                print(f"Default order = {default_order}")
            print_sudoku_solution(solution)


def main():
    # Print results for five 
    solve_and_print(CSPFiveLines, all_puzzles=True)

    # Print results for one line 
    solve_and_print(CSPOneLine, all_puzzles=True)

if __name__ == "__main__":
    main()
