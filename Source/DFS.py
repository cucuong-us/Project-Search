import time
import sys
import copy

class Game:
    # Khởi tạo ma trận và trạng thái ban đầu của trò chơi
    def __init__(self, matrix):
        self.path_sol = ""
        self.stack = []
        self.matrix = matrix
    
    # Trả về ma trận trạng thái hiện tại của trò chơi
    def get_matrix(self):
        return self.matrix
    
    # Trả về nội dung tại vị trí (x, y) trong ma trận
    def get_content(self, x, y):
        return self.matrix[y][x]
    
    # Đặt nội dung tại vị trí (x, y) trong ma trận
    def set_content(self, x, y, content):
        self.matrix[y][x] = content

    # Tìm và trả về vị trí của Ares trong ma trận
    def Ares_pos(self):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                pos_content = self.get_content(x, y)
                if pos_content == '@' or pos_content == '+':
                    return (x, y, pos_content)
        return None
    
    # Tìm và trả về danh sách vị trí của các viên đá trong ma trận
    def stones_pos(self):
        stones_pos = []
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                pos_content = self.get_content(x, y)
                if pos_content == '$' or pos_content == '*':
                    stones_pos.append((x, y, pos_content))
        return stones_pos
    
    # Tìm và trả về danh sách vị trí của các công tắc trong ma trận
    def switches_pos(self):
        switches_pos = []
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                pos_content = self.get_content(x, y)
                if pos_content == '.' or pos_content == '+' or pos_content == '*':
                    switches_pos.append((x, y, pos_content))
        return switches_pos

    # Trả về nội dung tại vị trí tiếp theo của Ares sau khi di chuyển
    def next(self, x, y):
        return self.get_content(self.Ares_pos()[0] + x, self.Ares_pos()[1] + y)

    # Kiểm tra xem trò chơi đã hoàn thành hay chưa
    def is_completed(self):
        for pos in self.switches_pos():
            if self.get_content(pos[0], pos[1]) != '*':
                return False
        return True

    # Kiểm tra xem Ares có thể di chuyển đến vị trí (x, y) hay không
    def can_move(self, x, y):
        return self.get_content(self.Ares_pos()[0] + x, self.Ares_pos()[1] + y) not in ['#', '$', '*']
        
    # Kiểm tra xem Ares có thể đẩy viên đá đến vị trí (x, y) hay không
    def can_push(self, x, y):
        return (self.next(x, y) in ['$', '*'] and self.next(x*2, y*2) in [' ', '.'])
    
    # Di chuyển Ares đến vị trí (x, y) nếu có thể
    # Dùng biến save để quyết định có lưu lại hành động vào ngăn xếp hay không
    # save = true, bước di chuyển sẽ đươc lưu vào ngăn xếp để có thể theo dõi lại các hành động đã thực hiện
    # => có thể quau lui khi cần thiết để tìm ra giải pháp
    def move(self, x, y, save):
        if self.can_move(x, y):
            current = self.Ares_pos()
            future = self.next(x, y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save:
                    self.stack.append((x, y, False))
            elif current[2] == '@' and future == '.':
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save:
                    self.stack.append((x, y, False))
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save:
                    self.stack.append((x, y, False))
            elif current[2] == '+' and future == '.':
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save:
                    self.stack.append((x, y, False))

    # Đẩy viên đá từ vị trí (x, y) đến vị trí (x + a, y + b)
    def push_stone(self, x, y, a, b):
        current_stone = self.get_content(x, y)
        future_stone = self.get_content(x + a, y + b)

        if current_stone == '$':
            self.set_content(x, y, ' ')
            if future_stone == '.':
                self.set_content(x + a, y + b, '*')
            elif future_stone == ' ':
                self.set_content(x + a, y + b, '$')
        elif current_stone == '*':
            self.set_content(x, y, '.')
            if future_stone == '.':
                self.set_content(x + a, y + b, '*')
            elif future_stone == ' ':
                self.set_content(x + a, y + b, '$')

    # Ares đẩy đá nếu có thể
    # Ý tưởng dùng biến save tương tự như def move(self, x, y, save):
    def push(self, x, y, save):
        if self.can_push(x, y):
            current = self.Ares_pos()
            future = self.next(x, y)
            future_stone = self.next(x*2, y*2)
            if current[2] == '@' and future == '$' and future_stone in [' ', '.']:
                self.push_stone(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save:
                    self.stack.append((x, y, True))
            elif current[2] == '@' and future == '*' and future_stone in [' ', '.']:
                self.push_stone(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save:
                    self.stack.append((x, y, True))
            elif current[2] == '+' and future == '$' and future_stone in [' ', '.']:
                self.push_stone(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save:
                    self.stack.append((x, y, True))
            elif current[2] == '+' and future == '*' and future_stone in [' ', '.']:
                self.push_stone(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save:
                    self.stack.append((x, y, True))

# -----------------------------------------------------------------------------------

# Hàm kiểm tra các bước di chuyển hợp lệ
def valid_move(state):
    x = 0
    y = 0
    move = []
    for step in ['u', 'd', 'l', 'r']:
        if step == 'u':
            x = 0
            y = -1
        elif step == 'd':
            x = 0
            y = 1
        elif step == 'l':
            x = -1
            y = 0
        elif step == 'r':
            x = 1
            y = 0

        if state.can_move(x, y):
            move.append(step)

    return move

# Hàm kiểm tra các bước đẩy hợp lệ
def valid_push(state):
    x = 0
    y = 0
    push = []
    for step in ['U', 'D', 'L', 'R']:
        if step == 'U':
            x = 0
            y = -1
        elif step == 'D':
            x = 0
            y = 1
        elif step == 'L':
            x = -1
            y = 0
        elif step == 'R':
            x = 1
            y = 0

        if state.can_push(x, y):
            push.append(step)

    return push

# Kiểm tra trạng thái hiện tại có bị deadlock hay không
def is_deadlock(state):
    for stone in state.stones_pos():
        if stone[2] == '$':
            x = stone[0]
            y = stone[1]

            # Corner up-left
            if state.get_content(x, y-1) in ['#', '$', '*'] and state.get_content(x-1, y) in ['#', '$', '*']:
                if state.get_content(x-1, y-1) in ['#','$','*']:
                    return True
                if state.get_content(x, y-1) == '#' and state.get_content(x-1, y) == '#':
                    return True
                if state.get_content(x, y-1) in ['$', '*'] and state.get_content(x-1, y) in ['$', '*']:
                    if state.get_content(x+1, y-1) == '#' and state.get_content(x-1, y+1) == '#':
                        return True
                if state.get_content(x, y-1) in ['$', '*'] and state.get_content(x-1, y) == '#':
                    if state.get_content(x+1, y-1) == '#':
                        return True
                if state.get_content(x, y-1) == '#' and state.get_content(x-1, y) in ['$', '*']:
                    if state.get_content(x-1, y+1) == '#':
                        return True
                    
            # Corner up-right
            if state.get_content(x, y-1) in ['#', '$', '*'] and state.get_content(x+1, y) in ['#', '$', '*']:
                if state.get_content(x+1, y-1) in ['#', '$', '*']:
                    return True
                if state.get_content(x, y-1) == '#' and state.get_content(x+1, y) == '#':
                    return True
                if state.get_content(x, y-1) in ['$', '*'] and state.get_content(x+1, y) in ['$', '*']:
                    if state.get_content(x-1, y-1) == '#' and state.get_content(x+1, y+1) == '#':
                        return True
                if state.get_content(x, y-1) in ['$', '*'] and state.get_content(x+1, y) == '#':
                    if state.get_content(x-1, y-1) == '#':
                        return True
                if state.get_content(x, y-1) == '#' and state.get_content(x+1, y) in ['$', '*']:
                    if state.get_content(x+1, y+1) == '#':
                        return True


            # Corner down-left
            elif state.get_content(x, y+1) in ['#', '$', '*'] and state.get_content(x-1, y) in ['#', '$', '*']:
                if state.get_content(x-1, y+1) in ['#', '$', '*']:
                    return True
                if state.get_content(x, y+1) == '#' and state.get_content(x-1,y) == '#':
                    return True
                if state.get_content(x, y+1) in ['$', '*'] and state.get_content(x-1,y) in ['$', '*']:
                    if state.get_content(x-1, y-1) == '#' and state.get_content(x+1, y+1) == '#':
                        return True
                if state.get_content(x, y+1) in ['$', '*'] and state.get_content(x-1, y) == '#':
                    if state.get_content(x+1, y+1) == '#':
                        return True
                if state.get_content(x, y+1) == '#' and state.get_content(x-1, y) in ['$', '*']:
                    if state.get_content(x-1, y-1) == '#':
                        return True
                    

            # Corner down-right
            elif state.get_content(x, y+1) in ['#', '$', '*'] and state.get_content(x+1, y) in ['#', '$', '*']:
                if state.get_content(x+1, y+1) in ['#', '$', '*']:
                    return True
                if state.get_content(x, y+1) == '#' and state.get_content(x+1, y) == '#':
                    return True
                if state.get_content(x, y+1) in ['$', '*'] and state.get_content(x+1, y) in ['$', '*']:
                    if state.get_content(x-1, y+1) == '#' and state.get_content(x+1, y-1) == '#':
                        return True
                if state.get_content(x, y+1) in ['$', '*'] and state.get_content(x+1, y) == '#':
                    if state.get_content(x-1, y+1) == '#':
                        return True
                if state.get_content(x, y+1) == '#' and state.get_content(x+1, y) in ['$', '*']:
                    if state.get_content(x+1, y-1) == '#':
                        return True
                
    return False

# -----------------------------------------------------------------------------------

# Hàm đọc file input từ thư mục Input
def read_input(file_path):
    with open(file_path, 'r') as f:
        data = f.read().splitlines()

    stones = list(map(int, data[0].split()))
    matrix = []
    for i in range(1, len(data)):
        matrix.append(list(data[i]))

    return stones, matrix

# Hàm ghi kết quả vào file output
def write_output(file_path, algorithm, steps, weight, nodes, time, memory, path_sol):
    with open(file_path, 'a+') as f:
        f.write(f'{algorithm}\n')
        f.write(f'Steps: {steps}, ')
        f.write(f'Weight: {weight}, ')
        f.write(f'Node: {nodes}, ')
        f.write(f'Time (ms): {round(time, 2)}, ')
        f.write(f'Memory (MB): {round(memory, 2)}\n')
        f.write(f'{path_sol}\n')

# -----------------------------------------------------------------------------------

# Tính toán tổng trọng lượng mà Ares đã đẩy các viên đá dựa trên đường đi
def calculate_weight(stones_weight, path_sol, matrix):
    input_matrix = copy.deepcopy(matrix)
    game = Game(input_matrix)
    weight = 0

    # Tạo từ điển lưu vị trí và trọng lượng của các viên đá
    stones_pos_weight = {(x, y): stones_weight[i] for i, (x, y, _) in enumerate(game.stones_pos())}

    for step in path_sol:
        if step == 'u':
            game.move(0, -1, False)
        elif step == 'd':
            game.move(0, 1, False)
        elif step == 'l':
            game.move(-1, 0, False)
        elif step == 'r':
            game.move(1, 0, False)
        elif step == 'U':
            ares_pos = game.Ares_pos()
            stone_pos = (ares_pos[0], ares_pos[1] - 1)
            if stone_pos in stones_pos_weight:
                weight += stones_pos_weight[stone_pos]
                new_stone_pos = (stone_pos[0], stone_pos[1] - 1)
                stones_pos_weight[new_stone_pos] = stones_pos_weight.pop(stone_pos)
            game.push(0, -1, False)
        elif step == 'D':
            ares_pos = game.Ares_pos()
            stone_pos = (ares_pos[0], ares_pos[1] + 1)
            if stone_pos in stones_pos_weight:
                weight += stones_pos_weight[stone_pos]
                new_stone_pos = (stone_pos[0], stone_pos[1] + 1)
                stones_pos_weight[new_stone_pos] = stones_pos_weight.pop(stone_pos)
            game.push(0, 1, False)
        elif step == 'L':
            ares_pos = game.Ares_pos()
            stone_pos = (ares_pos[0] - 1, ares_pos[1])
            if stone_pos in stones_pos_weight:
                weight += stones_pos_weight[stone_pos]
                new_stone_pos = (stone_pos[0] - 1, stone_pos[1])
                stones_pos_weight[new_stone_pos] = stones_pos_weight.pop(stone_pos)
            game.push(-1, 0, False)
        elif step == 'R':
            ares_pos = game.Ares_pos()
            stone_pos = (ares_pos[0] + 1, ares_pos[1])
            if stone_pos in stones_pos_weight:
                weight += stones_pos_weight[stone_pos]
                new_stone_pos = (stone_pos[0] + 1, stone_pos[1])
                stones_pos_weight[new_stone_pos] = stones_pos_weight.pop(stone_pos)
            game.push(1, 0, False)

    return weight

def DFS(game):
    # Các biến để theo dõi 
    node_generated = 0  # số lượng node được tạo
    time_exe = 0        # thời gian thực thi
    memory = 0          # bộ nhớ sử dụng
    path_sol = ""       # đường đi giải pháp

    # Lưu lại thời gian bắt đầu thuật toán
    start = time.time()

    # Tạo bản copy của trạng thái trò chơi ban đầu
    state = copy.deepcopy(game)
    node_generated += 1
    
    # Kiểm tra trạng thái ban đầu bị deadlock hay không
    if is_deadlock(state):
        end = time.time()
        time_exe = (end - start) * 1000
        path_sol = "No solution"
        return node_generated, time_exe, memory, path_sol
    
    # Khởi tạo danh sách các trạng thái cần khám phá 
    state_set = []
    state_set.append(state)

    # Tập hợp các trạng thái đã khám phá
    state_explored = set()

    while state_set:
        # Lấy trạng thái hiện tại từ danh sách các trạng thái cần khám phá
        current_state = state_set.pop()
        
        # Lấy các bước di chuyển và đẩy hợp lệ từ trạng thái hiện tại
        move = valid_move(current_state)
        push = valid_push(current_state)

        # Thêm trạng thái hiện tại vào tập hợp các trạng thái đã khám phá
        state_explored.add(tuple(map(tuple, current_state.get_matrix())))

        # Duyệt qua các bước di chuyển và đẩy hợp lệ
        for step in push + move:
            # Tạo một bản copy của trạng thái hiện tại
            new_state = copy.deepcopy(current_state)
            node_generated += 1

            # Thực hiện bước di chuyển hoặc đẩy tương ứng
            if step == 'u':
                new_state.move(0, -1, False)
            elif step == 'd':
                new_state.move(0, 1, False)
            elif step == 'l':
                new_state.move(-1, 0, False)
            elif step == 'r':
                new_state.move(1, 0, False)
            elif step == 'U':
                new_state.push(0, -1, False)
            elif step == 'D':
                new_state.push(0, 1, False)
            elif step == 'L':
                new_state.push(-1, 0, False)
            elif step == 'R':
                new_state.push(1, 0, False)

            # Cập nhật đường đi giải pháp
            new_state.path_sol += step

            # Kiểm tra nếu trạng thái mới là trạng thái hoàn thành
            if new_state.is_completed():
                end = time.time()
                time_exe = (end - start) * 1000
                memory = (sys.getsizeof(state_set) + sys.getsizeof(state_explored)) / (1024 * 1024)
                path_sol = new_state.path_sol
                return node_generated, time_exe, memory, path_sol
            
            # Nếu trạng thái mới chưa được khám phá và không bị deadlock
            # => thêm nó vào danh sách các trạng thái cần khám phá
            if (tuple(map(tuple, new_state.get_matrix())) not in state_explored) and (not is_deadlock(new_state)):
                state_set.append(new_state)

    # Nếu không tìm thấy giải pháp, tính toán thời gian và bộ nhớ sử dụng
    end = time.time()
    time_exe = (end - start) * 1000
    memory = (sys.getsizeof(state_set) + sys.getsizeof(state_explored)) / (1024 * 1024)
    return node_generated, time_exe, memory, path_sol

# -----------------------------------------------------------------------------------

def main(input_file_path, output_file_path):
    stones_weights, matrix = read_input(input_file_path)

    game = Game(matrix)

    node_generated, time_exe, memory, path_sol = DFS(game)

    steps = 0
    if path_sol != "No solution":
        if path_sol == '':
            path_sol = "No solution"
        else:
            steps = len(path_sol)

    weight = calculate_weight(stones_weights, path_sol, matrix)

    write_output(output_file_path, 'DFS', steps, weight, node_generated, time_exe, memory, path_sol)

# -----------------------------------------------------------------------------------