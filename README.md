# TRÍ TUỆ NHÂN TẠO - ĐỒ ÁN CÁ NHÂN
# ÁP DỤNG CÁC THUẬT TOÁN TRONG AI VÀO BÀI TOÁN 8 PUZZLE
# Bài tập cá nhân môn Trí Tuệ Nhân Tạo (AI) Trần Thị Như Quỳnh - 23110299 - 8 Puzzle 
 
---

## 📌 Mục Lục

- [Giới thiệu](#giới-thiệu)
- [Các thuật toán tìm kiếm](#các-thuật-toán-tìm-kiếm)
  - [1. Nhóm thuật toán Uninformed Search](#1-nhóm-thuật-toán-uninformed-search)
    - [BFS](#breadth-first-search-bfs)
    - [DFS](#depth-first-search-dfs)
    - [Iterative Deepening DFS](#iterative-deepening-dfs)
    - [Uniform Cost Search](#uniform-cost-search)
  - [2. Nhóm thuật toán Informed Search](#2-nhóm-thuật-toán-informed-search)
    - [Greedy Search](#greedy-search)
    - [A* Search](#a-search)
    - [IDA* Search](#ida-search)
  - [3. Nhóm thuật toán Local Search](#3-nhóm-thuật-toán-local-search)
    - [Simple Hill Climbing](#simple-hill-climbing)
    - [Steepest Hill Climbing](#steepest-hill-climbing)
    - [Beam Search](#beam-search)
    - [Stochastic Hill Climbing](#stochastic-hill-climbing)
    - [Simulated Annealing](#simulated-annealing)
    - [Genetic Algorithm](#genetic-algorithm)
  - [4. Nhóm thuật toán CSPs - Ràng buộc](#4-nhóm-thuật-toán-csps---ràng-buộc)
    - [Backtracking Search](#backtracking-search)
  - [5. Nhóm thuật toán tìm kiếm môi trường phức tạp](#5-nhóm-thuật-toán-tìm-kiếm-môi-trường-phức-tạp)
    - [Sensorless BFS](#sensorless-bfs)
    - [AND-OR Search](#and-or-search)
  - [6. Nhóm thuật toán Học tăng cường (Reinforcement Learning)](#6-nhóm-thuật-toán-học-tăng-cường-reinforcement-learning)
    - [Q-Learning](#q-learning)
- [📊 Tổng kết](#tổng-kết)

---

## 🧠 Giới Thiệu

Dự án này tập trung vào việc **so sánh hiệu suất các thuật toán tìm kiếm** trong Trí Tuệ Nhân Tạo thông qua **bài toán 8-Puzzle**. Các thuật toán được triển khai kèm giao diện mô phỏng quá trình giải từng bước.

---

## 📚 Các thuật toán tìm kiếm

### 1. Nhóm thuật toán Uninformed Search

#### Breadth-First Search (BFS)
- Duyệt theo từng lớp.
- Đảm bảo tìm được lời giải tối ưu nếu chi phí đồng đều.
📎 [Xem đoạn code Breadth-First Search (BFS)](https://github.com/epiflower06/BaiTapCaNhanAI23110299/blob/main/23110299_TranThiNhuQuynh_baitapcanhanAI.py#L249-L262)

#### Depth-First Search (DFS)
- Duyệt theo chiều sâu.
- Không đảm bảo tìm được lời giải tối ưu.
  
#### Iterative Deepening DFS
- Kết hợp ưu điểm DFS và BFS.
  
#### Uniform Cost Search
- Tìm đường đi chi phí thấp nhất.



### 2. Nhóm thuật toán Informed Search

#### Greedy Search
- Chọn nút có chi phí ước lượng nhỏ nhất.
📎 [`informed_search.py`](./path/to/informed_search.py)

#### A* Search
- Kết hợp chi phí thực và ước lượng (g + h).
📎 [`informed_search.py`](./path/to/informed_search.py)

#### IDA* Search
- Kết hợp A* với DFS theo độ sâu tăng dần.
📎 [`informed_search.py`](./path/to/informed_search.py)

---

### 3. Nhóm thuật toán Local Search

#### Simple Hill Climbing
#### Steepest Hill Climbing
#### Beam Search
#### Stochastic Hill Climbing
#### Simulated Annealing
#### Genetic Algorithm



### 4. Nhóm thuật toán CSPs - Ràng buộc

#### Backtracking Search

📎 Xem code: [`csp_solver.py`](./path/to/csp_solver.py)

### 5. Nhóm thuật toán tìm kiếm môi trường phức tạp

#### Sensorless BFS
#### AND-OR Search

📎 Xem code: [`complex_env_search.py`](./path/to/complex_env_search.py)

### 6. Nhóm thuật toán Học tăng cường (Reinforcement Learning)

#### Q-Learning

📎 Xem code: [`q_learning.py`](./path/to/q_learning.py)

---

## 💻 Demo

<img src="demo.gif" width="500" alt="Demo chạy 8-Puzzle AI">

---

## 📊 Tổng Kết

- Dự án giúp sinh viên **hiểu sâu sắc về các thuật toán AI**
- Cung cấp nền tảng cho các ứng dụng mở rộng trong lĩnh vực tự động hóa, robot, và lập kế hoạch.

---

## 📬 Liên hệ

Mọi góp ý xin gửi về: **tranthinh...@gmail.com**

---


