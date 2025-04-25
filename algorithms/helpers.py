def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row = zero_index // 3
    col = zero_index % 3
    moves = {
        'up':    (-1, 0),
        'down':  ( 1, 0),
        'left':  ( 0, -1),
        'right': ( 0,  1)
    }

    for (dr, dc) in moves.values():
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append(tuple(new_state))
    return neighbors

def manhattan_distance(state, goal):
    dist = 0
    for i, val in enumerate(state):
        if val != 0:
            goal_index = goal.index(val)
            row_s, col_s = divmod(i, 3)
            row_g, col_g = divmod(goal_index, 3)
            dist += abs(row_s - row_g) + abs(col_s - col_g)
    return dist

def apply_action(state, action):
        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)
        moves = {
            'up':    (-1, 0),
            'down':  ( 1, 0),
            'left':  ( 0, -1),
            'right': ( 0,  1)
        }
        dr, dc = moves[action]
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            return tuple(new_state)
        return state  # nếu không hợp lệ, trả về nguyên 