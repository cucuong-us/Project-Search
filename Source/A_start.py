import time
import heapq
import tracemalloc

class Node:
    def __init__(self, ares_x, ares_y, stones, grid, switches, parent=None, action=None, cost=0):
        self.ares_x = ares_x
        self.ares_y = ares_y
        self.stones = stones
        self.grid = grid
        self.switches = switches  # Thêm vị trí công tắc
        self.parent = parent
        self.action = action
        self.cost = cost
        self.total_cost = cost if parent is None else parent.total_cost + cost 

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def is_goal(self):
        return all(self.grid[x][y] == '*' for x, y in self.stones)

    def get_neighbors(self, stone_weights):
        neighbors = []
        directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]
        for dx, dy, move, push in directions:
            new_x = self.ares_x + dx
            new_y = self.ares_y + dy
            # Di chuyển tự do
            if self.grid[new_x][new_y] in [' ', '.']:
                new_node = self.clone()
                new_node.move(new_x, new_y, move)
                neighbors.append((new_node, 1))
            # Đẩy đá
            elif self.grid[new_x][new_y] == '$' or self.grid[new_x][new_y] == '*':
                stone_weight = stone_weights[self.stones.index((new_x, new_y))]
                behind_stone_x = new_x + dx
                behind_stone_y = new_y + dy
                if self.grid[behind_stone_x][behind_stone_y] in [' ', '.']:
                    new_node = self.clone()
                    new_node.push_stone(new_x, new_y, behind_stone_x, behind_stone_y, push)
                    push_cost = 1 + stone_weight
                    neighbors.append((new_node, push_cost))
        return neighbors

    def clone(self):
        return Node(self.ares_x, self.ares_y, self.stones.copy(), [row.copy() for row in self.grid], self.switches, self, self.action, self.cost)

    def move(self, new_x, new_y, action):
        self.grid[self.ares_x][self.ares_y] = ' ' if self.grid[self.ares_x][self.ares_y] == '@' else '.'
        self.grid[new_x][new_y] = '@' if self.grid[new_x][new_y] == ' ' else '+'
        self.ares_x = new_x
        self.ares_y = new_y
        self.action = action

    def push_stone(self, stone_x, stone_y, new_stone_x, new_stone_y, action):
        self.grid[self.ares_x][self.ares_y] = ' ' if self.grid[self.ares_x][self.ares_y] == '@' else '.'
        self.grid[stone_x][stone_y] = '@' if self.grid[stone_x][stone_y] == '$' else '+'
        self.grid[new_stone_x][new_stone_y] = '$' if self.grid[new_stone_x][new_stone_y] == ' ' else '*'
        self.stones[self.stones.index((stone_x, stone_y))] = (new_stone_x, new_stone_y)
        self.ares_x = stone_x
        self.ares_y = stone_y
        self.action = action

    def get_solution(self):
        solution = []
        node = self
        while node.parent is not None:
            solution.append(node.action)
            node = node.parent
        return ''.join(reversed(solution))

    def heuristic(self):
        total_distance = 0
        for stone_x, stone_y in self.stones:
            min_distance = float('inf')
            # Tìm công tắc gần nhất với viên đá hiện tại
            for switch_x, switch_y in self.switches:
                distance = abs(stone_x - switch_x) + abs(stone_y - switch_y)
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance  # Cộng khoảng cách tối thiểu của mỗi viên đá đến công tắc
        return total_distance

def move_position(x, y, direction):
    if direction == 'u':
        return x - 1, y
    elif direction == 'd':
        return x + 1, y
    elif direction == 'l':
        return x, y - 1
    elif direction == 'r':
        return x, y + 1
    return x, y

def calculate_total_cost(final_path, ares_start_x, ares_start_y, stone_weights, stones):
    total_cost = 0
    current_x, current_y = ares_start_x, ares_start_y
    stone_positions = stones.copy()
    for action in final_path:
        if action in ['u', 'd', 'l', 'r']:
            new_x, new_y = move_position(current_x, current_y, action)
            current_x, current_y = new_x, new_y
        elif action in ['U', 'D', 'L', 'R']:
            stone_direction = action.lower() 
            stone_x, stone_y = move_position(current_x, current_y, stone_direction) 
            stone_weight = stone_weights[stone_positions.index((stone_x, stone_y))]
            total_cost += stone_weight
            new_stone_x, new_stone_y = move_position(stone_x, stone_y, stone_direction)
            stone_positions[stone_positions.index((stone_x, stone_y))] = (new_stone_x, new_stone_y)
            current_x, current_y = stone_x, stone_y
    return total_cost

def a_star_search(start_node, stone_weights):
    frontier = []
    heapq.heappush(frontier, (0, start_node.total_cost + start_node.heuristic(), start_node))
    
    explored = {} 
    node_count = 0
    tracemalloc.start()
    start_time = time.process_time()
    
    while frontier:
        us_cost,current_total_cost, current_node = heapq.heappop(frontier)

        # Kiểm tra điều kiện đích
        if current_node.is_goal():
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            time_taken = (time.process_time() - start_time) * 1000
            memory_used = peak / 10**6
            return current_node, node_count, time_taken, memory_used

        # Đại diện trạng thái với vị trí Ares và các viên đá
        state = tuple(current_node.stones + [(current_node.ares_x, current_node.ares_y)])

        # Kiểm tra nếu trạng thái chưa được thăm hoặc có chi phí thấp hơn
        if state not in explored or current_total_cost < explored[state]:
            explored[state] = current_total_cost  # Cập nhật chi phí mới thấp hơn

            # Mở rộng các trạng thái con
            for neighbor, cost in current_node.get_neighbors(stone_weights):
                new_cost = us_cost + cost
                heapq.heappush(frontier, (new_cost, new_cost + neighbor.heuristic(), neighbor))
                node_count += 1

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time_taken = (time.process_time() - start_time) * 1000
    memory_used = peak / 10**6
    return None, node_count, time_taken, memory_used

def read_maze(filename):
    with open(filename, 'r') as file:
        stone_weights = list(map(int, file.readline().strip().split()))
        grid = []
        stones = []
        switches = []  # Thêm danh sách công tắc
        ares_x, ares_y = None, None
        for i, line in enumerate(file):
            grid.append(list(line.rstrip()))
            for j, char in enumerate(line.rstrip()):
                if char == '@' or char == '+':
                    ares_x, ares_y = i, j
                if char == '$' or char == '*':
                    stones.append((i, j))
                if char == '.' or char == '+' or char == '*':
                    switches.append((i, j))  # Lưu vị trí công tắc
        return stone_weights, grid, ares_x, ares_y, stones, switches  # Trả về vị trí công tắc
def write_output(filename, algorithm_name, steps, total_weight, node_count, time_taken, memory_used, solution):
    with open(filename, 'a+') as file:
        file.write(f"{algorithm_name}\n")
        file.write(f"Steps: {steps}, Weight: {total_weight}, Node: {node_count}, Time (ms): {time_taken:.2f}, Memory (MB): {memory_used:.2f}\n")
        file.write(f"{solution}\n")

def solve_as(input_file, output_file):
    # Đọc input từ file
    stone_weights, grid, ares_x, ares_y, stones, switches = read_maze(input_file)
    # Khởi tạo node bắt đầu
    start_node = Node(ares_x, ares_y, stones, grid, switches)
    # Thực hiện UCS
    goal_node, node_count, time_taken, memory_used = a_star_search(start_node, stone_weights)
    if goal_node:
        steps = len(goal_node.get_solution())
        solution = goal_node.get_solution()
        #switch_positions = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == '.']
        total_weight = calculate_total_cost(solution, ares_x, ares_y, stone_weights, stones)
        # Ghi output
        write_output(output_file, 'A*', steps, total_weight, node_count, time_taken, memory_used, solution)
        print(f"Solution written to {output_file}")
    else:
        print("No solution")
        write_output(output_file, 'A*', 0, 0, node_count, time_taken, memory_used, "No solution")
        
