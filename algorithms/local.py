from .helpers import manhattan_distance, get_neighbors
import random
import math
 
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