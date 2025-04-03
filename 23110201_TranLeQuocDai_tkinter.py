import tkinter as tk
from tkinter import ttk
from collections import deque
import heapq
import threading
import random
from tkinter.scrolledtext import ScrolledText
import time
import csv

# nhóm 1: bfs, dfs, iddfs, ucs -> tìm kiếm không dùng heuristic
# nhóm 2: greedy, a*, ida* -> tìm kiếm dùng heuristic
# nhóm 3: Local search -> Hill Climbing:
                        # Simple hill Climbing (leo đồi đơn giản)

# ============ Các hàm giải thuật  ============
def parse_puzzle_input(input_str):
    parts = input_str.strip().split(',')
    return tuple(int(x) for x in parts)

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

def manhattan_distance(state, goal):
    dist = 0
    for i, val in enumerate(state):
        if val != 0:
            goal_index = goal.index(val)
            row_s, col_s = divmod(i, 3)
            row_g, col_g = divmod(goal_index, 3)
            dist += abs(row_s - row_g) + abs(col_s - col_g)
    return dist

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

def simple_hill_climbing(start, goal):
    def evaluate(state):
        dist = 0
        for i, val in enumerate(state):
            if val != 0:
                goal_index = goal.index(val)
                row_s, col_s = divmod(i, 3)
                row_g, col_g = divmod(goal_index, 3)
                dist += abs(row_s - row_g) + abs(col_s - col_g)
        return dist
    current_state = start
    path = [start]  # Thêm path để ghi lại đường đi
    expansions = 0
    while True:
        expansions += 1
        neighbors = get_neighbors(current_state)
        next_state = None
        for neighbor in neighbors:
            if evaluate(neighbor) < evaluate(current_state):
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
    def evaluate(state):
        dist = 0
        for i, val in enumerate(state):
            if val != 0:
                goal_index = goal.index(val)
                row_s, col_s = divmod(i, 3)
                row_g, col_g = divmod(goal_index, 3)
                dist += abs(row_s - row_g) + abs(col_s - col_g)
        return dist
    
    current_state = start
    path = [start]  # Thêm path để ghi lại đường đi
    expansions = 0

    while True:
        expansions += 1
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_score = evaluate(current_state)
        
        for neighbor in neighbors:
            score = evaluate(neighbor)
            if score < best_score:
                best_score = score
                best_neighbor = neighbor

        if best_neighbor is None or best_score >= evaluate(current_state):
            break
        current_state = best_neighbor
        path.append(current_state)  # Ghi lại trạng thái mới
        if current_state == goal:
            return path, expansions  # Trả về path thay vì chỉ current_state
    return None, expansions

# ============ 8-Puzzle App =============
class PuzzleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle - Trần Lê Quốc Đại - 23110201")
        self.geometry("1200x650")
        self.configure(bg="#F0F4F8")

        self.start_state = None
        self.goal_state = None
        self.solution_path = []
        self.current_step = 0
        self.playing = False
        self.paused = False
        self.is_running = False  # Theo dõi trạng thái chạy
        self.current_thread = None  # Lưu thread hiện tại

        # Thiết lập style cho giao diện
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12, "bold"), background="#F0F4F8")
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill="both")

        # Phần trái: Điều khiển
        self.setup_left_frame(main_frame)
        
        # Phần giữa: Bảng puzzle
        self.setup_center_frame(main_frame)
        
        # Phần phải: Log
        self.setup_right_frame(main_frame)

    def setup_left_frame(self, main_frame):
        left_frame = ttk.Frame(main_frame, width=350)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        # Box nhập ma trận
        input_box = ttk.LabelFrame(left_frame, text="Nhập Ma Trận", padding=10)
        input_box.pack(fill="x", pady=(0, 10))
        
        self.start_matrix = self.create_matrix(input_box, "Initial State:", 0)
        self.goal_matrix = self.create_matrix(input_box, "Goal State:", 1, [[1,2,3], [4,5,6], [7,8,0]])

        # Box kết quả
        results_box = ttk.LabelFrame(left_frame, text="Kết Quả Thuật Toán", padding=10)
        results_box.pack(fill="x", pady=(0, 10))
        
        self.status_table = ttk.Treeview(results_box, columns=("Algorithm", "Time", "Expansions"), show="headings", height=5)
        self.status_table.heading("Algorithm", text="Algorithm")
        self.status_table.heading("Time", text="Time (s)")
        self.status_table.heading("Expansions", text="Expansions")
        for col in ["Algorithm", "Time", "Expansions"]:
            self.status_table.column(col, width=110, anchor="center")
            self.status_table.heading(col, command=lambda c=col: self.sort_treeview_column(c, False))
        self.status_table.pack(fill="x")

        # Box điều khiển
        controls_box = ttk.LabelFrame(left_frame, text="Điều Khiển", padding=10)
        controls_box.pack(fill="x", pady=(0, 10))

        self.algo_var = tk.StringVar(value="BFS")
        ttk.Label(controls_box, text="ALGORITHMS:").pack(anchor="w")
        ttk.Combobox(controls_box, textvariable=self.algo_var, values=["BFS", "DFS", "UCS", "Greedy", "IDDFS", "A*", "IDA*", "Simple Hill Climbing", "Steepest-ascent Climbing"], state="readonly").pack(fill="x", pady=5)

        btn_frame = ttk.Frame(controls_box)
        btn_frame.pack(fill="x")
        # Khai báo và lưu tham chiếu đến các nút LOAD và RUN
        self.load_button = ttk.Button(btn_frame, text="LOAD", command=self.on_load_clicked)
        self.load_button.pack(side="left", padx=2)
        self.run_button = ttk.Button(btn_frame, text="RUN", command=self.on_run_clicked)
        self.run_button.pack(side="left", padx=2)
        ttk.Button(btn_frame, text="RANDOM", command=self.on_random_clicked).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="CLEAR", command=self.clear_table).pack(side="left", padx=2)

        ttk.Label(controls_box, text="Speed:").pack(anchor="w", pady=(5, 0))
        self.speed_scale = ttk.Scale(controls_box, from_=0.1, to=3.0, value=1.0, orient=tk.HORIZONTAL)
        self.speed_scale.pack(fill="x")

        action_frame = ttk.Frame(controls_box)
        action_frame.pack(fill="x", pady=5)
        ttk.Button(action_frame, text="RESET", command=self.on_reset_clicked).pack(side="left", padx=2)
        self.pause_button = ttk.Button(action_frame, text="PAUSE", command=self.on_pause_clicked)
        self.pause_button.pack(side="left", padx=2)

        ttk.Button(controls_box, text="EXIT", command=self.on_exit_clicked).pack(side="left", pady=(5, 0))
        ttk.Button(controls_box, text="EXPORT", command=self.export_to_file).pack(side="left", padx=5)

    def create_matrix(self, parent, label, col, default=None):
        ttk.Label(parent, text=label).grid(row=0, column=col, pady=(0, 5))
        frame = ttk.Frame(parent)
        frame.grid(row=1, column=col, padx=10)
        matrix = []
        for r in range(3):
            row = []
            for c in range(3):
                e = ttk.Entry(frame, width=3, justify="center", font=("Arial", 12))
                e.grid(row=r, column=c, padx=2, pady=2)
                if default:
                    e.insert(0, str(default[r][c]))
                row.append(e)
            matrix.append(row)
        return matrix

    def setup_center_frame(self, main_frame):
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(side="left", expand=True, fill="both", padx=10)

        board_box = ttk.LabelFrame(center_frame, text="Bảng Puzzle", padding=10)
        board_box.pack(expand=True, fill="both")
        
        self.puzzle_inner = ttk.Frame(board_box)
        self.puzzle_inner.place(relx=0.5, rely=0.5, anchor="center")
        self.tiles = []
        for r in range(3):
            row_tiles = []
            for c in range(3):
                lbl = tk.Label(self.puzzle_inner, text="", font=("Arial", 20), width=4, height=2, bg="#FFFFFF", borderwidth=2, relief="groove")
                lbl.grid(row=r, column=c, padx=2, pady=2)
                row_tiles.append(lbl)
            self.tiles.append(row_tiles)

        self.status_box = tk.Text(center_frame, height=4, width=40, fg="blue", font=("Arial", 12), bg="#E8ECEF", relief="flat")
        self.status_box.pack(side="bottom", pady=10)
        self.status_box.config(state="disabled")

    def setup_right_frame(self, main_frame):
        right_frame = ttk.Frame(main_frame, width=300)
        right_frame.pack(side="left", fill="both", padx=(10, 0))
        
        log_box = ttk.LabelFrame(right_frame, text="Log", padding=10)
        log_box.pack(expand=True, fill="both")
        self.log_box = ScrolledText(log_box, width=40, height=20, font=("Arial", 12), bg="#E8ECEF", relief="flat")
        self.log_box.pack(expand=True, fill="both")
        self.log_box.config(state="disabled")

    # ---------- Hàm sắp xếp cột trong bảng treeview ----------
    def sort_treeview_column(self, col, reverse):
        items = [(self.status_table.set(k, col), k) for k in self.status_table.get_children('')]
        if col in ("Time", "Expansions"):
            items.sort(key=lambda t: float(t[0]), reverse=reverse)
        else:
            items.sort(reverse=reverse)
        for index, (val, k) in enumerate(items):
            self.status_table.move(k, '', index)
        self.status_table.heading(col, command=lambda: self.sort_treeview_column(col, not reverse))

    def clear_table(self):
        for item in self.status_table.get_children():
            self.status_table.delete(item)

    def export_to_file(self):
        file_name = "algorithm_results.csv"
        try:
            with open(file_name, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Start", "Goal", "Algorithm", "Time (s)", "Expansions"])
                for row_id in self.status_table.get_children():
                    algo, time_sec, expansions = self.status_table.item(row_id)["values"]
                    start_str = self.state_to_string(self.start_state)
                    goal_str = self.state_to_string(self.goal_state)
                    writer.writerow([start_str, goal_str, algo, time_sec, expansions])
            self.set_status(f"Đã xuất dữ liệu ra file '{file_name}'")
        except Exception as e:
            self.set_status(f"Lỗi khi xuất file: {e}")

    def read_3x3_matrix(self, matrix_3x3):
        vals = []
        for r in range(3):
            for c in range(3):
                text = matrix_3x3[r][c].get().strip()
                if text == "":
                    text = "0"
                vals.append(int(text))
        return tuple(vals)
    
    def on_load_clicked(self):
        if self.is_running:  # Nếu thuật toán đang chạy, không cho phép LOAD
            self.set_status("Không thể LOAD khi thuật toán đang chạy. Vui lòng RESET hoặc chờ hoàn tất.")
            return
        try:
            self.start_state = self.read_3x3_matrix(self.start_matrix)
            self.goal_state = self.read_3x3_matrix(self.goal_matrix)
        except Exception as e:
            self.set_status(f"Lỗi: {e}")
            return
        self.display_state(self.start_state)
        self.set_status("Đã LOAD ma trận START và GOAL.")
    
    def on_run_clicked(self):
        if self.is_running:
            self.set_status("Không thể RUN khi thuật toán đang chạy. Vui lòng RESET hoặc chờ hoàn tất.")
            return
        if not self.start_state or not self.goal_state:
            self.set_status("Hãy LOAD trước khi RUN.")
            return
        self.solution_path = []
        self.current_step = 0
        self.playing = True
        self.is_running = True
        self.load_button.config(state="disabled")  # Vô hiệu hóa nút LOAD
        self.run_button.config(state="disabled")  # Vô hiệu hóa nút RUN
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")
        self.current_thread = threading.Thread(target=self.run_search)
        self.current_thread.start()
    
    def on_reset_clicked(self):
        self.playing = False
        self.paused = False
        self.is_running = False
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread = None
        self.load_button.config(state="normal")
        self.run_button.config(state="normal")
        self.current_step = 0
        self.solution_path = []
        for row in self.start_matrix:
            for e in row:
                e.delete(0, tk.END)
        for row in self.tiles:
            for lbl in row:
                lbl.config(text="")
        # Xóa nội dung bảng so sánh
        self.clear_table()
        # Xóa nội dung trong Log box
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")
        self.set_status("Đã RESET.")
    
    def on_random_clicked(self):
        arr = list(range(9))
        def is_solvable(state_list):
                inv = 0
                a = [x for x in state_list if x != 0]
                for i in range(len(a)):
                    for j in range(i+1, len(a)):
                        if a[i] > a[j]:
                            inv += 1
                return inv % 2 == 0
        while True:
            random.shuffle(arr)
            if is_solvable(arr):
                break
        self.start_state = tuple(arr)
        for r in range(3):
            for c in range(3):
                index = r * 3 + c
                self.start_matrix[r][c].delete(0, tk.END)
                self.start_matrix[r][c].insert(0, str(arr[index]))
        self.display_state(self.start_state)
        # Xóa bảng Kết Quả Thuật Toán
        self.clear_table()
        self.set_status("Đã RANDOM ma trận START.")
    
    def on_pause_clicked(self):
        if not self.playing:
            self.set_status("Không có mô phỏng chạy.")
            return
        self.paused = not self.paused
        self.pause_button.config(text="RESUME" if self.paused else "PAUSE")
        if not self.paused:
            self.animate_solution()
    
    def on_exit_clicked(self):
        self.destroy()
    
    def run_search(self):
        self.set_status("Đang tìm lời giải...")
        algo = self.algo_var.get()
        start_time = time.perf_counter()
    
        if algo == "BFS":
            path, expansions = bfs(self.start_state, self.goal_state)
        elif algo == "DFS":
            path, expansions = dfs(self.start_state, self.goal_state)
        elif algo == "UCS":
            path, expansions = ucs(self.start_state, self.goal_state)
        elif algo == "Greedy":
            path, expansions = greedy_search(self.start_state, self.goal_state)
        elif algo == "IDDFS":
            path, expansions = iddfs(self.start_state, self.goal_state)
        elif algo == "A*":
            path, expansions = a_star(self.start_state, self.goal_state)
        elif algo == "IDA*":
            path, expansions = ida_star(self.start_state, self.goal_state)
        elif algo == "Simple Hill Climbing":
            path, expansions = simple_hill_climbing(self.start_state, self.goal_state)
        elif algo == "Steepest-ascent Climbing":
            path, expansions = steepest_ascent_hill_climbing(self.start_state, self.goal_state)
        else:
            path, expansions = None, 0
    
        end_time = time.perf_counter()
        duration = end_time - start_time
    
        if not path:
            self.playing = False
            self.is_running = False
            self.load_button.config(state="normal")  # Kích hoạt lại nút LOAD
            self.run_button.config(state="normal")  # Kích hoạt lại nút RUN
            self.set_status("Không tìm thấy lời giải.")
        else:
            self.solution_path = path
            num_steps = len(path) - 1
            status_msg = f"Tìm thấy {num_steps} bước.\nThời gian: {duration:.4f}s\nExpansions: {expansions}"
            self.set_status(status_msg)
            self.status_table.insert("", "end", values=(self.algo_var.get(), f"{duration:.4f}", expansions))
            self.log_box.config(state="normal")
            self.log_box.insert("1.0", status_msg + "\n")
            self.log_box.config(state="disabled")
            self.animate_solution()
    
    def animate_solution(self):
        if not self.playing or self.paused:
            return
        if self.current_step < len(self.solution_path):
            state = self.solution_path[self.current_step]
            self.display_state(state)
            self.log_box.config(state="normal")
            self.log_box.insert(tk.END, f"Bước {self.current_step}:\n{self.state_to_string(state)}\n\n")
            self.log_box.config(state="disabled")
            self.current_step += 1
            delay = 1.0 / self.speed_scale.get()
            self.after(int(delay * 1000), self.animate_solution)
        else:
            self.playing = False
            self.is_running = False
            self.load_button.config(state="normal")  # Kích hoạt lại nút LOAD
            self.run_button.config(state="normal")  # Kích hoạt lại nút RUN
            self.set_status("Đã mô phỏng xong.")
    
    def display_state(self, state):
        for i, val in enumerate(state):
            r, c = divmod(i, 3)
            self.tiles[r][c].config(text=str(val) if val != 0 else "")
    
    def set_status(self, msg):
        self.status_box.config(state="normal")
        self.status_box.delete("1.0", tk.END)
        self.status_box.insert(tk.END, msg)
        self.status_box.config(state="disabled")
    
    def state_to_string(self, state):
        lines = []
        for i in range(0, 9, 3):
            row = state[i:i+3]
            row_str = " ".join(str(x) if x != 0 else "_" for x in row)
            lines.append(row_str)
        return "\n".join(lines)
 

if __name__ == "__main__":
    app = PuzzleApp()
    app.mainloop()