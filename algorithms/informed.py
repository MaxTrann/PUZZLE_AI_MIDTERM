from .helpers import manhattan_distance, get_neighbors
import heapq #min-heap: giá trị nhỏ nhất nằm ở root
import math
import random
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
    heapq.heappush(open_set, (0 + manhattan_distance(start, goal), 0, start, [start])) #(f, g, current_state, path)
    visited = set()
    expansions = 0
    while open_set:
        f, g, current_state, path = heapq.heappop(open_set)
        expansions += 1
        if current_state == goal:
            return path, expansions
        if current_state in visited: # nếu đã mở rộng thì bỏ qua 
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
    # Bước 2: đặt ngưỡng
    def search(path, g, threshold):
        current_state = path[-1]
        f = g + manhattan_distance(current_state, goal)
        if f > threshold: # Bước 4: bị cắt tỉa
            return f, None
        if current_state == goal: # Bước 5: trả về đường đi
            return f, path
        min_threshold = float('inf') # đặt ngưỡng
        expansions[0] += 1
        # Bước 3: mở rộng nút
        for neighbor in get_neighbors(current_state):
            if neighbor not in path:
                path.append(neighbor)
                new_f, result = search(path, g + 1, threshold)
                if result is not None: # Bước 6: cập nhật ngưỡng
                    return new_f, result
                if new_f < min_threshold:
                    min_threshold = new_f
                path.pop()
        return min_threshold, None
    # Bước 1: khởi tạo
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
        all_neighbors.sort(key=lambda x: manhattan_distance(x[0], goal)) # thêm goal

        # Giữ lại beam_width trạng thái tốt nhất
        current_states = all_neighbors[:beam_width]

        # Kiểm tra nếu tìm thấy trạng thái mục tiêu
        for state, path in current_states:
            if state == goal:
                return path, expansions

    return None, expansions  # Không tìm thấy lời giải

def simple_hill_climbing(start, goal):
    current_state = start
    path = [start]  # Thêm path để ghi lại đường đi
    expansions = 0
    while True:
        expansions += 1
        neighbors = get_neighbors(current_state)
        next_state = None
        for neighbor in neighbors:
            if manhattan_distance(neighbor) < manhattan_distance(current_state):
                next_state = neighbor
                break
        if next_state is None:
            break
        current_state = next_state
        path.append(current_state)  # Ghi lại trạng thái mới
        if current_state == goal:
            return path, expansions  # Trả về path thay vì chỉ current_state
    return None, expansions

def steepest_ascent_hill_climbing(start, goal):    
    current_state = start
    path = [start]  # Thêm path để ghi lại đường đi
    expansions = 0

    while True:
        expansions += 1
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_score = manhattan_distance(current_state)
        
        for neighbor in neighbors:
            score = manhattan_distance(neighbor)
            if score < best_score:
                best_score = score
                best_neighbor = neighbor

        if best_neighbor is None or best_score >= manhattan_distance(current_state):
            break
        current_state = best_neighbor
        path.append(current_state)  # Ghi lại trạng thái mới
        if current_state == goal:
            return path, expansions  # Trả về path thay vì chỉ current_state
    return None, expansions

def stochastic_hill_climbing(start, goal):
    current_state = start
    path = [start]  # Ghi lại đường đi
    expansions = 0

    while True:
        expansions += 1
        neighbors = get_neighbors(current_state)
        better_neighbors = []

        # Tìm các trạng thái lân cận tốt hơn
        for neighbor in neighbors:
            if manhattan_distance(neighbor) < manhattan_distance(current_state):
                better_neighbors.append(neighbor)

        if not better_neighbors:  # Không có trạng thái nào tốt hơn
            break

        # Chọn ngẫu nhiên một trạng thái tốt hơn
        current_state = random.choice(better_neighbors)
        path.append(current_state)

        if current_state == goal:  # Đạt trạng thái mục tiêu
            return path, expansions

    return None, expansions  # Không tìm thấy lời giải

def simulated_annealing(start, goal, initial_temp=1000, cooling_rate=0.99, min_temp=0.1):
    current_state = start
    current_eval = manhattan_distance(current_state)
    path = [start]  # Ghi lại đường đi
    expansions = 0
    temperature = initial_temp

    while temperature > min_temp:
        expansions += 1
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break

        # Chọn ngẫu nhiên một trạng thái lân cận
        next_state = random.choice(neighbors)
        next_eval = manhattan_distance(next_state)

        # Tính toán sự thay đổi giá trị heuristic
        delta_eval = next_eval - current_eval

        # Quyết định chấp nhận trạng thái mới
        if delta_eval < 0 or math.exp(-delta_eval / temperature) > random.random():
            current_state = next_state
            current_eval = next_eval
            path.append(current_state)

        # Giảm nhiệt độ
        temperature *= cooling_rate

        # Kiểm tra nếu đạt trạng thái mục tiêu
        if current_state == goal:
            return path, expansions

    return None, expansions  # Không tìm thấy lời giải