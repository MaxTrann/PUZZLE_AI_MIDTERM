from .helpers import get_neighbors, apply_action
import itertools
from collections import deque

#Test case:[[1,2,3], [7, 0, 5], [8, 4, 6]]
def sensorless_search(start_set, goal_set):
    # --- 1) Nếu đầu vào là tuple-of-tuples, flatten về flat-9-tuple ---
    if start_set and isinstance(next(iter(start_set)), tuple) and isinstance(next(iter(start_set))[0], tuple):
        start_set = { sum(s, ()) for s in start_set }
    if goal_set and isinstance(next(iter(goal_set)), tuple) and isinstance(next(iter(goal_set))[0], tuple):
        goal_set = { sum(g, ()) for g in goal_set }

    # --- 2) Kiểm tra solvability ---
    def is_solvable(state):
        inv = 0
        for i in range(8):
            for j in range(i+1, 9):
                if state[i] and state[j] and state[i] > state[j]:
                    inv += 1
        return inv % 2 == 0

    # --- 3) Khởi tạo belief ban đầu ---
    if not start_set:
        belief0 = set(filter(is_solvable, itertools.permutations(range(9))))
    else:
        belief0 = set(start_set)

    queue      = deque([(belief0, [])])
    visited    = set()
    expansions = 0

    moves = {
        'up':    (-1,  0),
        'down':  ( 1,  0),
        'left':  ( 0, -1),
        'right': ( 0,  1)
    }

    # --- 4) BFS over belief states ---
    while queue:
        belief, path = queue.popleft()
        key = frozenset(belief)
        if key in visited:
            continue
        visited.add(key)
        expansions += 1

        # Điều kiện dừng: nếu ANY state trong belief match goal
        if any(st in goal_set for st in belief):
            return path, expansions

        # Sinh belief kế tiếp
        for action, (dr, dc) in moves.items():
            new_belief = set()
            ok = True
            for st in belief:
                zero = st.index(0)
                r, c = divmod(zero, 3)
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    idx2 = nr*3 + nc
                    lst  = list(st)
                    lst[zero], lst[idx2] = lst[idx2], lst[zero]
                    new_belief.add(tuple(lst))
                else:
                    ok = False
                    break
            if ok and new_belief:
                queue.append((new_belief, path + [action]))

    return None, expansions


def apply_action_belief(state, action):
        """
        Áp dụng hành động ('up', 'down', 'left', 'right') lên state dạng tuple of tuple (3x3).
        Trả về state mới sau khi di chuyển ô trống (0), hoặc None nếu không hợp lệ.
        """
        if state is None:
            raise ValueError("State là None - không thể thực hiện hành động.")

        moves = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        if action not in moves:
            raise ValueError(f"Hành động không hợp lệ: {action}")

        # Chuyển state thành dạng 1 chiều
        flat = sum(state, ())
        zero = flat.index(0)
        r, c = divmod(zero, 3)

        dr, dc = moves[action]
        nr, nc = r + dr, c + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            new_idx = nr * 3 + nc
            flat = list(flat)
            flat[zero], flat[new_idx] = flat[new_idx], flat[zero]
            return tuple(tuple(flat[i:i + 3]) for i in range(0, 9, 3))

        return None  # Nếu move không hợp lệ

def belief_bfs(start_set, goal_set):
    """
    Tìm kiếm Belief-State BFS với nhiều trạng thái đầu vào và mục tiêu.
    - start_set: tập hợp các trạng thái đầu vào (belief state ban đầu)
    - goal_set: tập hợp các trạng thái mục tiêu
    Trả về danh sách hành động và số lần mở rộng.
    """
    def flatten(state):
        """Chuyển trạng thái 3x3 thành tuple 9 phần tử."""
        return tuple(cell for row in state for cell in row)

    # Chuyển goal_set sang dạng flatten để so sánh
    goal_flat_set = {flatten(g) for g in goal_set}

    queue = deque([(start_set, [])])  # Mỗi phần tử: (belief_state, actions)
    visited = set()
    expansions = 0

    while queue:
        belief, actions = queue.popleft()
        frozen = frozenset(belief)
        if frozen in visited:
            continue
        visited.add(frozen)
        expansions += 1

        # DEBUG: In thông tin để kiểm tra goal và belief
        # print("\n==== DEBUG ====")
        # print("Goal Set (flattened):")
        # for g in goal_flat_set:
        #     print(g)

        # print("Current Belief States (flattened):")
        # for b in belief:
        #     print(flatten(b))
        # print("================\n")

        # dừng khi ANY one state đạt goal
        if any(flatten(s) in goal_flat_set for s in belief):
            return actions, expansions

        # Các hành động có thể: up, down, left, right
        for action in ["up", "down", "left", "right"]:
            new_belief = set()
            for state in belief:
                try:
                    from algorithms.belief_state import apply_action_belief
                    new_state = apply_action_belief(state, action)
                    if new_state is not None:
                        new_belief.add(new_state)
                except Exception:
                    continue
            if new_belief:
                queue.append((new_belief, actions + [action]))

    return None, expansions

