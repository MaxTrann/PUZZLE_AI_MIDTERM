from .helpers import get_neighbors, is_solvable
from collections import deque
import heapq
import random

def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set([start])
    expansions = 0
    while queue:
        current_state, path = queue.popleft()
        expansions += 1
        if current_state == goal:
            return path, expansions
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                queue
    return None, expansions

def dfs(start, goal, depth_limit=50):
    def dfs_recursive(state, path, visited, depth, expansions):
        if depth > depth_limit:
            return None, expansions
        expansions += 1

        if state == goal:
            return path, expansions
        if state in visited:
            return None, expansions

        visited.add(state)
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                result, expansions = dfs_recursive(neighbor, path + [neighbor], visited, depth + 1, expansions)
                if result:
                    return result, expansions
        return None, expansions
    
    return dfs_recursive(start, [start], set(), 0, 0)

def ucs(start, goal):
    pq = []
    heapq.heappush(pq, (0, start, [start]))  # (cost, state, path)
    visited = set()
    expansions = 0
    while pq:
        cost, current_state, path = heapq.heappop(pq)
        expansions += 1
        if current_state == goal:
            return path, expansions
        if current_state in visited:
            continue
        visited.add(current_state)
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + 1, neighbor, path + [neighbor]))
    return None, expansions

def iddfs(start, goal, max_depth=50):
    expansions = [0]
    def dls(current, limit, path, visited):
        expansions[0] += 1
        if current == goal:
            return path
        if limit == 0:
            return None
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                result = dls(neighbor, limit - 1, path + [neighbor], visited)
                if result is not None:
                    return result
                visited.remove(neighbor)
        return None
    if start == goal:
        return [start], 0
    for depth in range(max_depth + 1):
        visited = set([start])
        result = dls(start, depth, [start], visited)
        if result is not None:
            return result, expansions[0]
    return [], expansions[0]

def backtracking_search(start, goal, max_depth = 50):
    expansions = [0]
    visited = set()
    def is_complete(state):
        return state == goal

    def is_consistent(state, path):
        return state not in path

    def recursive_backtracking(assignment, depth):
        expansions[0] += 1
        current = assignment[-1]
        if depth > max_depth:
            return None
        
        if is_complete(assignment[-1]):
            return assignment

        for neighbor in get_neighbors(assignment[-1]):
            if is_consistent(neighbor, assignment):
                visited.add(neighbor)
                assignment.append(neighbor)

                result = recursive_backtracking(assignment, depth + 1)
                if result:
                    return result
                
                assignment.pop()
                visited.remove(neighbor)
        return None
    
    visited.add(start)
    result = recursive_backtracking([start], 0)
    return (result, expansions[0])

#Thuật toán backtracking dùng csp
def solve(initial_state=None):
    nodes_expanded = [0]
    max_depth = [0]
    path = []

    #flat_state = [num for row in initial_state for num in row]
    variables = [f"X{i+1}" for i in range(9)]
    #value_order = flat_state.copy()
    domains = {var: list(range(9)) for var in variables}

     # Xáo domain để có thứ tự ngẫu nhiên
    for var in domains:
        random.shuffle(domains[var])

    constraints = create_constraints()

    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints,
        'initial_assignment': {}
    }

    result = backtrack({}, 0, csp, nodes_expanded, max_depth, path)

    if result:
        solution_grid = [[0 for _ in range(3)] for _ in range(3)]
        for var, value in result.items():
            idx = int(var[1:]) - 1
            row, col = idx // 3, idx % 3
            solution_grid[row][col] = value

        return {
            'path': path,
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': solution_grid
        }
    else:
        return {
            'path': [],
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': None
        }

def create_constraints():
    constraints = []

    # Ràng buộc dọc (X1 với X4, X2-X5,...)
    top_bottom_pairs = [
        ('X1', 'X4'), ('X2', 'X5'), ('X3', 'X6'),
        ('X4', 'X7'), ('X5', 'X8')
    ]
    for top, bottom in top_bottom_pairs:
        constraints.append((top, bottom, lambda t, b: b == t + 3 and t != 0))

    # Ràng buộc ngang (X1-X2, X2-X3, X4-X5,...)
    left_right_pairs = [
        ('X1', 'X2'), ('X2', 'X3'),
        ('X4', 'X5'), ('X5', 'X6'),
        ('X7', 'X8')
    ]

    def create_left_right_constraint(left, right):
        return lambda l, r: r == l + 1 and l != 0
    
    for left, right in left_right_pairs:
        constraints.append((left, right, create_left_right_constraint(left, right)))

    return constraints

def is_consistent(var, value, assignment, csp):
    if value in assignment.values():
        return False

    temp_assignment = assignment.copy()
    temp_assignment[var] = value

    for constraint in csp['constraints']:
        if len(constraint) == 2:
            name, constraint_func = constraint
            if not constraint_func(temp_assignment):
                return False
        elif len(constraint) == 3:
            var1, var2, constraint_func = constraint
            if var1 in temp_assignment and var2 in temp_assignment:
                if not constraint_func(temp_assignment[var1], temp_assignment[var2]):
                    return False

    return True

def backtrack(assignment, index, csp, nodes_expanded, max_depth, path):
    nodes_expanded[0] += 1
    max_depth[0] = max(max_depth[0], len(assignment))

    if assignment:
        grid = [[None for _ in range(3)] for _ in range(3)]
        for var, value in assignment.items():
            idx = int(var[1:]) - 1
            row, col = divmod(idx, 3)
            grid[row][col] = value
        path.append(grid)

    if index == len(csp['variables']):
        final_state = tuple(assignment[f"X{i+1}"] for i in range(9))
        return assignment if is_solvable(final_state) else None

    var = csp['variables'][index]

    for value in csp['domains'][var]:
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value
            result = backtrack(assignment, index + 1, csp, nodes_expanded, max_depth, path)
            if result:
                return result
            del assignment[var]
    return None
