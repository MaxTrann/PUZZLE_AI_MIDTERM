from .helpers import get_neighbors
import itertools

def sensorless_search(goal, initial_states=None):
    from collections import deque

    all_states = set(itertools.permutations(range(9)))

    # Nếu không truyền initial_states thì mặc định là toàn bộ
    if initial_states is None:
        possible_states = all_states
    else:
        possible_states = set(initial_states)

    queue = deque([(possible_states, [])])
    visited = set()
    expansions = 0

    while queue:
        current_states, path = queue.popleft()
        frozen = frozenset(current_states)

        if frozen in visited:
            continue
        visited.add(frozen)
        expansions += 1

        if len(current_states) == 1 and goal in current_states:
            return path, expansions

        for action in ['up', 'down', 'left', 'right']:
            new_states = set()
            for state in current_states:
                zero_index = state.index(0)
                row, col = divmod(zero_index, 3)
                moves = {
                    'up':    (-1, 0),
                    'down':  ( 1, 0),
                    'left':  ( 0, -1),
                    'right': ( 0,  1)
                }
                dr, dc = moves[action]
                new_row = row + dr
                new_col = col + dc
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_index = new_row * 3 + new_col
                    new_state = list(state)
                    new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                    new_states.add(tuple(new_state))
            if new_states:
                queue.append((new_states, path + [action]))

    return None, expansions

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


def belief_bfs(start_belief, goal_state):
    from collections import deque

    def is_goal_belief(belief):
        return all(state == goal_state for state in belief)

    def apply_action(state, action):
        state = list(state)
        zero = state.index(0)
        r, c = divmod(zero, 3)
        moves = {
            'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)
        }
        dr, dc = moves[action]
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_idx = nr * 3 + nc
            state[zero], state[new_idx] = state[new_idx], state[zero]
            return tuple(state)
        return None

    def get_neighbors(belief):
        neighbors = []
        for action in ['up', 'down', 'left', 'right']:
            new_belief = set()
            for state in belief:
                next_state = apply_action(state, action)
                if next_state:
                    new_belief.add(next_state)
            if new_belief:
                neighbors.append((frozenset(new_belief), action))
        return neighbors

    queue = deque([(frozenset(start_belief), [])])
    visited = set()
    expansions = 0

    while queue:
        belief, path = queue.popleft()
        if belief in visited:
            continue
        visited.add(belief)
        expansions += 1

        if is_goal_belief(belief):
            return path, expansions

        if len(belief) == 1:
            # Hội tụ về 1 trạng thái duy nhất
            return path, expansions

        for new_belief, action in get_neighbors(belief):
            if new_belief not in visited:
                queue.append((new_belief, path + [action]))

    return None, expansions