from a_star import a_star
from Map import Map_Obj

def euclidean(state):
    '''
    Heuristic function that calculates the euclidean (diagonal) distance
    from the input position to the current goal position
    '''
    map_, *pos = state
    goal = map_.get_goal_pos()
    return ((goal[0] - pos[0])**2 + (goal[1] - pos[1])**2)**0.5

def manhattan(state):
    '''
    Heuristic function given by the sum of the length of the
    decomposed vectors from current position to goal position.
    '''
    map_, *pos = state
    goal = map_.get_goal_pos()
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

def successors_gen(state):
    '''
    Generator function which yields all successors for a given state.
    '''
    map_, x, y = state
    (w, h) = map_.int_map.shape

    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        x_ = x + dx
        y_ = y + dy
    
        if (x_ < 0) or (x_ >= w) or (y_ < 0) or (y_ >= h):
            continue
    
        if map_.get_cell_value((x + dx, y + dy)) != Map_Obj.OBSTACLE_CELL:
            yield (map_, x + dx, y + dy)

def goal_predicate(state):
    '''
    Checks if current position is a goal configuration.
    '''
    map_, x, y = state
    return tuple(map_.get_goal_pos()) == (x, y)

def cost_func(from_state, to_state):
    '''
    Returns the cost of a state transition, as determined by the cell value
    of the target state (the same for all cells in part 1 map).
    '''
    map_, x, y = to_state
    return map_.get_cell_value((x, y))

def main():
    for task in range(1, 5): # runs through tasks 1 - 4, continues after key input
        map_obj = Map_Obj(task=task)

        start_state = (map_obj, *map_obj.get_start_pos())
        heuristic_func = manhattan

        output = a_star(start_state, heuristic_func, successors_gen, goal_predicate, cost_func=cost_func)
        for coords in output:
            map_obj.set_cell_value(coords, "☺", str_map = True)

        map_obj.show_map()
        input()

if __name__ == "__main__":
    main()