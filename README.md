# 🧩 8-Puzzle Visualizer

## 🧠 Giới thiệu

**8-Puzzle Visualizer** là ứng dụng được phát triển bằng Python với giao diện trực quan sử dụng `Tkinter`, nhằm mô phỏng quá trình hoạt động của các thuật toán Trí tuệ Nhân tạo trong việc giải bài toán 8-puzzle cổ điển. Ứng dụng hỗ trợ đa dạng thuật toán từ tìm kiếm không heuristic đến các kỹ thuật nâng cao như tìm kiếm niềm tin và giải thuật tiến hóa.

---

## ⚙️ Tính năng chính

### 🔎 Các nhóm thuật toán được hỗ trợ:

#### 📘 1. **Tìm kiếm không có thông tin (Uninformed Search):**
- Breadth-First Search (BFS) – Tìm kiếm theo chiều rộng
- Depth-First Search (DFS) – Tìm kiếm theo chiều sâu
- Uniform Cost Search (UCS) – Tìm kiếm chi phí đều
- Iterative Deepening DFS (IDDFS) – Tìm kiếm sâu dần

#### 📙 2. **Tìm kiếm có thông tin (Informed Search):**
- Greedy Best-First Search – Tìm kiếm tham lam
- A* Search – A sao
- IDA* – A* sâu dần

#### 📘 3. **Tìm kiếm có ràng buộc (Constraint Search):**
- Backtracking AC-3
- Backtracking CSP
- Trial and Error

#### 📕 4. **Tìm kiếm cục bộ (Local Search):**
- Simple Hill Climbing
- Steepest-ascent Climbing
- Stochastic Hill Climbing
- Simulated Annealing
- Beam Search
- Genetic Algorithm

#### 📒 5. **Tìm kiếm trong môi trường phức tạp:**
- AND-OR Search
- Sensorless Search ~ Search with No Observation
- Belief-State BFS ~ Search with Partial Observation

#### 📗 6. **Học củng cố (Reforcement Learning):**
- Q-Learning
---

## 🖥️ Giao diện người dùng (GUI)

- Giao diện hiện đại bằng Tkinter, dễ thao tác.
- Hình ảnh hóa từng bước di chuyển trong lời giải.
- Cho phép chọn giải thuật và chạy từng bước (step-by-step).
- Điều chỉnh tốc độ mô phỏng theo thanh trượt.
- Sinh ngẫu nhiên trạng thái ban đầu hợp lệ với lựa chọn độ khó.
- Xuất báo cáo kết quả chạy dưới dạng CSV.
- Log trực tiếp diễn tiến lời giải.

---

## 📂 Cấu trúc thư mục

```
PUZZLE_AI_MIDTERM/
├── algorithms/
│ ├── pycache/
│ ├── and_or.py
│ ├── belief_state.py
│ ├── constraint.py
│ ├── evolutionary.py
│ ├── helpers.py
│ ├── informed.py
│ ├── local.py
│ └── uninformed.py
├── app/
│ ├── pycache/
│ └── gui.py
├── gif/
│ └── *.gif
├── main.py
├── README.md
```

---

## 👤 Tác giả

- **Trần Lê Quốc Đại**  
- **MSSV:** 23110201  
- **Môn học:** Trí Tuệ Nhân Tạo  
- **Trường:** Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)  

---

## 📽️ Minh họa lời giải theo từng nhóm thuật toán

### 📘 Tìm kiếm không có thông tin
### 🔍 BFS
![BFS](gif/BFS.gif)
### 🔍 DFS
![DFS](gif/DFS.gif)
### 🔍 UCS
![UCS](gif/UCS.gif)
### 🔍 IDDFS
![IDDFS](gif/IDDFS.gif)

### 📙 Tìm kiếm có thông tin
### 🔍 GREEDY
![Greedy](gif/GREEDY.gif)
### 🔍 A_STAR
![A*](gif/A_STAR.gif)
### 🔍 IDA_STAR
![IDA*](gif/IDA_STAR.gif)

### 📘 Tìm kiếm có ràng buộc
### 🔍 BACKTRACKING AC3
![Backtracking AC3](gif/AC3.gif)
### 🔍 BACKTRACKING CSP
![Backtracking CSP](gif/CSP.gif)
### 🔍 TRIAL AND ERROR
![Trial and Error](gif/TRIAL.gif)

### 📕 Tìm kiếm cục bộ
### 🔍 SIMPLE HILL CLIMBING
![Simple Hill Climbing](gif/SIMPLE_CLIMBING.gif)
### 🔍 STEEPEST HILL CLIMBING
![Steepest Climbing](gif/STEEPEST_CLIMBING.gif)
### 🔍 STOCHASTIC HILL CLIMBING
![Stochastic Hill Climbing](gif/STOCHASTIC.gif)
### 🔍 SIMULATED ANNEALING
![Simulated Annealing](gif/SIMULATED.gif)
### 🔍 BEAM SEARCH
![Beam Search](gif/BEAM_SEARCH.gif)
### 🔍 GENETIC ALGORITHM
![Genetic Algorithm](gif/GENETIC.gif)

### 📒 Tìm kiếm trong môi trường phức tạp
### 🔍 SENSORLESS SEARCH
![Sensorless Search](gif/SENSORLESS.gif)
### 🔍 BELIEF-STATE BFS
![Belief-State BFS](gif/BELIEF_BFS.gif)
### 🔍 AND-OR SEARCH
![AND-OR Search](gif/AND_OR.gif)

### 📗 Học củng cố
### 🔍 Q-LEARNING
![Q-Learning](gif/Q_LEARNING.gif)

---

> © 2025 – Trần Lê Quốc Đại – HCMUTE
