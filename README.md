# 🧩 8-Puzzle Visualizer

## 🧠 Giới thiệu

**8-Puzzle Visualizer** là một ứng dụng viết bằng Python nhằm mô phỏng các thuật toán Trí tuệ nhân tạo (AI) để giải bài toán 8-puzzle kinh điển. Chương trình cung cấp giao diện người dùng trực quan (GUI) giúp hiển thị trực tiếp cách các thuật toán tìm kiếm và giải quyết bài toán qua từng bước. Hệ thống hỗ trợ các loại thuật toán tìm kiếm mù, có thông tin và tìm kiếm cục bộ.

---

## ⚙️ Tính năng

### ✅ Thuật toán được hỗ trợ:

- **Tìm kiếm không sử dụng heuristic (Uninformed Search):**
  - Breadth-First Search (BFS) – Tìm kiếm theo chiều rộng
  - Depth-First Search (DFS) – Tìm kiếm theo chiều sâu
  - Uniform Cost Search (UCS) – Tìm kiếm theo chi phí đều
  - Iterative Deepening Search (IDDFS) – Tìm kiếm sâu dần

- **Tìm kiếm có sử dụng heuristic (Informed Search):**
  - Greedy Best-First Search – Tìm kiếm tham lam
  - A* Search – Thuật toán A sao
  - Iterative Deepening A* (IDA*) – A* sâu dần
  - Beam Search – Tìm kiếm chùm

- **Tìm kiếm cục bộ (Local Search):**
  - Simple Hill Climbing – Leo đồi đơn giản
  - Steepest-ascent Climbing – Leo đồi dốc nhất
  - Stochastic Hill Climbing – Leo đồi ngẫu nhiên
  - Simulated Annealing – Mô phỏng luyện kim

- **Khác:**
  - AND-OR Search – Tìm kiếm điều kiện rẽ nhánh
  - Genetic Algorithm – Giải thuật di truyền

---

### 🖥️ Tính năng giao diện (GUI):

- Giao diện hiện đại, dễ sử dụng được xây dựng bằng `Tkinter`.
- Hình ảnh hóa trực quan trạng thái và chuyển động của puzzle.
- Mô phỏng lời giải từng bước, có thể điều chỉnh tốc độ.
- Sinh trạng thái khởi đầu ngẫu nhiên hợp lệ.
- Cho phép chạy giải thuật từng bước (step-by-step).
- Ghi log và hiển thị đường đi lời giải đầy đủ.

---

## 👤 Tác giả

- Trần Lê Quốc Đại – 23110201
- Dự án phục vụ học phần **Trí Tuệ Nhân Tạo - Kỳ 2 Năm 2**

---
## 📌 Mô phỏng các thuật toán tìm kiếm 8-Puzzle
### 🔍 BFS
![BFS](gif/BFS.gif)

### 🔍 DFS
![DFS](gif/DFS.gif)

### 🔍 UCS
![UCS](gif/UCS.gif)

### 🔍 IDDFS
![IDDFS](gif/IDDFS.gif)

### 🔍 A*
![A*](gif/A_STAR.gif)

### 🔍 IDA*
![IDA*](gif/IDA_STAR.gif)

### 🔍 Greedy Best First Search
![Greedy](gif/GREEDY.gif)

### 🔍 Simple Hill Climbing
![Simple Hill Climbing](gif/SIMPLE_CLIMBING.gif)

### 🔍 Steepest Ascent Hill Climbing
![Steepest Climbing](gif/STEEPEST_CLIMBING.gif)

### 🔍 BEAM SEARCH
![Beam Search](gif/BEAM_SEARCH.gif)

### 🔍 Genetic Algorithm
![Genetic Algorithm](gif/GENETIC.gif)

### 🔍 And-Or Search
![And-Or Search](gif/AND_OR.gif)

### 🔍 Sensorless Search
![Sensorless Search](gif/SENSORLESS.gif)

