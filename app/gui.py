import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time
import csv
import math
import threading
import random
from itertools import permutations

from algorithms.belief_state import apply_action_belief

from algorithms.helpers import apply_action, is_solvable, generate_belief_with_123_top_and_zero_center

from algorithms.uninformed import bfs, dfs, iddfs, ucs, backtracking_search
from algorithms.informed import greedy_search, a_star, ida_star, beam_search
from algorithms.local import simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, simulated_annealing
from algorithms.and_or import and_or_search
from algorithms.belief_state import sensorless_search, belief_bfs
from algorithms.evolutionary import genetic_algorithm
from algorithms.constraint import solve, ac3, create_constraints, backtrack, solve_with_ac3, solve_trial_and_error
from algorithms.evolutionary import genetic_algorithm
from algorithms.q_learning import q_learning
class PuzzleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle - Trần Lê Quốc Đại - 23110201")
        self.geometry("1200x650")
        self.configure(bg="#F0F4F8")

        self.start_state = None
        self.goal_state = None
        self.belief_start_list = []  # bao gồm start_matrix và các matrix được thêm
        self.belief_goal_list = []   # bao gồm goal_matrix và các matrix được thêm
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
        input_box.pack(fill="both", pady=(0, 10)) # fill là both để khung ko bị nhỏ
        
        # Tạo Canvas và Scrollbar bên trong input_box
        canvas = tk.Canvas(input_box, height=200, width=440)  # Đặt chiều cao cố định
        scrollbar = ttk.Scrollbar(input_box, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Khung nội dung bên trong Canvas
        input_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=input_frame, anchor="nw")

        # Cập nhật scrollregion khi kích thước thay đổi
        def configure_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        input_frame.bind("<Configure>", configure_scrollregion)

        # Đặt Canvas và Scrollbar trong input_box
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Khu vực cho START
        start_box = ttk.LabelFrame(input_frame, text="Initial State", padding=10)
        start_box.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.start_matrix = self.create_matrix(start_box, "Initial State:", 0)
        self.belief_start_list.append(self.start_matrix)
        ttk.Button(start_box, text="+ Thêm trạng thái START", command=lambda: self.add_belief_matrix(start_box, self.belief_start_list)).grid(row=2, column=0, pady=5)

        # Khu vực cho GOAL
        goal_box = ttk.LabelFrame(input_frame, text="Goal State", padding=10)
        goal_box.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.goal_matrix = self.create_matrix(goal_box, "Goal State:", 0, [[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.belief_goal_list.append(self.goal_matrix)
        ttk.Button(goal_box, text="+ Thêm trạng thái GOAL", command=lambda: self.add_belief_matrix(goal_box, self.belief_goal_list)).grid(row=2, column=0, pady=5)


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
        ttk.Combobox(controls_box, textvariable=self.algo_var, values=[
            "--- Tìm kiếm không có thông tin ---",
            "BFS",
            "DFS",
            "UCS",
            "IDDFS",
            "--- Tìm kiếm có thông tin ---",
            "Greedy",  
            "A*",
            "IDA*",
            "--- Tìm kiếm có ràng buộc ---",
            "Backtracking AC-3",
            "Backtracking CSP",
            "Trial and Error",
            "--- Tìm kiếm cục bộ ---",
            "Simple Hill Climbing",
            "Steepest-ascent Climbing",
            "Stochastic Hill Climbing",
            "Simulated Annealing",
            "Beam Search",
            "Genetic Algorithm",
            "--- Tìm kiếm môi trường phức tạp ---",
            "AND-OR Search", 
            "Sensorless Search ~ Search with No Observation",
            "Belief-State BFS ~ Search with Partial Observation",
            "--- Học củng cố ---",
            "Q-Learning",
        ], state="readonly").pack(fill="x", pady=5)


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
        # Thêm nhãn cho ma trận
        ttk.Label(parent, text=label).grid(row=0, column=col, pady=(0, 5))

        # Tạo khung chứa ma trận
        frame = ttk.Frame(parent)
        frame.grid(row=1, column=col, padx=35, pady=5, sticky="nsew") # Thêm sticky để căn giữa
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
    def add_belief_matrix(self, parent, target_list):
        # Tính toán row dựa trên số lượng ma trận hiện có
        current_row = parent.grid_size()[1]  # Lấy số hàng hiện tại trong grid của parent
        container = ttk.Frame(parent)
        container.grid(row=current_row, column=0, pady=4, sticky="w")  # Sử dụng row động
        matrix = []
        for r in range(3):
            row = []
            for c in range(3):
                e = ttk.Entry(container, width=3, font=("Arial", 11), justify="center")
                e.grid(row=r, column=c, padx=1, pady=1)
                row.append(e)
            matrix.append(row)
        # Nút xóa sử dụng grid
        del_btn = ttk.Button(container, text="Xóa", command=lambda: self.remove_belief_matrix(container, matrix, target_list))
        del_btn.grid(row=0, column=3, rowspan=3, padx=5)
        target_list.append(matrix)
    def remove_belief_matrix(self, container, matrix, target_list):
        container.destroy()
        target_list.remove(matrix)

    def read_all_beliefs(self, matrix_list):
        result = []
        for mat in matrix_list:
            grid = []
            for row in mat:
                row_vals = []
                for e in row:
                    try:
                        v = e.get().strip()
                        val = int(v) if v else 0
                        row_vals.append(val)
                    except ValueError:
                        row_vals.append(0)  # Nếu nhập ký tự không hợp lệ, thay bằng 0
                grid.append(tuple(row_vals))
            # Kiểm tra đủ 3 hàng 3 cột
            if len(grid) == 3 and all(len(r) == 3 for r in grid):
                result.append(tuple(grid))
        return result
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
        algo = self.algo_var.get()
        if algo not in ["Sensorless Search ~ Search with No Observation", "Belief-State BFS ~ Search with Partial Observation"] and (not self.start_state or not self.goal_state):
            self.set_status("Hãy LOAD trước khi RUN hoặc NHẬP đầy đủ.")
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

        # Xóa nội dung trong Log Box
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")

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
    
    def get_belief_states(self):
        """
        Đọc tất cả các ma trận từ belief_start_list và belief_goal_list.
        Trả về tập hợp các trạng thái đầu vào và trạng thái mục tiêu.
        """
        start_belief = set(self.read_all_beliefs(self.belief_start_list))
        goal_belief = set(self.read_all_beliefs(self.belief_goal_list))
        return start_belief, goal_belief

    def run_search(self):
        self.set_status("Đang tìm lời giải...")
        algo = self.algo_var.get()

        if algo.startswith("---"):
            self.set_status("Vui lòng chọn một thuật toán hợp lệ.")
            self.is_running = False
            self.load_button.config(state="normal")
            self.run_button.config(state="normal")
            return

        # Lấy tất cả trạng thái đầu vào và mục tiêu
        start_set, goal_set = self.get_belief_states()
        if not start_set or not goal_set:
            self.set_status("Hãy LOAD trước khi RUN hoặc NHẬP đầy đủ.")
            self.is_running = False
            self.load_button.config(state="normal")
            self.run_button.config(state="normal")
            return

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
        # elif algo == "Backtracking":
        #     path, expansions = backtracking_search(self.start_state, self.goal_state)
        elif algo == "Backtracking CSP":
            start_time = time.perf_counter()
            path, costs, _ = self.adapt_backtracking([[0]*3 for _ in range(3)], self.goal_state)
            duration = time.perf_counter() - start_time

            if path:
                # Thiết lập cho animate
                self.solution_path = path
                self.current_step = 0
                self.playing = True
                self.paused = False

                # Cập nhật bảng kết quả
                expansions = len(path)
                self.status_table.insert("", "end", values=(algo, f"{duration:.4f}", expansions))
                self.set_status(
                    f"Đã sinh trạng thái hợp lệ bằng CSP.\n"
                    f"Thời gian: {duration:.4f}s\n"
                    f"Expansions: {expansions}"
                )

                # Bắt đầu animate: board + log
                self.animate_solution()
            else:
                self.set_status("Không thể sinh trạng thái hợp lệ.")

            return

        elif algo == "A*":
            path, expansions = a_star(self.start_state, self.goal_state)
        elif algo == "IDA*":
            path, expansions = ida_star(self.start_state, self.goal_state)
        elif algo == "Simple Hill Climbing":
            path, expansions = simple_hill_climbing(self.start_state, self.goal_state)
        elif algo == "Steepest-ascent Climbing":
            path, expansions = steepest_ascent_hill_climbing(self.start_state, self.goal_state)
        elif algo == "Stochastic Hill Climbing":
            path, expansions = stochastic_hill_climbing(self.start_state, self.goal_state)
        elif algo == "Simulated Annealing":
            path, expansions = simulated_annealing(self.start_state, self.goal_state)
        elif algo == "Beam Search":
            path, expansions = beam_search(self.start_state, self.goal_state, beam_width=2)
        elif algo == "AND-OR Search":
            path, expansions = and_or_search(self.start_state, self.goal_state)
        elif algo == "Genetic Algorithm":
            path, expansions = genetic_algorithm(self.start_state, self.goal_state, log_callback=self.log_to_gui)
        elif algo == "Sensorless Search ~ Search with No Observation":
            # đọc về các belief ban đầu & goal đều là tuple-of-tuples (3×3)
            raw_starts = set(self.read_all_beliefs(self.belief_start_list))
            raw_goals  = set(self.read_all_beliefs(self.belief_goal_list))

            # gọi sensorless_search (nó sẽ flatten bên trong)
            actions, expansions = sensorless_search(raw_starts, raw_goals)

            if actions:
                path = None
                for s in raw_starts:
                    current = sum(s, ())  # flatten
                    temp_path = [current]
                    success = True
                    for move in actions:
                        current = apply_action(current, move)
                        if current is None:
                            success = False
                            break
                        temp_path.append(current)
                    if success and current in {sum(g, ()) for g in raw_goals}:
                        path = temp_path
                        break

                if path is None:
                    # fallback nếu không có state nào match (hiếm khi xảy ra)
                    first_3x3 = next(iter(raw_starts))
                    current = sum(first_3x3, ())
                    path = [current]
                    for move in actions:
                        current = apply_action(current, move)
                        path.append(current)
            else:
                path = None
        elif algo == "Belief-State BFS ~ Search with Partial Observation":
            start_set = set(self.read_all_beliefs(self.belief_start_list))
            goal_set = set(self.read_all_beliefs(self.belief_goal_list))

            actions, expansions = belief_bfs(start_set, goal_set)

            if actions:
                # Tìm state ban đầu sao cho sau khi thực hiện actions sẽ match với 1 goal
                path = None
                for s in start_set:
                    current = s
                    temp_path = [current]
                    success = True
                    for move in actions:
                        current = apply_action_belief(current, move)
                        if current is None:
                            success = False
                            break
                        temp_path.append(current)
                    if success and current in goal_set:
                        path = temp_path
                        break

                if path is None:
                    # fallback nếu không state nào match goal
                    first_state = next(iter(start_set))
                    path = [first_state]
                    current = first_state
                    for move in actions:
                        new_state = apply_action_belief(current, move)
                        if new_state is None:
                            break
                        path.append(new_state)
            else:
                path = None
        elif algo == "Backtracking AC-3":
            start_time = time.perf_counter()
            path, costs, all_paths, arc_count = self.adapt_backtracking_ac3()
            duration = time.perf_counter() - start_time

            if path:
                self.solution_path = path
                self.current_step = 0
                self.playing = True
                self.paused = False

                expansions = len(path)
                self.status_table.insert("", "end", values=(algo, f"{duration:.4f}", expansions))
                self.set_status(
                    f"AC-3 + Backtrack đã tạo ra trạng thái hợp lệ.\n"
                    f"Thời gian: {duration:.4f}s\n"
                    f"Expansions: {expansions}\n"
                    f"Arc Processed: {arc_count}"
                )

                self.animate_solution()
            else:
                self.set_status("Không thể sinh trạng thái hợp lệ bằng AC-3.")
            return
        elif algo == "Trial and Error":
            start_time = time.perf_counter()
            path, expansions, depth = solve_trial_and_error()
            duration = time.perf_counter() - start_time

            if path:
                self.solution_path = path
                self.current_step = 0
                self.playing = True
                self.paused = False

                self.status_table.insert("", "end", values=(algo, f"{duration:.4f}", expansions))
                self.set_status(
                    f"Đã sinh trạng thái hợp lệ bằng Trial and Error.\n"
                    f"Thời gian: {duration:.4f}s\n"
                    f"Expansions: {expansions}"
                )
                self.animate_solution()
            else:
                self.set_status("Không thể sinh trạng thái hợp lệ bằng Trial and Error.")

            return
        elif algo == "Q-Learning":
            start = self.start_state
            goal = self.goal_state

            path, expansions = q_learning(start, goal)

            if path:
                self.solution_path = path
                self.current_step = 0
                self.playing = True
                self.paused = False

                self.status_table.insert("", "end", values=(algo, f"{len(path) * 0.001:.4f}", expansions))
                self.set_status(
                    f"Q-Learning đã tìm thấy đường đi.\n"
                    f"Chiều dài đường đi: {len(path)} bước\n"
                    f"Expansions: {expansions}"
                )

                self.animate_solution()
            else:
                self.set_status("Q-Learning không tìm thấy lời giải.")
            #return
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
    def log_to_gui(self, message):
        self.log_box.config(state="normal")         # MỞ ghi log
        self.log_box.insert(tk.END, message + '\n') # Ghi log
        self.log_box.see(tk.END)                    # Auto scroll
        self.log_box.config(state="disabled")   

    def display_state(self, state):
        flat_state = sum(state, ()) if isinstance(state[0], tuple) else state
        for i, val in enumerate(flat_state):
            r, c = divmod(i, 3)
            self.tiles[r][c].config(
                text=str(val) if val != 0 else "",
                font=("Arial", 20),
                width=4,
                height=2
            )
    
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
    def adapt_backtracking(self, initial_state, goal_state=None):
        from algorithms.constraint import solve
        # solve() trả về dict với 'path' là list các grid 3×3
        result = solve(initial_state)
        if not result["solution"]:
            return None, None, []

        # Flatten từng grid 3×3 thành tuple 9 phần tử
        flat_path = []
        for grid in result["path"]:
            flat = tuple(0 if cell is None else cell
                        for row in grid for cell in row)
            flat_path.append(flat)

        # Chi phí = chỉ số bước
        costs = list(range(len(flat_path)))

        # all_paths (nếu cần)
        all_paths = [(flat_path[:i+1], costs[i])
                    for i in range(len(flat_path))]

        return flat_path, costs, all_paths
    
    def adapt_backtracking_ac3(self, goal_state=None):
        from algorithms.constraint import solve_with_ac3

        result = solve_with_ac3()
        if not result["solution"]:
            return None, None, [], 0  # thêm 0 là arc_processed

        flat_path = []
        for grid in result["path"]:
            flat = tuple(0 if cell is None else cell
                        for row in grid for cell in row)
            flat_path.append(flat)

        costs = list(range(len(flat_path)))
        all_paths = [(flat_path[:i+1], costs[i]) for i in range(len(flat_path))]

        arc_count = result.get("arc_processed", 0)
        return flat_path, costs, all_paths, arc_count

