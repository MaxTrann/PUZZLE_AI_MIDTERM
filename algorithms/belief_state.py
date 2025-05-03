from .helpers import get_neighbors, apply_action
import itertools
from collections import deque

def sensorless_search(goal, initial_states=None):
    def is_solvable(state):
        inv = 0
        for i in range(8):
            for j in range(i+1, 9):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inv += 1
        return inv % 2 == 0

    all_states = set(filter(is_solvable, itertools.permutations(range(9))))

    # Nếu không truyền initial_states thì mặc định là toàn bộ
    if initial_states is None:
        possible_states = all_states
    else:
        possible_states = set(initial_states)

    queue = deque([(possible_states, [])]) # sử dụng deque để BFS
    visited = set()
    expansions = 0
    moves = {
        'up':    (-1, 0),
        'down':  ( 1, 0),
        'left':  ( 0, -1),
        'right': ( 0,  1)
    }
    while queue:
        current_states, path = queue.popleft()
        frozen = frozenset(current_states)
        if frozen in visited:
            continue
        visited.add(frozen)
        expansions += 1

        if len(current_states) == 1 and goal in current_states:
            return path, expansions

        for action in moves:
            new_states = set()
            valid = True
            for state in current_states:
                if 0 not in state: 
                    valid = False
                    break
                zero_index = state.index(0)
                row, col = divmod(zero_index, 3)
                dr, dc = moves[action]
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_index = new_row * 3 + new_col
                    new_state = list(state)
                    new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                    new_states.add(tuple(new_state))
                else:
                    valid = False # nếu 1 state không thực hiện được 
                    break
            if valid and new_states:
                queue.append((new_states, path + [action]))

    return None, expansions

def belief_bfs(start_belief, goal_state):
    def is_goal_belief(belief):
        # Tất cả trạng thái trong belief phải trùng goal
        return all(state == goal_state for state in belief)

    # Kiểm tra trạng thái có lời giải không
    def is_solvable(state):
        flat = sum(state, ())
        inv = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] and flat[j] and flat[i] > flat[j]:
                    inv += 1
        return inv % 2 == 0
    
    # Sinh các belief kế tiếp
    def get_neighbors(belief):
        neighbors = []
        for action in ['up', 'down', 'left', 'right']:
            new_belief = set()
            for state in belief:
                next_state = apply_action_belief(state, action)
                if next_state:
                    new_belief.add(next_state)
            if new_belief:
                neighbors.append((frozenset(new_belief), action))
        return neighbors

    # Lọc belief ban đầu: loại các trạng thái không thể giải
    start_belief = {s for s in start_belief if is_solvable(s)}
    if not start_belief:
        return None, 0

    queue = deque([(frozenset(start_belief), [])])
    visited = set()
    expansions = 0

    while queue:
        belief, path = queue.popleft()
        if belief in visited:
            continue
        visited.add(belief)
        expansions += 1

        if is_goal_belief(belief) or (len(belief) == 1 and goal_state in belief):
            return path, expansions

        for new_belief, action in get_neighbors(belief):
            if new_belief not in visited:
                queue.append((new_belief, path + [action]))

    return None, expansions

def apply_action_belief(state, action):
        """
        Áp dụng hành động lên một state dạng tuple of tuple (3x3)
        """
        flat = sum(state, ())  # Chuyển thành tuple 1 chiều
        zero = flat.index(0)
        r, c = divmod(zero, 3)
        moves = {
            'up': (-1, 0), 'down': (1, 0),
            'left': (0, -1), 'right': (0, 1)
        }
        dr, dc = moves[action]
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_idx = nr * 3 + nc
            flat = list(flat)
            flat[zero], flat[new_idx] = flat[new_idx], flat[zero]
            return tuple(tuple(flat[i:i+3]) for i in range(0, 9, 3))
        return None