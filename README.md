# 🧩 8-Puzzle Visualizer

## 1. Mục tiêu

Dự án **8-Puzzle Visualizer** được phát triển với các mục tiêu chính như sau:
- 🧠 **Triển khai các thuật toán AI**: Áp dụng các thuật toán được học được học trong Trí tuệ Nhân tạo (AI) để giải bài toán 8-puzzle, bao gồm các phương pháp cơ bản (Breadth-First Search, Depth-First Search) đến nâng cao (A*, Genetic Problem, Q-Learning).
- 🧩 **Xây dựng giao diện trực quan**: Tạo một giao diện người dùng (GUI) sử dụng Tkinter, cho phép người dùng nhập trạng thái bắt đầu, kết thúc, chọn thuật toán và quan sát quá trình giải chi tiết, điều chỉnh tốc độ mô phỏng, xuất kết quả dưới dạng file csv. Giao diện được tối ưu để thân thiện và hỗ trợ tương tác với người dùng.
- 📊 **So sánh hiệu suất**: Đánh giá hiệu quả của thuật toán dựa trên thời gian chạy (tính bằng giây) và số lần mở rộng trạng thái (expansions) giúp hiểu rõ được ưu/nhược điểm của từng thuật toán sử dụng.
- 📚 **Hỗ trợ học tập**: Cung cấp một công cụ trực quan, dễ sử dụng để minh họa và phân tích cá thuật toán, phục vụ cho việc trực quan các thuật toán một cách dễ hiểu. Bài tập cá nhân cũng là một dự án giúp củng cố lý thuyết, kỹ năng lập trình, khả năng phân tích vấn đề.

---

## 2. Nội dung
Dự án **8-Puzzle Visualizer** triển khai bài toán 8-puzzle, một bài toán cổ điển trong Trí tuệ Nhân tạo, với mục tiêu sắp xếp các ô số từ trạng thái ban đầu về trạng thái mục tiêu thông qua việc di chuyển ô trống. Dự án tích hợp **sáu nhóm thuật toán** tìm kiếm, bao gồm:
- **Tìm kiếm có thông tin** (Informed Search): Các thuật toán sử dụng heuristic để hướng dẫn tìm kiếm một cách hiệu quả hơn.
- **Tìm kiếm không có thông tin** (Uninformed Search): Các thuật toán dựa trên khám phá mù, không sử dụng hàm thông tin heuristic.
- **Tìm kiếm có ràng buộc** (Constraint Satisfaction Problem): Các thuật toán giải bài toán bằng cách gán các giá trị thỏa mãn với các ràng buộc cho trước.
- **Tìm kiếm cục bộ** (Local Search): Các thuật toán cải thiện trạng thái dần dần dựa trên hàm đánh giá.
- **Tìm kiếm trong môi trường phức tạp** (Searching in complex environments): Các thuật toán xử lý các tình huống không xác định hoặc quan sát không đầy đủ.
- **Học tăng cường** (Reinforcement Learning): Các thuật toán học từ kinh nghiệm để tìm lời giải tối ưu.

Mỗi nhóm được trình bày chi tiết với:
- **Thành phần chính của bài toán**: Mô tả trạng thái, hành động, kiểm tra mục tiêu, và hàm heuristic (nếu có).
- **Lời giải**: Chuỗi trạng thái và hành động từ trạng thái ban đầu đến mục tiêu.
- **GIF minh họa**: Hình ảnh động thể hiện quá trình giải của từng thuật toán.
- **So sánh hiệu suất**: Bảng so sánh ghi lại thời gian thực thi và số lần mở rộng (expansions) để so sánh (cùng trạng thái ban đầu và mục tiêu).
- **Nhận xét**: Phân tích ưu điểm, nhược điểm và hiệu quả khi áp dụng vào bài toán 8-puzzle.
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

