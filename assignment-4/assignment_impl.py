import copy
from assignment_base import CSPBase


class CSPImpl(CSPBase):
    def __init__(self):
        super().__init__()

        # Metadata
        self._backtrack_calls = 0
        self._failures = 0
    

    def backtrack(self, assignment, default_order=False):
        '''
        Performs a single iteration of variable assignment and 
        recursively solves the subproblem.
        '''
        self._backtrack_calls += 1  # Metadata

        # Check if partial solution is complete
        if all(len(domain) == 1 for domain in assignment.values()):
            return assignment
        
        # Select an unassigned variable, and attempt to solve
        # subproblem for every legal value in the variables' domain. 
        u_var = self.select_unassigned_variable(assignment)
        for value in self.order_legal_values(assignment, u_var, default_order=default_order):
            # Copy domains and shrink selected variable domain, 
            # equivalent to variable assignment of the form: 
            #   u_var <- value
            assignment_copy = copy.deepcopy(assignment)
            assignment_copy[u_var] = [value]

            # Revisit nodes which might have been affected by variable 
            # assignment (all neighbours in constraint graph)
            neighbour_edges = list((j, u_var) for j in self.constraints[u_var].keys())
            if self.inference(assignment_copy, neighbour_edges):
                # Attempt to solve subproblem if domain was reduced
                # as a result of the new var. assignment
                result = self.backtrack(assignment_copy, default_order=default_order)
                if result:
                    return result
        self._failures += 1
        return {}    

    def order_legal_values(self, assignment, variable, default_order=False):
        '''
        Least-constraining value heuristic: choose a value that rules
        out the smallest number of values in variables connected to the
        current variable by constraints.   

        Returns:
            List of legal values for 'variable', sorted by 
            number of occurences in neighbours' legal values
        '''
        if default_order:
            return assignment[variable]

        # Create mapping from selectable variable assignment 
        # to number of occurences in neighbours' legal values
        neighbours = self.constraints[variable].keys()
        neighbours_legals = [v for neighbour in neighbours for v in assignment[neighbour]]
        frequencies = {k : neighbours_legals.count(k) for k in assignment[variable]}
        return sorted(frequencies.keys(), key=lambda key: frequencies[key])

    def select_unassigned_variable(self, assignment):
        '''
        Select unassigned variable according to the degree heuristic,
        ie. the variable with the highest number of constraints
        '''
        # NOTE: 'min' on tuples performs an element-wise comparison
        lengths = ((len(domain), var) for var, domain in assignment.items())
        return min(tup for tup in lengths if tup[0] > 1)[1]

    def inference(self, assignment, queue):
        '''
        Given a set of assignments and constraints, revises 
        the corresponding variable domains as well as the domain 
        of any variables affected by the domain reduction.
        '''
        while queue:
            i, j = queue.pop(0) 
            if self.revise(assignment, i, j): # Trim domain
                # If the trimmed domain is empty, there is no solution
                if not assignment[i]:
                    return False

                # Revisit neighbours in constraint graph
                queue.extend((_j, i) for _j in (self.constraints[i].keys() - {j}))
        return True

    def revise(self, assignment, i, j):
        '''
        Given a pair of variables and their domains, removes all values which 
        violates a constraint in the former variables' domain.
        '''
        # For every value 'x' in I's domain, assert that there exists
        # a corresponding legal value 'y' in J's domain.
        revised = False
        for x in assignment[i]:
            # If no such value exists, remove 'x' from I's domain
            if not any((x, y) in self.constraints[i][j] for y in assignment[j]):
                assignment[i].remove(x)
                revised = True
        return revised


# Static method signatures from base class
def create_map_coloring_csp():
    return CSPBase.create_map_coloring_csp(CSPImpl())

def create_sudoku_csp(filename):
    return CSPBase.create_sudoku_csp(filename, CSPImpl())

def print_sudoku_solution(solution):
    CSPBase.print_sudoku_solution(solution)


def main():
    # Print results
    for filename in ("easy", "medium", "hard", "veryhard", "extreme", "worldshardest"):
    # for filename in ("easy", "medium", "hard", "veryhard"):
        print(f"\n --- {filename.capitalize()} --- ")
        for default_order in (False, True):
            csp = create_sudoku_csp(f"{filename}.txt")
            solution = csp.backtracking_search(default_order=default_order)
            print(f"Default order = {default_order}")
            print(f"Number of calls to backtrack: {csp._backtrack_calls}")
            print(f"Number of backtrack failures: {csp._failures}")
            print_sudoku_solution(solution)

if __name__ == "__main__":
    main()
