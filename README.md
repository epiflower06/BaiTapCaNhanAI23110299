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

Dự án này tập trung vào việc cài đặt và so sánh hiệu suất của các thuật toán tìm kiếm trong trí tuệ nhân tạo, sử dụng bài toán 8-Puzzle làm trường hợp thử nghiệm. Bài toán 8-Puzzle là một trò chơi đơn giản nhưng hiệu quả để minh họa nguyên lý hoạt động của các thuật toán tìm kiếm.

Các thuật toán được triển khai trong dự án này được phân thành 6 nhóm chính:

- **Thuật toán tìm kiếm mù (Uninformed Search)**
- **Thuật toán tìm kiếm có thông tin (Informed Search)**
- **Thuật toán leo đồi và biến thể, di truyền (Local Search)**
- **Thuật toán dựa trên ràng buộc (CSPs)**
- **Thuật toán tìm kiếm trong môi trường phức tạp (Complex Environment)**
- **Thuật toán học tăng cường (Reinforcement Learning)**
Dự án cung cấp một giao diện trực quan, cho phép người dùng theo dõi quá trình tìm kiếm lời giải theo từng bước, giúp hiểu rõ hơn về cơ chế hoạt động của mỗi thuật toán.

---

## 📚 Các thuật toán tìm kiếm

### 1. Nhóm thuật toán Uninformed Search

#### Breadth-First Search (BFS)
- **Cách hoạt động:** Khám phá không gian trạng thái theo chiều rộng, mở rộng toàn bộ nút ở độ sâu hiện tại trước khi tiếp tục.
- **Ưu điểm:** Đảm bảo tìm được đường đi ngắn nhất nếu chi phí bước đồng nhất.
- **Nhược điểm:** Tiêu tốn rất nhiều bộ nhớ.
- **Độ phức tạp:**  
  - Thời gian: O(b^d)  
  - Không gian: O(b^d)
📎 [Xem đoạn code Breadth-First Search (BFS)](https://github.com/epiflower06/BaiTapCaNhanAI23110299/blob/main/23110299_TranThiNhuQuynh_baitapcanhanAI.py#L249-L262)

#### Depth-First Search (DFS)
- **Cách hoạt động:** Khám phá sâu theo nhánh cho đến cùng rồi quay lui.
- **Ưu điểm:** Tiết kiệm bộ nhớ hơn BFS.
- **Nhược điểm:** Không đảm bảo tìm đường ngắn nhất, có thể rơi vào vòng lặp vô hạn.
- **Độ phức tạp:**  
  - Thời gian: O(b^m)  
  - Không gian: O(b*m)
📎 [Xem đoạn code Depth-First Search (DFS)](https://github.com/epiflower06/BaiTapCaNhanAI23110299/blob/main/23110299_TranThiNhuQuynh_baitapcanhanAI.py#L264-L279)
#### Iterative Deepening 
- Kết hợp ưu điểm DFS và BFS.
📎 [Xem đoạn code Iterative Deepening ]
#### Uniform Cost Search
- Tìm đường đi chi phí thấp nhất.

📎 [Xem đoạn code Uniform Cost Search]

### 2. Nhóm thuật toán Informed Search

#### Greedy Search
- Chọn nút có chi phí ước lượng nhỏ nhất.
📎 [Xem đoạn code Greedy Search]
#### A* Search
- Kết hợp chi phí thực và ước lượng (g + h).
📎 [Xem đoạn code A* Search]

#### IDA* Search
- Kết hợp A* với DFS theo độ sâu tăng dần.
📎 [Xem đoạn code IDA* Search]

---

### 3. Nhóm thuật toán Local Search

#### Simple Hill Climbing
📎 [Xem đoạn code Simple Hill Climbing]
#### Steepest Hill Climbing
📎 [Xem đoạn code Steepest Hill Climbing]
#### Beam Search
📎 [Xem đoạn code Beam Search]
#### Stochastic Hill Climbing
📎 [Xem đoạn code Stochastic Hill Climbing]
#### Simulated Annealing
📎 [Xem đoạn code Simulated Annealing]
#### Genetic Algorithm
📎 [Xem đoạn code Genetic Algorithm]



### 4. Nhóm thuật toán CSPs - Ràng buộc

#### Backtracking Search

📎 [Xem đoạn code Backtracking Search]

### 5. Nhóm thuật toán tìm kiếm môi trường phức tạp

#### Sensorless BFS
📎 [Xem đoạn code Sensorless BFS]
#### AND-OR Search
📎 [Xem đoạn code  AND-OR Search]


### 6. Nhóm thuật toán Học tăng cường (Reinforcement Learning)

#### Q-Learning

📎 [Xem đoạn code Q-Learning]

---


## 📊 Tổng Kết

- Dự án giúp sinh viên **hiểu sâu sắc về các thuật toán AI**
- Cung cấp nền tảng cho các ứng dụng mở rộng trong lĩnh vực tự động hóa, robot, và lập kế hoạch.

---

## 📬 Liên hệ

Mọi góp ý xin gửi về: **ttnquynh20@gmail.com**

---


