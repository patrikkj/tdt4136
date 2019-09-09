from datastructures import MinHeap
from Map import Map_Obj

# def relax_dijkstra(u, v, w, decrease_key):
#     if get_key(v) > get_key(u) + w:
#         decrease_key(v, get_key(u) + w)
#         set_pi(v, u)

# def dijkstra(graph, start, **kwargs):
#     # Generalize
#     default_kwargs = {'key_attr': 'key', 'neighbours_attr': 'neighbours', 'pi_attr': 'pi'}
#     _generalize(kwargs, default_kwargs)

#     # Initialize nodes
#     initialize_single_source(graph, start)

#     # Initialize min-heap using 'key' as priority
#     q = MinHeap(graph, key_attr=key_attr)

#     # Greedy traversal node by node
#     while q:
#         u = q.extract_min()
#         for v, _ in get_neighbours(u):
#             # Relax with reference to decrease-key function, lookup using node instead of index
#             relax_dijkstra(u, v, w, q.decrease_key_noderef)

# Map format
START_CELL = 'S'
GOAL_CELL = 'G'
OBSTACLE_CELL = '-1'
REGULAR_CELLS = ('1', '2', '3', '4')

# Heuristic functions
heuristics = {
    "manhattan": lambda start, end: abs(end[0] - start[0]) + abs(end[1] - start[1]),
    "euclidian": lambda start, end: ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
}


class Node:
    # Constants for node status
    OPEN, CLOSED = 1, 0


def initialize_start_node(start_state, heuristic_func):
    start = Node()
    start.state = start_state
    start.g = 0
    start.h = heuristic_func(start_state)
    start.f = start.g + start.h
    start.status = Node.OPEN
    start.parent = None
    start.successors = []
    return start

def initialize_successor_node(parent, successor_state, heuristic_func, cost_func):
    successor = Node()
    successor.state = successor_state
    successor.g = parent.g + cost_func(parent.state, successor_state)
    successor.h = heuristic_func(successor_state)
    successor.f = successor.g + successor.h
    successor.status = None
    successor.parent = parent
    successor.successors = []
    return successor



def successors_gen(coord):
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        pass

def create_path_to(node):
    # Base case
    if node.parent is None:
        return [node]

    return create_path_to(node.parent) + [node]

def attach_and_eval(successor, parent):
    pass

def propagate_path_improvements(successor):
    pass

def a_star(start_state, heuristic_func, successors_gen, goal_predicate, hash_func=None, cost_func=None):
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
        hash_func:          Function for hashing a given state, used for memoization and and state comparison: 
                                state -> hash value
                            If function is omitted, defaults to built-in hash function.
        cost_func:          Function which returns the cost of a state transition:
                                from_state, to_state -> cost
                            Defaults to a cost of one.
    
    Returns:
        A list of the form 
            [(x0, y0), (x1, y1), ..., (xn, yn)] 
        representing a path from start to end node.
    """
    # Set default args
    if not hash_func:
        hash_func = hash
    if not cost_func:
        cost_func = lambda *_: 1

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
        u.status = Node.CLOSED

        # Test to see if goal state is reached
        if goal_predicate(u.state):
            return create_path_to(u)        

        # Process successor states of current node
        for v_state in successors_gen():
            # Check if state has been previously encountered
            if v_state in memo:
                v = memo[v_state]
            else:
                v = initialize_successor_node(u, v_state, heuristic_func, cost_func)

            # Add to parents' list of successors
            u.successors.append(v)

            if v not in open_ and v not in closed:
                attach_and_eval(v, u)
                open_.insert(v)
                v.status = Node.OPEN
            elif u.g + cost_func(u.state, v.state) < v.g:
                attach_and_eval(v, u)
                if v.status == Node.CLOSED:
                    propagate_path_improvements(v)


def task_1():
    map_obj = Map_Obj()
    map_obj.show_map()
    map_obj.print_map(map_obj.str_map)

task_1()