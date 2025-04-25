from .helpers import manhattan_distance, get_neighbors
import heapq

def greedy_search(start, goal):
    if start == goal:
        return [start], 0
    visited = set([start])
    heap = [(manhattan_distance(start, goal), start, [start])]
    expansions = 0
    while heap:
        expansions += 1
        h, current, path = heapq.heappop(heap)
        if current == goal:
            return path, expansions
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                h_neighbor = manhattan_distance(neighbor, goal)
                heapq.heappush(heap, (h_neighbor, neighbor, path + [neighbor]))
    return None, expansions 

def a_star(start, goal):
    if start == goal:
        return [start], 0
    open_set = []
    heapq.heappush(open_set, (0 + manhattan_distance(start, goal), 0, start, [start]))
    visited = set()
    expansions = 0
    while open_set:
        f, g, current_state, path = heapq.heappop(open_set)
        expansions += 1
        if current_state == goal:
            return path, expansions
        if current_state in visited:
            continue
        visited.add(current_state)
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                new_g = g + 1
                h = manhattan_distance(neighbor, goal)
                new_f = new_g + h
                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))
    return None, expansions

def ida_star(start, goal):
    def search(path, g, threshold):
        current_state = path[-1]
        f = g + manhattan_distance(current_state, goal)
        if f > threshold:
            return f, None
        if current_state == goal:
            return f, path
        min_threshold = float('inf')
        expansions[0] += 1
        for neighbor in get_neighbors(current_state):
            if neighbor not in path:
                path.append(neighbor)
                new_f, result = search(path, g + 1, threshold)
                if result is not None:
                    return new_f, result
                if new_f < min_threshold:
                    min_threshold = new_f
                path.pop()
        return min_threshold, None
    if start == goal:
        return [start], 0
    threshold = manhattan_distance(start, goal)
    path = [start]
    expansions = [0]
    while True:
        new_threshold, result = search(path, 0, threshold)
        if result is not None:
            return result, expansions[0]
        if new_threshold == float('inf'):
            return None, expansions[0]
        threshold = new_threshold

def beam_search(start, goal, beam_width=2):
    # def evaluate(state):
    #     # Hàm đánh giá: Khoảng cách Manhattan
    #     dist = 0
    #     for i, val in enumerate(state):
    #         if val != 0:  # Bỏ qua ô trống
    #             goal_index = goal.index(val)
    #             row_s, col_s = divmod(i, 3)
    #             row_g, col_g = divmod(goal_index, 3)
    #             dist += abs(row_s - row_g) + abs(col_s - col_g)
    #     return dist

    # Khởi tạo
    current_states = [(start, [start])]  # Danh sách trạng thái hiện tại (state, path)
    expansions = 0

    while current_states:
        expansions += 1
        all_neighbors = []

        # Sinh tất cả các trạng thái lân cận
        for state, path in current_states:
            for neighbor in get_neighbors(state):
                if neighbor not in path:  # Tránh lặp lại trạng thái trong đường đi
                    all_neighbors.append((neighbor, path + [neighbor]))

        # Nếu không có trạng thái lân cận, dừng lại
        if not all_neighbors:
            break

        # Sắp xếp các trạng thái lân cận theo giá trị heuristic
        all_neighbors.sort(key=lambda x: manhattan_distance(x[0]))

        # Giữ lại beam_width trạng thái tốt nhất
        current_states = all_neighbors[:beam_width]

        # Kiểm tra nếu tìm thấy trạng thái mục tiêu
        for state, path in current_states:
            if state == goal:
                return path, expansions

    return None, expansions  # Không tìm thấy lời giải