from collections import deque
import random
from algorithms.helpers import is_solvable
#Thuật toán backtracking dùng csp, Không kiểm tra cung trước, chỉ duyệt giá trị từng biến trong quá trình backtrack ==> ko cần biến arc_count như ac3
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

def revise(csp, Xi, Xj):
    removed = False
    for x in csp['domains'][Xi][:]:
        funcs = [func for (var1, var2, func) in csp['constraints'] if var1 == Xi and var2 == Xj]
        if not funcs:
            continue
        func = funcs[0]
        if not any(func(x, y) for y in csp['domains'][Xj]):
            csp['domains'][Xi].remove(x)
            removed = True
    return removed

def ac3(csp, arc_count=None):
    """
    AC-3(csp, arc_count)
    - Trả về False nếu phát hiện domain trống (vô nghiệm).
    - Trả về True nếu enforce arc-consistency thành công.
    - Ghi lại số lượng cung (arc) đã xử lý nếu arc_count là list [0].
    """
    if arc_count is None:
        arc_count = [0]  # Cho phép không truyền cũng chạy được

    queue = deque((Xi, Xj) for (Xi, Xj, _) in csp['constraints'])

    while queue:
        Xi, Xj = queue.popleft()
        arc_count[0] += 1  # Đếm mỗi cung xử lý

        if revise(csp, Xi, Xj):
            if not csp['domains'][Xi]:
                return False
            neighbors = {var1 for (var1, var2, _) in csp['constraints']
                         if var2 == Xi and var1 != Xj}
            for Xk in neighbors:
                queue.append((Xk, Xi))
    return True


def solve_with_ac3():
    nodes_expanded = [0]
    max_depth = [0]
    path = []

    variables = [f"X{i+1}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}
    for var in domains:
        random.shuffle(domains[var])

    constraints = create_constraints()

    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints,
        'initial_assignment': {}
    }

    arc_count = [0]
    if not ac3(csp, arc_count):
        return {
            'path': [],
            'nodes_expanded': 0,
            'max_depth': 0,
            'solution': None,
            'arc_processed': arc_count[0]
        }

    # Shuffle lại các miền sau khi đã prune bằng AC-3
    for var in csp['domains']:
        random.shuffle(csp['domains'][var])
    # Bắt đầu backtrack
    # Chọn biến đầu tiên để gán giá trị
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
            'solution': solution_grid,
            'arc_processed': arc_count[0]
        }
    else:
        return {
            'path': [],
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': None,
            'arc_processed': arc_count[0]
        }

def solve_trial_and_error():
    import random
    from algorithms.helpers import is_solvable
    from collections import deque

    nodes_expanded = [0]
    max_depth = [0]
    path = []

    variables = [f"X{i+1}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}  # Không xáo trộn để giữ đúng nghĩa trial & error
    # Shuffle để tạo tính ngẫu nhiên
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

        # Chuyển path dạng 3x3 thành flat để GUI animate
        flat_path = []
        for grid in path:
            flat = tuple(0 if cell is None else cell for row in grid for cell in row)
            flat_path.append(flat)

        return flat_path, nodes_expanded[0], max_depth[0]

    else:
        return [], nodes_expanded[0], max_depth[0]