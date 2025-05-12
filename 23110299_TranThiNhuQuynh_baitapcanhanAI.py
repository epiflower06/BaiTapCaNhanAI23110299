# ======================= PHẦN 1: THƯ VIỆN VÀ KHỞI TẠO =======================
import pygame
import sys
import heapq
import random
import math
import time
import copy
from collections import deque, defaultdict

pygame.init()
# ======================= PHẦN 2: CẤU HÌNH GIAO DIỆN VÀ BIẾN =======================
# Kích thước cửa sổ game
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("8 Puzzle")

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 128, 0)
light_green = (144, 238, 144)
blue = (173, 216, 230)

font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 20)

# Kích thước của mỗi ô vuông trong puzzle
cell_size = 60
puzzle_margin = 5  # khoảng cách giữa các ô

# ======================= PHẦN 3: CẤU TRÚC GIAO DIỆN =======================
# Vị trí bảng trạng thái bắt đầu
start_state_rect = pygame.Rect(50, 150, 3 * cell_size, 3 * cell_size)
puzzle_width = 3 * cell_size
puzzle_height = 3 * cell_size
puzzle_x = start_state_rect.x
puzzle_y = start_state_rect.y

# Các nút điều khiển chính
button_run_rect = pygame.Rect(450, 50, 70, 30)   # Nút RUN
button_stop_rect = pygame.Rect(550, 50, 70, 30)  # Nút STOP
button_exit_rect = pygame.Rect(650, 50, 70, 30)  # Nút EXIT
active_button = None  # Biến lưu trạng thái nút đang được nhấn

# Vị trí bảng trạng thái đích
goal_state_rect = pygame.Rect(450, 150, 3 * cell_size, 3 * cell_size)
goal_x = goal_state_rect.x
goal_y = goal_state_rect.y

# Vị trí vùng hiển thị đường đi kết quả
path_rect = pygame.Rect(50, 400, 700, 150)

# ======================= PHẦN 4: RADIO BUTTON & THỐNG KÊ =======================

# Vị trí nút chọn chế độ nhập tay và ngẫu nhiên
nhap_radio_rect = pygame.Rect(70, 90, 20, 20)
random_radio_rect = pygame.Rect(180, 90, 20, 20)

# ghi lại chế độ  ("Input" hoặc "Random")
selected_input_method = None

# Vị trí hiển thị thông tin thời gian và số bước giải
thoi_gian_text_pos = (50, 570)
so_buoc_text_pos = (50, 600)
thoi_gian_value = "0.00 s"  # Thời gian giải thuật
so_buoc_value = "0"         # Số bước đã thực hiện

# ======================= PHẦN 5: TRẠNG THÁI BÀI TOÁN =======================

start_state = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
#start_state = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
#start_state = [[2, 3, 6], [1, 5, 0], [4, 7, 8]]

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Các biến điều khiển giải thuật và animation
solution_path = []         # Danh sách các bước từ start đến goal
solving = False            # Cờ báo có đang chạy giải thuật không
animation_start_time = 0   # Thời điểm bắt đầu chạy animation
animation_step = 0         # Bước hiện tại đang hiển thị
animation_delay = 0.5      # Độ trễ giữa các bước (giây)
last_animation_time = 0    # Thời điểm cập nhật animation gần nhất

# ======================= PHẦN 6: HÀM TIỆN ÍCH =======================

# Sinh puzzle ngẫu nhiên từ 0 đến 8 và chuyển thành ma trận 3x3
def generate_random_puzzle():
    numbers = list(range(9))
    random.shuffle(numbers)
    return [numbers[i:i + 3] for i in range(0, 9, 3)]

# Vẽ bảng puzzle tại vị trí (x, y), cho biết đây là start hay goal để tô màu phù hợp
def draw_puzzle(state, x, y, is_start_state=False):
    if isinstance(state, tuple):
        try:
            state = [list(row) for row in state]
        except Exception:
            return  
        
    # Kiểm tra tính hợp lệ của ma trận
    if not (isinstance(state, list) and len(state) == 3 and
            all(isinstance(row, list) and len(row) == 3 for row in state)):
        return  
    for i in range(3):
        for j in range(3):
            num = state[i][j]
            cell_x = x + j * cell_size
            cell_y = y + i * cell_size

            if is_start_state:
                cell_color = blue 
                if num == goal_state[i][j] and num != 0:
                    cell_color = light_green # xanh lá đúng vị trí
            else:
                cell_color = light_green # xanh dương là mặc định

            # Vẽ ô
            pygame.draw.rect(screen, cell_color, (cell_x, cell_y, cell_size, cell_size))
            pygame.draw.rect(screen, black, (cell_x, cell_y, cell_size, cell_size), 2)

            if num != 0:
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=(cell_x + cell_size // 2,
                                                  cell_y + cell_size // 2))
                screen.blit(text, text_rect)

# ======================= PHẦN 7: VẼ GIAO DIỆN CHÍNH (GUI) =======================
def draw_gui():
    screen.fill(white)# Làm trắng toàn bộ màn hình
    if active_button == "run":
        pygame.draw.rect(screen, green, button_run_rect)  
    else:
        pygame.draw.rect(screen, white, button_run_rect)
        pygame.draw.rect(screen, green, button_run_rect, 3) 
    text_run = font.render("Run", True, black)
    screen.blit(text_run, (button_run_rect.x + 15, button_run_rect.y + 5))

    if active_button == "stop":
        pygame.draw.rect(screen, green, button_stop_rect)  
    else:
        pygame.draw.rect(screen, white, button_stop_rect)
        pygame.draw.rect(screen, green, button_stop_rect, 3)  
    text_stop = font.render("Stop", True, black)
    screen.blit(text_stop, (button_stop_rect.x + 10, button_stop_rect.y + 5))

    if active_button == "exit":
        pygame.draw.rect(screen, green, button_exit_rect)  
    else:
        pygame.draw.rect(screen, white, button_exit_rect)
        pygame.draw.rect(screen, green, button_exit_rect, 3) 
    text_exit = font.render("Exit", True, black)
    screen.blit(text_exit, (button_exit_rect.x + 10, button_exit_rect.y + 5))

    text_start = font.render("Start state", True, black)
    screen.blit(text_start, (start_state_rect.x, start_state_rect.y - 25))
    pygame.draw.rect(screen, green, start_state_rect, 2)
    draw_puzzle(start_state, puzzle_x, puzzle_y, is_start_state=True)

    text_goal = font.render("Goal state", True, black)
    screen.blit(text_goal, (goal_state_rect.x, goal_state_rect.y - 25))
    pygame.draw.rect(screen, green, goal_state_rect, 2)
    draw_puzzle(goal_state, goal_x, goal_y)

    text_path = font.render("Path", True, black)
    screen.blit(text_path, (path_rect.x, path_rect.y - 25))
    pygame.draw.rect(screen, green, path_rect, 2)
    if solution_path:
        path_text = "\n".join(str(state) for state in solution_path)
        path_lines = path_text.split('\n')
        for i, line in enumerate(path_lines):
            text_surface = small_font.render(line, True, black)
            screen.blit(text_surface, (path_rect.x + 10, path_rect.y + 10 + i * 15))
            if path_rect.y + 10 + (i + 1) * 15 > path_rect.bottom - 10:
                break 

    text_nhap = font.render("Input", True, black)
    screen.blit(text_nhap, (nhap_radio_rect.x + 30, nhap_radio_rect.y))
    pygame.draw.circle(screen, black, nhap_radio_rect.center, 10, 2)
    if selected_input_method == "Input":
        pygame.draw.circle(screen, green, nhap_radio_rect.center, 7)

    text_random = font.render("Random", True, black)
    screen.blit(text_random, (random_radio_rect.x + 30, random_radio_rect.y))
    pygame.draw.circle(screen, black, random_radio_rect.center, 10, 2)
    if selected_input_method == "Random":
        pygame.draw.circle(screen, green, random_radio_rect.center, 7)

    text_thoi_gian = font.render(f"Time : {thoi_gian_value}", True, black)
    screen.blit(text_thoi_gian, thoi_gian_text_pos)
    text_so_buoc = font.render(f"Step : {so_buoc_value}", True, black)
    screen.blit(text_so_buoc, so_buoc_text_pos)

    pygame.draw.rect(screen, blue, dropdown_rect)
    text_thuattoan = font.render(selected_algorithm_name if selected_algorithm_name else "Select Algorithm", True, black)
    screen.blit(text_thuattoan, (dropdown_rect.x + 5, dropdown_rect.y + 5))

    if dropdown_open:
        for i, option in enumerate(dropdown_options):
            pygame.draw.rect(screen, blue, dropdown_options_rects[i])
            pygame.draw.rect(screen, black, dropdown_options_rects[i], 2)
            text_option = font.render(option, True, black)
            screen.blit(text_option, (dropdown_options_rects[i].x + 5, dropdown_options_rects[i].y + 5))

    pygame.display.flip()

# ======================= PHẦN 8: HÀM TÌM Ô TRỐNG VÀ SINH TRẠNG THÁI KẾ =======================

# Tìm vị trí ô trống trong ma trận
def find_blank(state):
    if isinstance(state, tuple):
        state = [list(row) for row in state] # Nếu là tuple, chuyển về list
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c # Trả về vị trí hàng, cột của ô trống
    raise ValueError("No blank (0) in this state")

# Tạo tất cả các trạng thái con có thể từ trạng thái hiện tại bằng cách di chuyển ô trống
def successors(state):
    blank_r, blank_c = find_blank(state)#vị trí ô trống
    possible_moves = []
    # Di chuyển lên
    if blank_r > 0:
        new_state = [row[:] for row in state]#sao chép ma trận
        new_state[blank_r][blank_c], new_state[blank_r - 1][blank_c] = new_state[blank_r - 1][blank_c], new_state[blank_r][blank_c]
        possible_moves.append(new_state)
    #xuống
    if blank_r < 2:
        new_state = [row[:] for row in state]
        new_state[blank_r][blank_c], new_state[blank_r + 1][blank_c] = new_state[blank_r + 1][blank_c], new_state[blank_r][blank_c]
        possible_moves.append(new_state)
    # trái
    if blank_c > 0:
        new_state = [row[:] for row in state]
        new_state[blank_r][blank_c], new_state[blank_r][blank_c - 1] = new_state[blank_r][blank_c - 1], new_state[blank_r][blank_c]
        possible_moves.append(new_state)
    #phải
    if blank_c < 2:
        new_state = [row[:] for row in state]
        new_state[blank_r][blank_c], new_state[blank_r][blank_c + 1] = new_state[blank_r][blank_c + 1], new_state[blank_r][blank_c]
        possible_moves.append(new_state)
    return possible_moves

def is_equal(state1, state2):
    return all(state1[i][j] == state2[i][j] for i in range(3) for j in range(3))
#-----------------------PHẦN 9: NHÓM THUẬT TOÁN UNIFORMED SEARCH (Không Heuristic)------------------------------------------
#=================================Thuật toán Breadth - first Search===================================
def bfs(start, goal):
    visited = set()# Tập trạng thái đã thăm
    queue = deque([(start, [])])# Hàng đợi lưu (trạng thái hiện tại, đường đi)
    while queue:
        state, path = queue.popleft()# Lấy phần tử đầu hàng đợi
        key = str(state)
        if key in visited:
            continue
        visited.add(key)
        if state == goal:
            return path + [state] # Tìm thấy -> trả về đường đi
        for next_state in successors(state):
            queue.append((next_state, path + [state]))
    return []
#***************************Thuật toán Depth - first Search ***********************************
def dfs(start, goal, depth_limit=200):
    visited = set()
    stack = [(start, [])]# Ngăn xếp lưu (trạng thái, đường đi)
    while stack:
        state, path = stack.pop()
        key = str(state)
        if key in visited:
            continue
        visited.add(key)
        if state == goal:
            return path + [state]
        if len(path) >= depth_limit:
            continue# Giới hạn độ sâu để tránh lặp vô hạn
        for next_state in successors(state):
            stack.append((next_state, path + [state]))
    return []
#================================Thuật toán Uniform Cost Search==========================================
def ucs(start, goal):
    heap = []
    visited = set()
    heapq.heappush(heap, (0, start, [])) # Heap lưu (chi phí, trạng thái, đường đi)
    while heap:
        cost, state, path = heapq.heappop(heap)
        key = str(state)
        if key in visited:
            continue
        visited.add(key)
        if state == goal:
            return path + [state]
        for next_state in successors(state):
            heapq.heappush(heap, (cost + 1, next_state, path + [state]))
    return []

#***************************Thuật toán Iterative Deepening ***********************************
def iterative_deepening(start, goal):
    def dls(state, goal, limit, path, visited): # Hàm tìm kiếm giới hạn độ sâu (DLS)
        if state == goal:
            return path + [state]
        if limit <= 0:
            return None
        visited.add(str(state))
        for next_state in successors(state):
            if str(next_state) not in visited:
                result = dls(next_state, goal, limit - 1, path + [state], visited)
                if result:
                    return result
        return None
    # Lặp với độ sâu tăng dần
    for depth in range(1, 50):
        visited = set()
        result = dls(start, goal, depth, [], visited)
        if result:
            return result
    return []
#-----------------------------------------------------------------------------------------
# ======================= PHẦN 10: INFORMED SEARCH (Có sử dụng heuristic) =======================

# ----------- Hàm heuristic: Tính tổng khoảng cách Manhattan từ mỗi ô đến vị trí đúng -----------
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                # Vị trí đúng của ô val trong goal state
                goal_i = (val - 1) // 3
                goal_j = (val - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance# Giá trị càng thấp càng gần đích

#==========================Thuật toán Greedy Search====================================
def greedy(start, goal):
    heap = []
    visited = set()
    heapq.heappush(heap, (heuristic(start), start, []))# (heuristic, state, path)
    while heap:
        h, state, path = heapq.heappop(heap)
        key = str(state)
        if key in visited:
            continue
        visited.add(key)
        if state == goal:
            return path + [state]
        for next_state in successors(state):
            heapq.heappush(heap, (heuristic(next_state), next_state, path + [state]))
    return []
#=============================Thuật toán A* ==================================
def astar(start, goal):
    heap = []
    visited = set()
    heapq.heappush(heap, (heuristic(start), 0, start, [])) # (f = g + h, g, state, path)
    while heap:
        f, g, state, path = heapq.heappop(heap)
        key = str(state)
        if key in visited:
            continue
        visited.add(key)
        if state == goal:
            return path + [state]
        for next_state in successors(state):
            heapq.heappush(heap, (g + 1 + heuristic(next_state), g + 1, next_state, path + [state]))
    return []
#============================Thuật toán Iterative Deepening A* =======================================
def ida_star(start, goal):
        # Hàm tìm kiếm theo ngưỡng
    def search(state, g, threshold, path):
        f = g + heuristic(state)
        if f > threshold:
            return f, None
        if state == goal:
            return f, path + [state]
        min_cost = float("inf")
        for next_state in successors(state):
            if next_state not in path:  # Tránh vòng lặp
                new_cost, result = search(next_state, g + 1, threshold, path + [state])
                if result:
                    return new_cost, result
                min_cost = min(min_cost, new_cost)
        return min_cost, None
    # Bắt đầu với ngưỡng = heuristic ban đầu
    threshold = heuristic(start)
    while True:
        new_threshold, result = search(start, 0, threshold, [])
        if result:
            return result
        if new_threshold == float("inf"):
            return []
        threshold = new_threshold

# ======================= PHẦN 11: LOCAL SEARCH (Tìm kiếm cục bộ, không duyệt toàn bộ) =======================
# ----------- Simple Hill Climbing: Leo dốc đơn giản, đi tới hàng xóm tốt hơn -----------
def simple_hillclimbing(start, goal):
    current = start                            # Trạng thái hiện tại
    current_h = heuristic(current)             # Tính heuristic hiện tại
    path = [current]                           # Danh sách lưu đường đi
    visited = set()                            # Tránh lặp vô hạn
    while True:
        neighbors = successors(current)# Sinh các trạng thái hàng xóm
        best_neighbor = None
        best_h = current_h # Giả sử trạng thái hiện tại là tốt nhất

        # Duyệt các hàng xóm để tìm cái tốt hơn (heuristic thấp hơn)
        for neighbor in neighbors:
            h = heuristic(neighbor)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
        if best_neighbor is None: # Không còn hàng xóm tốt hơn
            break
        current = best_neighbor# Cập nhật trạng thái hiện tại
        current_h = best_h
        key = str(current)
        if key in visited:# Đã từng thăm → dừng (tránh vòng lặp)
            break
        visited.add(key)
        path.append(current)# Lưu vào đường đi
        if current == goal:
            return path
    return path if current == goal else []

# ----------- Steepest Ascent Hill Climbing: Luôn chọn hàng xóm tốt nhất -----------
def steepest_climbing(start, goal):
    current = start
    current_h = heuristic(current)
    path = [current]
    visited = set()
    while True:
        neighbors = successors(current)
        best_neighbor = None
        best_h = current_h
        # Duyệt qua toàn bộ hàng xóm, chọn cái có heuristic nhỏ nhất
        for neighbor in neighbors:
            h = heuristic(neighbor)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
        if best_neighbor is None:# Không có hàng xóm nào tốt hơn
            break
        current = best_neighbor
        current_h = best_h
        key = str(current)
        if key in visited:
            break
        visited.add(key)
        path.append(current)
        if current == goal:
            return path
    return path if current == goal else []

# ----------- Stochastic Hill Climbing: Chọn ngẫu nhiên một hàng xóm tốt hơn -----------
def stochastic_hill_climbing(start, goal):
    current = start
    current_h = heuristic(current)
    path = [current]
    visited = set()
    while True:
        neighbors = successors(current)
         # Lọc các hàng xóm có heuristic tốt hơn hiện tại
        better_neighbors = [neighbor for neighbor in neighbors if heuristic(neighbor) < current_h]
        if not better_neighbors: # Không còn hàng xóm tốt hơn → kết thúc
            break

        # Chọn ngẫu nhiên một hàng xóm tốt hơn
        current = random.choice(better_neighbors)
        current_h = heuristic(current)
        key = str(current)
        if key in visited:
            break
        visited.add(key)
        path.append(current)
        if current == goal:
            return path
    return path if current == goal else []

# ----------- Beam Search: Giữ lại một số trạng thái tốt nhất ở mỗi vòng -----------
def beam_search(start, goal, beam_width=3, max_loop=1000):
    current_states = [start] # Danh sách các trạng thái hiện tại (beam)
    paths = {tuple(map(tuple, start)): [start]}# Bản đồ trạng thái → đường đi
    loop = 0
    visited = set()
    while loop < max_loop:
        all_neighbors = []
        for state in current_states:
            neighbors = successors(state)
            for neighbor in neighbors:
                if tuple(map(tuple, neighbor)) not in visited:
                    h = heuristic(neighbor)
                    # Lưu hàng xóm với heuristic và đường đi mới
                    all_neighbors.append((h, neighbor, paths[tuple(map(tuple, state))] + [neighbor]))
                    visited.add(tuple(map(tuple, neighbor)))
        if not all_neighbors:# Không còn hàng xóm nào hợp lệ
            break
        # Chọn beam_width hàng xóm có heuristic thấp nhất
        all_neighbors.sort(key=lambda x: x[0]) # Sắp xếp tăng dần theo heuristic
        current_states = []
        new_paths = {}
        for i in range(min(beam_width, len(all_neighbors))):
            h, state, path = all_neighbors[i]
            current_states.append(state)
            new_paths[tuple(map(tuple, state))] = path
            if state == goal:
                return path
        paths = new_paths # Cập nhật beam
        loop += 1
    # Sau max_loop, kiểm tra xem có trạng thái nào là goal không
    for state in current_states:
        if state == goal:
            return paths[tuple(map(tuple, state))]
    return []

# ----------- Simulated Annealing: Chấp nhận tạm thời trạng thái xấu để thoát cực trị cục bộ -----------
def sa(start, goal, initial_temp=1000, cooling_rate=0.995, min_temp=0.01):
    current = start
    current_h = heuristic(current)
    path = [current]
    temp = initial_temp
    max_steps = 1000
    step = 0
    while temp > min_temp and step < max_steps:
        neighbors = successors(current)
        if not neighbors:
            break
        next_state = random.choice(neighbors)# Chọn hàng xóm ngẫu nhiên
        next_h = heuristic(next_state)
        delta_e = next_h - current_h
        # Nếu trạng thái mới tốt hơn → chấp nhận ngay
        # Nếu xấu hơn → vẫn có thể chấp nhận với xác suất exp(-delta/temp)
        if delta_e <= 0 or random.random() < math.exp(-delta_e / max(temp, 1e-10)):
            current = next_state
            current_h = next_h
            path.append(current)
        temp *= cooling_rate# Giảm nhiệt độ dần
        step += 1
        if current == goal: # Trả về đường đi, loại bỏ bước trùng lặp liên tiếp

            return [s for i, s in enumerate(path) if i == 0 or path[i-1] != s]
    return [s for i, s in enumerate(path) if i == 0 or path[i-1] != s] if current == goal else []


# -------------------GENETIC ALGORITHM (Giải thuật di truyền)-------------------
# ----------- Hàm thực thi một chuỗi bước di chuyển lên trạng thái bắt đầu -----------
def apply_moves(state, moves):
    current = [row[:] for row in state]  # Sao chép trạng thái hiện tại
    states = [current]                   # Danh sách lưu các trạng thái sau mỗi bước

    for dr, dc in moves:
        try:
            r, c = find_blank(current)   # Tìm vị trí ô trống
            nr, nc = r + dr, c + dc      # Vị trí mới sau khi di chuyển
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state = [row[:] for row in current]
                # Đổi chỗ ô trống với ô mục tiêu
                new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                states.append(new_state)
                current = new_state
            else:
                break
        except ValueError:
            break
    return states, current# Trả về toàn bộ chuỗi trạng thái và trạng thái cuối cùng

# ----------- Hàm tính fitness (độ phù hợp) của một cá thể (chuỗi bước di chuyển) -----------
def ga_fitness(moves, start, goal):
    _, final_state = apply_moves(start, moves)  # Áp dụng chuỗi bước lên start
    distance = heuristic(final_state)           # Đo khoảng cách đến goal
    return -distance - len(moves) * 0.1         # Ưu tiên ngắn và gần goal hơn

# ----------- Lai ghép 2 cá thể (2 chuỗi bước) để tạo con -----------
def ga_crossover(p1, p2):
    if not p1 or not p2:
        return p1 if p1 else p2# Nếu một trong hai cha mẹ rỗng
    point = random.randint(0, min(len(p1), len(p2)))# Chọn điểm lai ngẫu nhiên
    child = p1[:point] + p2[point:]# Ghép phần đầu của p1 với phần cuối của p2
    return child

# ----------- Đột biến: thay đổi ngẫu nhiên một bước trong chuỗi -----------
def ga_mutate(moves, start):
    if not moves:
        return [random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])]
    moves = moves[:]  # Tạo bản sao để tránh làm thay đổi gốc
    if len(moves) > 0:  # Ensure moves is non-empty for indexing
        idx = random.randint(0, len(moves) - 1)  # Fix index range
        if random.random() < 0.5 and len(moves) < 50:  
            # Thêm một bước di chuyển tại vị trí ngẫu nhiên
            moves.insert(idx, random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)]))
        elif random.random() < 0.5 and len(moves) > 1:  # Xóa một bước nếu đủ dài
            moves.pop(random.randint(0, len(moves) - 1))
        elif moves:  # Thay thế một bước ngẫu nhiên
            moves[idx] = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
    if not moves:  # Đảm bảo luôn có ít nhất một bước
        moves = [random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])]
    return moves

# ----------- Tạo cá thể mới ngẫu nhiên -----------
def ga_random_moves():
    return [random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)]) for _ in range(random.randint(5, 20))]

# ----------- Giải thuật di truyền chính -----------
def genetic_algorithm(start, goal, max_gen=1000, pop_size=200, mutation_rate=0.3):
        # Khởi tạo quần thể ban đầu: 1 cá thể rỗng + các cá thể ngẫu nhiên
    population = [[]] + [ga_random_moves() for _ in range(pop_size - 1)]
    best_moves = []
    best_fitness = float('-inf')
    stuck_count = 0# Đếm số thế hệ không cải thiện
    for gen in range(max_gen):
        # Sắp xếp quần thể theo độ phù hợp giảm dần
        population.sort(key=lambda moves: ga_fitness(moves, start, goal))
        best = population[0]
        current_fitness = ga_fitness(best, start, goal)
        _, final_state = apply_moves(start, best)
        if is_equal(final_state, goal): # Đã tìm thấy lời giải
            states, _ = apply_moves(start, best)
            return states
        # Kiểm tra xem có cải thiện không
        if current_fitness == best_fitness:
            stuck_count += 1
        else:
            stuck_count = 0
            best_fitness = current_fitness
            best_moves = best
        if stuck_count >= 100:
            break# Dừng sớm nếu không cải thiện sau nhiều thế hệ
        # Tạo quần thể mới
        new_pop = population[:10]  # Elitism: giữ lại 10 cá thể tốt nhất
        while len(new_pop) < pop_size:
            # Lai ghép hai cá thể cha mẹ ngẫu nhiên trong top 50
            p1, p2 = random.choices(population[:50], k=2)
            child = ga_crossover(p1, p2)
            if random.random() < mutation_rate:
                child = ga_mutate(child, start)
            new_pop.append(child)
        population = new_pop# update

        # Nếu kết thúc mà chưa tới goal, vẫn trả lại cá thể tốt nhất tìm được
    states, final_state = apply_moves(start, best_moves)
    return states if is_equal(final_state, goal) else []


#--------------------------PHẦN 13: NHÓM THUẬT TOÁN COMPLEX ENVIRONMENT---------------------------------------
#======================Thuật toán Sensorless BFS===========================================
# Trong bài toán này, ta không biết chính xác trạng thái ban đầu mà chỉ có một tập hợp các trạng thái có thể xảy ra (belief state).
# Mỗi hành động phải áp dụng lên toàn bộ tập hợp này → thuật toán phải xử lý các trạng thái đồng thời.

# Hàm kiểm tra trạng thái có giải được hay không dựa vào số lần hoán vị (tính chẵn lẻ)
def is_solvable(state):
    flat = [cell for row in state for cell in row if cell != 0]  # Bỏ ô trống (0), dồn ma trận thành 1 hàng
    inversions = sum(1 for i in range(len(flat)) for j in range(i+1, len(flat)) if flat[i] > flat[j])  # Đếm số cặp nghịch thế
    blank_row = find_blank(state)[0]  # Lấy chỉ số dòng của ô trống
    return (inversions + blank_row) % 2 == 0  # Tổng nghịch thế + vị trí ô trống phải chẵn => trạng thái hợp lệ

# Thuật toán BFS áp dụng cho bài toán belief state (nhiều trạng thái cùng lúc, không xác định trạng thái ban đầu chính xác)
def sensorless_bfs(initial_states, goal_state):
    # Chuẩn hóa belief state thành frozenset các trạng thái (dạng tuple để băm)
    if isinstance(initial_states, list):
        initial_belief = frozenset([tuple(tuple(row) for row in initial_states)])
    else:
        initial_belief = frozenset(initial_states)

    visited = set()  # Tập các belief state đã duyệt
    queue = deque([(initial_belief, [])])  # Hàng đợi BFS gồm (belief_state, path)

    while queue:
        belief_state, path = queue.popleft()
        if belief_state in visited:
            continue
        visited.add(belief_state)

        # Kiểm tra nếu bất kỳ trạng thái nào trong belief trùng với trạng thái đích
        goal_tuple = tuple(tuple(row) for row in goal_state)
        if any(s == goal_tuple for s in belief_state):
            solution = [[row[:] for row in initial_states]]  # Bắt đầu xây dựng đường đi từ trạng thái đầu tiên
            current = solution[0]
            for action in path:
                r, c = find_blank(current)
                dr, dc = action
                if 0 <= r + dr < 3 and 0 <= c + dc < 3:
                    new_state = [row[:] for row in current]
                    new_state[r][c], new_state[r + dr][c + dc] = new_state[r + dr][c + dc], new_state[r][c]
                    solution.append(new_state)
                    current = new_state
            return solution  # Trả về chuỗi trạng thái từ đầu đến đích

        # Thử các bước di chuyển từ các trạng thái hiện có trong belief
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_belief = set()
            for state in belief_state:
                state_list = [list(row) for row in state]
                try:
                    r, c = find_blank(state_list)
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 3 and 0 <= nc < 3:
                        new_state = [row[:] for row in state_list]
                        new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                        next_belief.add(tuple(tuple(row) for row in new_state))
                except ValueError:
                    continue
            if next_belief:
                next_belief_key = frozenset(next_belief)
                if next_belief_key not in visited:
                    queue.append((next_belief_key, path + [(dr, dc)]))
    return []  # Không tìm được đường đi

# ========================== Thuật toán AND-OR Search ==============================
# Giải bài toán trong không gian belief (có nhiều trạng thái đầu vào), trả về kế hoạch nếu có
def and_or_search(belief, goal, visited=None, depth=0, max_depth=100):
    if visited is None:
        visited = set()

    # Chuẩn hóa belief state về frozenset
    if isinstance(belief, list):
        belief = frozenset([tuple(tuple(row) for row in belief)])
    elif not isinstance(belief, frozenset):
        belief = frozenset(belief)

    if depth > max_depth:  # Giới hạn độ sâu để tránh đệ quy vô hạn
        return None

    if not belief:  # Nếu belief rỗng => không hợp lệ
        return None
    for state in belief:
        if not (isinstance(state, tuple) and len(state) == 3 and
                all(isinstance(row, tuple) and len(row) == 3 for row in state)):
            return None  # Kiểm tra định dạng trạng thái

    belief_key = frozenset(belief)
    if belief_key in visited:
        return None
    visited.add(belief_key)

    goal_tuple = tuple(tuple(row) for row in goal)

    if any(state == goal_tuple for state in belief):  # Nếu đạt goal
        return []

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Duyệt các hành động
        next_belief = set()
        for state in belief:
            try:
                state_list = [list(row) for row in state]
                r, c = find_blank(state_list)
                nr, nc = r + dr, c + dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    new_state = [row[:] for row in state_list]
                    new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                    next_belief.add(tuple(tuple(row) for row in new_state))
            except (ValueError, TypeError):
                continue

        if next_belief:
            plan_rest = and_or_search(next_belief, goal, visited, depth + 1, max_depth)
            if plan_rest is not None:
                return [("Move", (dr, dc))] + plan_rest

    return None

# ================= NHÓM THUẬT TOÁN CSP======================== 
# ---------------------Backtracking Search --------------------
def backtracking_search(state, goal, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    if state == goal:
        return path + [state]
    ser = tuple(tuple(row) for row in state)
    visited.add(ser)
    for nxt in successors(state):  # Duyệt các trạng thái kế tiếp hợp lệ
        nxt_ser = tuple(tuple(row) for row in nxt)
        if nxt_ser in visited:
            continue
        res = backtracking_search(nxt, goal, visited, path + [state])
        if res is not None:
            return res
    return None

# ================= NHÓM THUẬT TOÁN Reinforcement Learning==================
# -----------------Q-Learning Agent ------------------
# Các hằng số biểu diễn hướng di chuyển
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
actions = ['up', 'down', 'left', 'right']

# Hàm thực hiện hành động trên trạng thái
def move(state, action):
    r, c = find_blank(state)
    new = [row[:] for row in state]
    if action == 'up' and r > 0:
        new[r][c], new[r-1][c] = new[r-1][c], new[r][c]
    elif action == 'down' and r < 2:
        new[r][c], new[r+1][c] = new[r+1][c], new[r][c]
    elif action == 'left' and c > 0:
        new[r][c], new[r][c-1] = new[r][c-1], new[r][c]
    elif action == 'right' and c < 2:
        new[r][c], new[r][c+1] = new[r][c+1], new[r][c]
    else:
        return None
    return new

# Trả về tất cả các trạng thái kế tiếp hợp lệ
def successorss(state):
    moves = []
    for a in ['up', 'down', 'left', 'right']:
        ns = move(state, a)
        if ns:
            moves.append(ns)
    return moves

# Định nghĩa lớp Q-Learning
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2, episodes=5000):
        self.alpha = alpha  # Hệ số học
        self.gamma = gamma  # Hệ số giảm giá
        self.epsilon = epsilon  # Xác suất khám phá
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99995
        self.episodes = episodes
        self.actions = ['up', 'down', 'left', 'right']
        self.q_table = defaultdict(lambda: {a: 0.0 for a in self.actions})  # Bảng Q
        self.trained = False

    def serialize(self, state):
        return tuple(num for row in state for num in row)  # Chuyển trạng thái thành tuple 1 chiều

    def get_reward(self, state, next_state, goal_state):
        if is_equal(next_state, goal_state):
            return 100
        current_h = heuristic(state)
        next_h = heuristic(next_state)
        return (current_h - next_h) * 0.1 - 1  # Thưởng nếu tiến gần đến mục tiêu

    def choose_action(self, state, explore=True):
        s = self.serialize(state)
        if explore and random.random() < self.epsilon:
            return random.choice(self.actions)  # Khám phá
        valid_actions = [a for a in self.actions if move(state, a) is not None]
        if not valid_actions:
            return random.choice(self.actions)
        q_values = [self.q_table[s][a] for a in valid_actions]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(valid_actions, q_values) if q == max_q]
        return random.choice(best_actions)  # Khai thác

    def learn(self, state, action, reward, next_state):
        s = self.serialize(state)
        ns = self.serialize(next_state)
        current_q = self.q_table[s][action]
        next_q = max(self.q_table[ns].values(), default=0)
        self.q_table[s][action] = current_q + self.alpha * (reward + self.gamma * next_q - current_q)  # Cập nhật Q

    def train(self, start_state, goal_state):
        """
        Huấn luyện agent sử dụng Q-learning để tìm đường đến mục tiêu.
        :param start_state: trạng thái bắt đầu
        :param goal_state: trạng thái mục tiêu
        """
        if self.trained:
            return
        for episode in range(self.episodes):
            state = copy.deepcopy(start_state)
            for step in range(100):
                action = self.choose_action(state, explore=True)
                next_state = move(state, action)
                if next_state is None:
                    continue
                reward = self.get_reward(state, next_state, goal_state)
                self.learn(state, action, reward, next_state)
                state = next_state
                if is_equal(state, goal_state):
                    break
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.trained = True

    def solve(self, start_state, goal_state):
        """
        Sử dụng chính sách đã học để giải quyết bài toán.
        :param start_state: trạng thái bắt đầu
        :param goal_state: trạng thái mục tiêu
        :return: đường đi tìm được từ start_state đến goal_state
        """
        path = [copy.deepcopy(start_state)]
        state = copy.deepcopy(start_state)
        steps = 0
        max_steps = 50
        visited = {self.serialize(state)}
        while steps < max_steps and not is_equal(state, goal_state):
            action = self.choose_action(state, explore=False)  # Chọn hành động tốt nhất (không khám phá)
            next_state = move(state, action)
            if next_state is None:
                break
            ser = self.serialize(next_state)
            if ser in visited:
                break  # Nếu đã thăm trạng thái này, dừng lại
            path.append(next_state)
            visited.add(ser)
            state = next_state
            steps += 1
        return path
dropdown_open = False
agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.2, episodes=5000)

algorithms = {
    #nhóm Uninformed search
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Iterative Deepening": iterative_deepening,
    #nhóm Informed search
    "A*": astar,
    "IDA*": ida_star,
    "Greedy": greedy,
    #nhóm Local search
    "Simple HC": simple_hillclimbing,
    "Steepest Ascent HC": steepest_climbing,
    "Stochastic HC": stochastic_hill_climbing,
    "S Annealing": sa,
    "Beam Search": beam_search,
    "Genetic Algorithm": genetic_algorithm,
    #nhóm Complex environment
    "Sensorless BFS": sensorless_bfs,
    "AND OR": and_or_search,
    #nhóm CSP (Constraint satisfaction problem)
    "Backtracking": lambda s, g: backtracking_search(s, g),
    #nhóm Reinforcement learning
    "Q-learning": lambda s, g: agent.solve(s, g)
}

selected_algorithm_name = "Select Algorithm"
selected_algorithm_func = None
dropdown_rect = pygame.Rect(50, 50, 200, 30)
dropdown_options = list(algorithms.keys())
dropdown_options_rects = [pygame.Rect(50, 80 + i * 30, 200, 30) for i in range(len(dropdown_options))]

def animate_solution():
    global animation_step, last_animation_time, start_state, thoi_gian_value
    if animation_step < len(solution_path):
        current_time = time.time()
        if current_time - last_animation_time > animation_delay:
            start_state = solution_path[animation_step]
            if isinstance(start_state, tuple):
                start_state = [list(row) for row in start_state]
            animation_step += 1
            last_animation_time = current_time
            if animation_start_time > 0:
                elapsed_time = current_time - animation_start_time
                thoi_gian_value = f"{elapsed_time:.2f} s"

def start_solving():
    global solving, solution_path, thoi_gian_value, so_buoc_value, animation_step, animation_start_time
    if not solving and selected_algorithm_func is not None:
        solving = True
        solution_path = []
        animation_step = 0
        animation_start_time = time.time()
        thoi_gian_value = "0.00 s"
        so_buoc_value = "Calculating..."
        start_time = time.time()
        if selected_algorithm_name == "AND OR":
            belief = [row[:] for row in start_state]
            solution = []
            plan = and_or_search(belief, goal_state)
            if plan is not None:
                current = [row[:] for row in start_state]
                solution = [current]
                for action, (dr, dc) in plan:
                    r, c = find_blank(current)
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 3 and 0 <= nc < 3:
                        new_state = [row[:] for row in current]
                        new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                        solution.append(new_state)
                        current = new_state
        elif selected_algorithm_name in ["Sensorless BFS", "Genetic Algorithm"]:
            #solution = sensorless_bfs(start_state, goal_state)
            if not (isinstance(start_state, list) and len(start_state) == 3 and
                    all(isinstance(row, list) and len(row) == 3 for row in start_state)):
                solution = []
            elif not is_solvable(start_state):
                print("Puzzle is unsolvable")
                solution = []
            else:
                solution = sensorless_bfs(start_state, goal_state)
        elif selected_algorithm_name == "Q-learning":
            agent.train(start_state, goal_state)
            solution = agent.solve(start_state, goal_state)
        else:
            solution = selected_algorithm_func(start_state, goal_state)
        end_time = time.time()
        solve_time = end_time - start_time
        so_buoc_value = str(len(solution) - 1) if solution else "Not found"
        solution_path = solution

running = True
while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dropdown_rect.collidepoint(event.pos):
                dropdown_open = not dropdown_open
            elif dropdown_open:
                for i, option in enumerate(dropdown_options):
                    rect = dropdown_options_rects[i]
                    if rect.collidepoint(event.pos):
                        selected_algorithm_name = option
                        selected_algorithm_func = algorithms.get(option)
                        dropdown_open = False
                        solution_path = []
                        animation_step = 0
                        thoi_gian_value = "0.00 s"
                        so_buoc_value = "0"
                        solving = False
                        start_state = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
                        #start_state = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
                        #start_state = [[2, 3, 6], [1, 5, 0], [4, 7, 8]]

                        active_button = None
                        agent.trained = False
                        break
            elif nhap_radio_rect.collidepoint(event.pos):
                selected_input_method = "Input"
                start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
                agent.trained = False
            elif random_radio_rect.collidepoint(event.pos):
                selected_input_method = "Random"
                start_state = generate_random_puzzle()
                agent.trained = False
            elif button_run_rect.collidepoint(event.pos):
                active_button = "run"
                start_solving()
            elif button_stop_rect.collidepoint(event.pos):
                active_button = "stop"
                solving = not solving
            elif button_exit_rect.collidepoint(event.pos):
                active_button = "exit"
                running = False
    if solving and solution_path and animation_step < len(solution_path):
        if current_time - last_animation_time > animation_delay:
            start_state = solution_path[animation_step]
            animation_step += 1
            last_animation_time = current_time
            elapsed_time = current_time - animation_start_time
            thoi_gian_value = f"{elapsed_time:.2f} s"
    draw_gui()

pygame.quit()
sys.exit()