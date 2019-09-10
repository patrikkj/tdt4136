from a_star import a_star
from Map import Map_Obj
from part_1_and_2 import successors_gen, cost_func


INSAYN_SPEED = False # whether our drunk friend is moving at half our speed (true) o a quarter of our speed (false)


def samf_chase_heuristic(state):
    '''
    As the goal is moving in a straight line (decreasing x-value), we estimate the manhattan distance to current goal position,
    then correct it in the x direction by calculating the displacement that will occur in the number of ticks it will take for us
    to get to the current goal position.
    '''
    map_, *pos = state
    goal = map_.get_goal_pos()
    h_0 = abs(goal[0] - pos[0]) + abs(goal[1] - pos[1]) # initial goal distance estimate (manhattan)
    dx = h_0 / 4 # estimated displacement in x direction when we arrive at goal
    new_goal = goal[0] - dx, goal[1] # update goal estimate
    return abs(new_goal[0] - pos[0]) + abs(new_goal[1] - pos[1])


def goal_predicate(state):
    '''
    Call tick() function for each search iteration
    '''
    map_, x, y = state
    map_.tick()

    ##################################################
    if (INSAYN_SPEED):
        map_.tick()
    ##################################################

    return tuple(map_.get_goal_pos()) == (x, y)

def main():
    map_obj = Map_Obj(task=5)

    start_state = (map_obj, *map_obj.get_start_pos())
    heuristic_func = samf_chase_heuristic

    output = a_star(start_state, heuristic_func, successors_gen, goal_predicate, cost_func=cost_func)
    for node in output:
        map_obj.set_cell_value(node.state[1:], "☺", str_map = True)

    map_obj.show_map()

if __name__ == "__main__":
    main()