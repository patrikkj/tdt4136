from min_heap import MinHeap
from Map import Map_Obj


class Node:
    def __init__(self, state=None, g=None, h=None, f=None, status=None, parent=None, successors=None):
        self.state = state
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
        self.successors = successors if successors else []

    def __str__(self):
        return f"({self.state[1]}, {self.state[2]})"


def initialize_start_node(start_state, heuristic_func):
    start = Node(
        state=start_state,
        status=None,
        parent=None,
        successors=[]
    )
    start.g = 0
    start.h = heuristic_func(start_state)
    start.f = start.g + start.h
    return start

def initialize_successor_node(parent, successor_state, heuristic_func, cost_func):
    successor = Node(
        state=successor_state,
        status=None,
        parent=parent,
        successors=[]
    )
    successor.g = parent.g + cost_func(parent.state, successor_state)
    successor.h = heuristic_func(successor_state)
    successor.f = successor.g + successor.h
    return successor

def create_path_to(node):
    # Base case
    if node.parent is None:
        return [node]

    return create_path_to(node.parent) + [node]

def attach_and_eval(successor, parent, heuristic_func, cost_func):
    successor.parent = parent
    successor.g = parent.g + cost_func(successor.state, parent.state)
    successor.h = heuristic_func(successor.state)
    successor.f = successor.g + successor.h

def propagate_path_improvements(parent, heuristic_func, cost_func):
    for successor in parent.successors:
        new_cost = parent.g + cost_func(parent.state, successor.state)
        if new_cost < successor.g:
            successor.parent = parent
            successor.g = new_cost
            successor.f = successor.g 


def a_star(start_state, heuristic_func, successors_gen, goal_predicate, cost_func=lambda *_: 1):
    """
    Generalized implementation of A* search.

    Input:
        start_state:        Initial state
        heuristic_func:     Function of the form (state) -> heuristic value
        successors_gen:     Generator which yields all successors for a given state: 
                                state -> yield successor state
        goal_predicate:     Predicate to test whether the given state is a goal state:
                                state -> True or False

        (Optional)
        cost_func:          Function which returns the cost of a state transition:
                                from_state, to_state -> cost
                            Defaults to a cost of one.
    
    Returns:
        A list of the form 
            [(x0, y0), (x1, y1), ..., (xn, yn)] 
        representing a path from start to end node.
    """
    # Memoization table, maps from state to corresponding node
    memo = {}

    # Initialize containers
    closed = set()
    open_ = MinHeap(key_attr='f')

    # Initialize starting node
    start = initialize_start_node(start_state, heuristic_func)
    open_.insert(start)
    memo[start_state] = start

    # Loop as long as there are nodes to process 
    while open_:
        u = open_.extract_min()
        closed.add(u)

        # Test to see if goal state is reached
        if goal_predicate(u.state):
            print("Goal found!")
            return [node.state[1:] for node in create_path_to(u)]       

        # Process successor states of current node
        for v_state in successors_gen(u.state):
            # Check if state has been previously encountered, create new by default
            if v_state in memo:
                v = memo[v_state]
            else:
                v = initialize_successor_node(u, v_state, heuristic_func, cost_func)
                memo[v_state] = v

            # Add to parents' list of successors
            u.successors.append(v)

            # In case of encountering a new node (not opened or closed)
            if v not in open_ and v not in closed:
                attach_and_eval(v, u, heuristic_func, cost_func)
                open_.insert(v)
            # If path is an improvement to previously discovered node
            elif u.g + cost_func(u.state, v.state) < v.g:
                attach_and_eval(v, u, heuristic_func, cost_func)
                # If successor is an internal node
                if v in closed:
                    propagate_path_improvements(v, heuristic_func, cost_func)
