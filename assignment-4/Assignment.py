import copy
import itertools

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        # Metadata
        self._backtrack_calls = 0
        self._failures = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = list(filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j]))

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self, order=False):
        """
        This functions starts the CSP solver and returns the found
        solution.
        """
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment, order=order)

    def backtrack(self, assignment, order=False):
        self._backtrack_calls += 1

        # Check if partial solution is complete
        if all(len(domain) == 1 for domain in assignment.values()):
            return assignment
        
        # Select an unassigned variable according to a heuristic
        u_var = self.select_unassigned_variable(assignment)
        
        # Attempt to solve subproblem with all possible values for the given variable
        iterable = self.order_legal_values(assignment, u_var) if order else assignment[u_var]
        for value in iterable:
            assignment_copy = copy.deepcopy(assignment)

            # Assign the value to the variable
            assignment_copy[u_var] = [value]

            # Revisit all neighbours to variable in the constraint graph
            # TODO: implement queue as an actual queue instead of list
            updated_queue = list((j, u_var) for j in self.constraints[u_var].keys())

            # If domain is reduced as a result of vairable assignment            
            if self.inference(assignment_copy, updated_queue):
                # Attempt to solve subproblem with the newly assigned variable
                result = self.backtrack(assignment_copy, order=order)
                if result:
                    return result
        self._failures += 1
        return {}         

    def order_legal_values(self, assignment, variable):
        '''
        Least-constraining value heuristic: choose a value that rules
        out the smallest number of values in variables connected to the
        current variable by constraints.   
        --> Order legal values according to number of occurences in neighbours' legal values
        '''
        # TODO: make this function readable
        neighbours = self.constraints[variable].keys()
        frequencies = {k : 0 for k in assignment[variable]}
        
        for value in assignment[variable]:
            frequencies[value] = sum(value == neighbour_value for neighbour in neighbours for neighbour_value in assignment[neighbour])
        return sorted(frequencies.keys(), key=lambda key: frequencies[key])

    def select_unassigned_variable(self, assignment):
        '''
        Select unassigned variable according to the degree heuristic,
        ie. the variable with the highest number of constraints
        '''
        # NOTE: 'min' on tuples performs an element-wise comparison
        lengths = ((len(v), k) for k, v in assignment.items())
        return min(tup for tup in lengths if tup[0] > 1)[1]

    def inference(self, assignment, queue):
        while queue:
            i, j = queue.pop(0) 
            
            # Trim domain
            if self.revise(assignment, i, j):
                # If the trimmed domain is empty, there is no solution
                if len(assignment[i]) < 1:
                    return False

                # Revisit neighbours in constraint graph
                queue.extend((_j, i) for _j in (self.constraints[i].keys() - {j}))
        return True

    def revise(self, assignment, i, j):
        # For every value 'x' in I's domain, assert that there exists
        # a corresponding legal value 'y' in J's domain.
        revised = False
        for x in assignment[i]:
            if not any((x, y) in self.constraints[i][j] for y in assignment[j]):
                assignment[i].remove(x)
                revised = True
        return revised

def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp


def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str, range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    # TODO: Cleanup string concatenation
    output = ""
    for row in range(9):
        for col in range(9):
            output += solution['%d-%d' % (row, col)][0]
            if col == 2 or col == 5:
                output += ' |'
            output += " "
        output += "\n"
        if row == 2 or row == 5:
            output += '------+-------+------\n'
    
    print(output)


for filename in ("easy", "medium", "hard", "veryhard"):
    print(f"\n --- {filename.capitalize()} --- ")
    for order in (True, False):
        csp = create_sudoku_csp(f"{filename}.txt")
        solution = csp.backtracking_search(order=order)
        print(f"\tORDER = {order}")
        print(f"\tNumber of calls to backtrack: {csp._backtrack_calls}")
        print(f"\tNumber of backtrack failures: {csp._failures}\n")
    print_sudoku_solution(solution)
