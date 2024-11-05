import copy
import itertools
import time
import tkinter.filedialog
import tracemalloc
from collections import deque


# Hàm tạo các hoán vị
# input: iterable object
# ouput: một list hoán vị mới
def permute(a):
    """
    (iterable object) -> Danh sách các hoán vị của input object
    Hàm nhận vào một kiểu dữ liệu có thứ tự a và trả về danh sách các hoán vị của vật đó
    """
    # Sử dụng itertools.permutations để tạo ra các hoán vị
    return [list(p) for p in itertools.permutations(a)]


# Đọc dữ liệu
# input: đường dẫn tới tệp tin
# ouput: Trả về một list 2 chiều map_2d chứa biểu diễn map, một list trọng lượng của các hòn đá
def read_map_file(filename):
    """
    (filename:str) -> rocks:list, map_2d: list of list
    Đọc dữ liệu từ đường dẫn filename đầu vào và trả về danh sách các cân nặng của từng hòn đá, kiểu của mỗi cân nặng là str,
    trả về list of list ma trận 2 chiều chứa bản đồ, mỗi ký tự trong bản đồ là kiểu str
    """
    map_2d = []
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if i == 0:  # Bỏ qua dòng đầu tiên
                rocks = line.strip("\n").split(" ")
                continue
            # Loại bỏ ký tự xuống dòng và chuyển dòng thành danh sách các ký tự
            map_2d.append(list(line.strip("\n")))
    return rocks, map_2d


# Ghi dữ liệu
# input: Tên file để ghi dữ liệu vào và chuỗi data chứa dữ liệu cần ghi
# output: Số bytes đã ghi vào file
def write_data(filename, data):
    """
    (filename:str, data: str) -> số bytes đã ghi: int
    Ghi dữ liệu data vào file có tên là filename trong thư mục hiện tại
    """
    with open(filename, "a+") as file:
        bytes = file.write(data)

    return bytes


# BFS


# Tìm vị trí bắt đầu của Arex
# input: bản đồ list of list
# output: vị trí i, j, đây là tọa độ của Arex đang đứng
def find_arex(map_data):
    """
    (map_data: list of list) -> i, j: int, int
    Đọc dữ liệu map_data và trả về tọa độ vị trí đứng của Arex (tọa độ này theo chỉ số của ma trận map_data)
    """
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == "@" or map_data[i][j] == "+":
                return i, j


# BFS để tìm điểm ra tọa độ các hòn đá và các cần gạt
# input: bản đồ map_2d, vị trí bắt đầu x start_i, vị trí bắt đầu y start_y, goal_num: số lượng trọng số của các hòn đá
# output: Số lượng node được nằm trong trong list expanded nodes, một list chứa các tuple tọa độ của hòn đá,
# một list chứa các tuple tọa độ của switches
def bfs_find_origin(map_2d, start_i, start_j, goal_num):
    """
    (map_2d: list of list, start_i: int, start_j: int, goal_num: int) -> số node trong expanded nodes, stones: list of tuple, switches: list of tuple
    Hàm đọc map map_2d, vị trí bắt đầu start_i, start_j của Arex và số lượng hòn đá goal_num cần phải tìm, sau đó trả về số lượng nodes trong expanded nodes
    list các tọa độ của hòn đá, list các tọa độ của cần gạt
    """
    # Kích thước của bản đồ
    m = len(map_2d)
    n = 0
    for r in map_2d:
        if n < len(r):
            n = len(r)
    # 4 hướng di chuyển: lên, xuống, trái, phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Giới thiệu về deque
    # deque là double-ended queue: một cấu trúc cho phép thêm xóa ở 2 đầu danh sách một cách hiệu quả

    # append(x): Thêm x vào cuối deque.
    # appendleft(x): Thêm x vào đầu deque.
    # pop(): Xóa và trả về phần tử cuối cùng của deque.
    # popleft(): Xóa và trả về phần tử đầu tiên của deque.
    # extend(iterable): Thêm tất cả các phần tử trong iterable vào cuối deque.
    # extendleft(iterable): Thêm tất cả các phần tử trong iterable vào đầu deque (lưu ý rằng phần tử được thêm theo thứ tự ngược lại).

    # Hàng đợi BFS
    queue = deque([(start_i, start_j)])
    # expanded nodes
    explored = []
    # Đánh dấu các ô đã thăm, ma trận m x n visited với mỗi phần tử được khởi tạo là kiểu False
    visited = [[False for _ in range(n)] for _ in range(m)]
    visited[start_i][start_j] = True
    # 2 list chứa tọa độ các hòn đá và cần gạt
    stones = []
    switches = []
    if map_2d[start_i][start_j] == "+":
        switches.append((start_i, start_j))
    # BFS
    while queue:
        # Lấy ra khỏi hàng đợi và thêm vào expanded nodes
        x, y = queue.popleft()
        explored.append((x, y))

        # Duyệt qua 4 hướng
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Kiểm tra nếu ô mới nằm trong bản đồ và chưa được thăm
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                # Kiểm tra nếu có thể đi qua ô đó (ví dụ, ô không phải là tường '#')
                if map_2d[nx][ny] != "#":
                    # Cập nhật là vị trí này đã thăm
                    visited[nx][ny] = True
                    # Nếu là hòn đá thì thêm tọa độ vào list stones
                    if map_2d[nx][ny] == "$":
                        stones.append((nx, ny))
                    elif map_2d[nx][ny] == "*":
                        stones.append((nx, ny))
                        switches.append((nx, ny))
                    # Nếu là cần gạt thì thêm tọa độ vào list switches
                    elif map_2d[nx][ny] == "." or map_2d[nx][ny] == "+":
                        switches.append((nx, ny))
                    # Hàm kiểm tra đã đạt được mục tiêu chưa (giống hàm isGoal() trong mã giả file lý thuyết)
                    if (
                        len(switches) == goal_num and len(stones) == goal_num
                    ):  # Khi số lượng hòn đá và cần gạt đúng bằng số lượng trọng số của goal_num thì dừng
                        return len(explored), stones, switches
                    # Thêm child vào queue
                    queue.append((nx, ny))

    return len(explored), stones, switches


# BFS để tìm đường đi từ hòn đá tới switch sao cho đường đi này arex có thể đẩy hòn đá được
# input: bản đồ map_2d, vị trí bắt đầu của hòn đá (start_i, start_j), goal: một list các cần gạt
# (chỉ cần đến được tọa độ của một trong nhiều cần gạt là đạt được mục tiêu)
# output: trả về một list parent: dùng để truy vết tìm ra đường đi đầu và cuối, len(explored): số node trong expanded nodes
def bfs_from_rock_to_switches(map_2d, start_i, start_j, goal: list):
    # Loại vị trí hòn đá đang xét đường đi trên bản đồ, mục đích là để đi khỏi bị cản bởi chính nó
    map_2d[start_i][start_j] = " "
    # Kích thước của bản đồ
    m = len(map_2d)
    n = 0
    for r in map_2d:
        if n < len(r):
            n = len(r)

    # 4 hướng di chuyển: lên, xuống, trái, phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # 4 vị trí để hòn đá có thể được đẩy: đằng sau hòn đá, phía trên hòn đá, bên phải hòn đá, bên trái hòn đá
    push_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Điểm bắt đầu
    start = (start_i, start_j)
    # Nếu điểm bắt đầu của hòn đá là một trong các điểm đích (tọa độ của cần gạt)
    # thì thoát
    if start == goal[0]:
        goal.remove(start)
        return 0, {start: None}
    # Tạo một queue
    queue = deque([start])
    # Tạo expanded nodes
    explored = []
    # Đánh dấu các ô đã thăm, ma trận m x n visited với mỗi phần tử được khởi tạo là kiểu False
    visited = [[False for _ in range(n)] for _ in range(m)]
    visited[start_i][start_j] = True
    # list dùng để truy vết
    parent = {start: None}  # Để lưu vị trí cha

    # BFS
    while queue:
        # Lấy ra khỏi hàng đợi và thêm vào expanded nodes
        x, y = queue.popleft()
        explored.append((x, y))

        # Duyệt qua 4 hướng mà hòn đá có thể đi, 4 vị trí để có thể đẩy hòn đá theo 4 hướng đó
        for i in range(len(directions)):
            dx, dy = directions[i]
            ax, ay = push_directions[i]
            nx, ny = x + dx, y + dy
            arex_x, arex_y = x + ax, y + ay

            # Kiểm tra nếu ô mới nằm trong bản đồ và chưa được thăm
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                # Kiểm tra hòn đá có thể đi qua ô đó
                if (
                    map_2d[nx][ny] != "#"  # ô đó không phải là tường
                    and (
                        map_2d[nx][ny] != "$" and map_2d[nx][ny] != "*"
                    )  # ô đó không phải là hòn đá khác
                    and map_2d[arex_x][arex_y]
                    != "#"  # Vị trí để có thể đẩy hòn đá theo một hướng, vị trí này không phải tường
                    and (
                        map_2d[arex_x][arex_y] != "$" and map_2d[arex_x][arex_y] != "*"
                    )  # Vị trí để có thể đẩy hòn đá theo một hướng, vị trí này không phải hòn đá khác
                ):
                    # Cập nhật là vị trí này đã thăm
                    visited[nx][ny] = True
                    # lưu vết
                    parent[(nx, ny)] = (x, y)
                    # Nếu hòn đá đã tới được vị trí của cần gạt đầu tiên
                    if (nx, ny) == goal[0]:
                        goal.remove(
                            (nx, ny)
                        )  # Vị trí cần gạt này đã được lắp đầy, vì vậy loại tọa độ này ra
                        map_2d[start_i][start_j] = "$"
                        return len(explored), parent  # Trả về kết quả
                    queue.append((nx, ny))

    # Nếu đi không thành công thì gán lại hòn đá về vị trí ban đầu
    map_2d[start_i][start_j] = "$"
    return (
        len(explored),
        parent,
    )  # Nếu không có kết quả, vẫn trả về để tính số node đã được nằm trong expanded nodes


# Dùng để tìm đường đi từ hòn đá tới cách cần gạt
# input: bản đồ, list các hòn đá, list các cần gạt
# output: số node đã mở khi tìm đường đi, list of list all_paths của các đường đi: với mỗi phần tử
# là một list chứa đường đi từ tọa độ một hòn đá tới tọa độ một cần gạt
def find_paths_for_rocks_to_switches(map_data, rocks, switches):
    # Tạo một bản deep copy của list switches
    new_switches = switches[:]
    # Chứa các đường đi của hòn đá tới cần gạt
    all_paths = []
    # Để tính tổng số node
    nodes = 0
    # Với mỗi tọa độ của hòn đá
    for x, y in rocks:
        # Trả về số node và list parent để truy vết
        nodes, parent = bfs_from_rock_to_switches(map_data, x, y, new_switches)
        # Sau khi chạy hàm bfs_from_rock_to_switches, nếu có đường đi thì new_switches sẽ mất đi một cần gạt
        # current_pos: set, sẽ chứa cần gạt bị xóa đó
        current_pos = set(switches).difference(set(new_switches))
        # Nếu tồn tại current_pos thì nghĩa là có đường đi từ hòn đá tới cần gạt current_pos
        if current_pos:
            # do current_pos sẽ trả về một set nhiều phần tử, ta sẽ lấy phần tử đầu tiên
            current_pos = next(iter(current_pos))
            switches.remove(current_pos)
            # Nếu tìm được đường đi rồi thì vị trí của hòn đá sẽ bị xóa đi, để trống
            map_data[x][y] = " "
            # Vị trí của cần gạt sẽ bị hòn đá lấp vào
            map_data[current_pos[0]][current_pos[1]] = "$"
            # Truy vết để lấy đường đi và lưu vào path
            path = []
            while current_pos is not None:
                path.append(current_pos)
                current_pos = parent[current_pos]
            path.reverse()  # Đảo ngược đường đi để từ start đến goal
            # Lưu vào all_paths
            all_paths.append(path)

    return nodes, all_paths


# Mục đích dùng để xáo trộn trình tự hòn đá và trình tự cần gạt để xét được mọi đường đi từ đá tới cần gạt
# input: bản đồ, list các hòn đá, list các cần gạt
# output: bool type chỉ có tìm được đường đi cho mọi cục đá tới cần gạt tương ứng không,
# số node trong expanded nodes, list of list đường đi từ cục đá tới cần gạt
def swap_the_rock(map_data, rocks, switches, start_i, start_j):
    # list of list hoán vị của list rocks và list switches
    permutetation_of_rocks = permute(rocks)
    permutetation_of_switches = permute(switches)
    total_nodes = 0
    # Duyệt qua từng hoán vị
    for permuted_switches in permutetation_of_switches:
        for permuted_rocks in permutetation_of_rocks:
            all_paths = []
            answer = []
            new_map = copy.deepcopy(map_data)
            new_switches = permuted_switches[:]
            nodes, all_paths = find_paths_for_rocks_to_switches(
                new_map, permuted_rocks, new_switches
            )
            total_nodes += nodes
            # nếu số đường đi tìm được bằng số hòn đá thì thành công
            if len(all_paths) == len(rocks):
                for i in all_paths:
                    if len(i) == 1:
                        all_paths.remove(i)

                copy_all_paths = copy.deepcopy(all_paths)

                Ares_pos = (start_i, start_j)
                # Tìm list of list các cặp start và goal
                result = find_postion_for_Arex_to_push(all_paths, Ares_pos)
                found = False
                for start_goal in result:
                    # Tìm đường đi từ các cặp start và goal
                    found, num3, sub_parent = bfs_from_Arex_to_switches(
                        map_data, start_goal[0], start_goal[1], copy_all_paths
                    )
                    total_nodes += num3
                    # Nếu không tìm được được đi của một trong số các cặp start và goal, nghĩa là không có đáp án
                    if not found:
                        break
                    path = []
                    current_pos = start_goal[1]
                    while current_pos is not None:
                        path.append(current_pos)
                        current_pos = sub_parent[current_pos]
                    path.reverse()  # Đảo ngược đường đi để từ start đến goal
                    # nối các đường đi thành đường đi hoàn chỉnh
                    path.pop(0)
                    answer.extend(path)
                    # answer.append(path)
                if not found:
                    continue
                answer.insert(0, Ares_pos)
                return answer, all_paths, total_nodes, result

    return [], [], total_nodes, result


# Dựa vào đường đi của hòn đá, tìm vị trí để Arex đẩy được hòn đá theo đường đi đã tìm được
# input: đường đi của hòn đá, tọa độ của Arex
# output: list of list vỡi một phần tử là một list chứa điểm bắt đầu và kết thúc
def find_postion_for_Arex_to_push(all_paths, Arex_pos):
    result = []
    start = Arex_pos
    for path in all_paths:
        for i in range(len(path) - 1):
            if (
                path[i][0] == path[i + 1][0] and path[i][1] < path[i + 1][1]
            ):  # Đi sang phải
                goal = (path[i][0], path[i][1] - 1)
                if goal != start:
                    result.append([start, goal])
                result.append([goal, path[i]])
                start = path[i]
            elif (
                path[i][0] == path[i + 1][0] and path[i][1] > path[i + 1][1]
            ):  # Đi sang trái
                goal = (path[i][0], path[i][1] + 1)
                if goal != start:
                    result.append([start, goal])
                result.append([goal, path[i]])
                start = path[i]
            elif (
                path[i][0] < path[i + 1][0] and path[i][1] == path[i + 1][1]
            ):  # Đi xuống dưới
                goal = (path[i][0] - 1, path[i][1])
                if goal != start:
                    result.append([start, goal])
                result.append([goal, path[i]])
                start = path[i]
            elif (
                path[i][0] > path[i + 1][0] and path[i][1] == path[i + 1][1]
            ):  # Đi lên trên
                goal = (path[i][0] + 1, path[i][1])
                if goal != start:
                    result.append([start, goal])
                result.append([goal, path[i]])
                start = path[i]

    return result


# Tìm đường đi cho arex tới vị trí cần thiết
# input: bản đồ, tọa độ bắt đầu , tọa độ xuất phát, đường đi của hòn đá
# output: Arex có tới vị trí đó được không, số node, đường đi trả về
def bfs_from_Arex_to_switches(map_2d, start, goal: tuple, all_paths):
    if start == goal:
        return True, 0, {start: None}
    # Trường hợp đích đến là tọa độ của hòn đá, đẩy hòn đá tới vị trí tiếp theo trong đường đi của hòn đá tìm được
    for i in range(len(all_paths)):
        if goal == all_paths[i][0]:
            map_2d[goal[0]][goal[1]] = " "
            map_2d[all_paths[i][1][0]][all_paths[i][1][1]] = "$"
            del all_paths[i][0]
    # Kích thước của bản đồ
    m = len(map_2d)
    n = 0
    for r in map_2d:
        if n < len(r):
            n = len(r)

    # 4 hướng di chuyển: lên, xuống, trái, phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Hàng đợi BFS
    queue = deque([start])
    explored = []
    # Đánh dấu các ô đã thăm
    visited = [[False for _ in range(n)] for _ in range(m)]
    visited[start[0]][start[1]] = True

    parent = {start: None}  # Để truy vết

    # BFS
    while queue:
        x, y = queue.popleft()
        explored.append((x, y))

        # Duyệt qua 4 hướng
        for i in range(len(directions)):
            dx, dy = directions[i]
            nx, ny = x + dx, y + dy
            # Kiểm tra nếu ô mới nằm trong bản đồ và chưa được thăm
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                # Kiểm tra nếu có thể đi qua ô đó (ví dụ, ô không phải là tường '#' hoặc đá '$')
                if map_2d[nx][ny] != "#" and (
                    map_2d[nx][ny] != "$" and map_2d[nx][ny] != "*"
                ):
                    visited[nx][ny] = True
                    parent[(nx, ny)] = (x, y)
                    if (nx, ny) == goal:
                        return True, len(explored), parent
                    queue.append((nx, ny))

    return False, len(explored), parent


# Tìm đường đi kết quả cuối cùng
# input: bản đồ, list chứa trọng lượng của hòn đá
def BFS_find_path(map_data, rocks_data):
    # Tìm tọa độ của Arex trong bản đồ
    start_i, start_j = find_arex(map_data)
    total = 0
    weight_of_rocks = {}
    # Tìm tọa độ hòn đá và cần gạt
    num1, stones, switches = bfs_find_origin(
        map_data, start_i, start_j, len(rocks_data)
    )
    copy_stones = copy.deepcopy(stones)
    # Sắp xếp danh sách các hòn đá theo quy tắc từ trái sang phải, từ trên xuống dưới, mục đích tạo từ điển
    # với key là tọa độ hòn đá, value là trọng số của hòn đá ấy
    sorted_points = sorted(copy_stones, key=sort_points)
    for i in range(len(sorted_points)):
        weight_of_rocks[sorted_points[i]] = int(rocks_data[i])

    total += num1
    answer, all_paths, num2, result = swap_the_rock(
        map_data, stones, switches, start_i, start_j
    )
    total += num2
    return answer, all_paths, total, result, weight_of_rocks
    # for i in all_paths:
    #     if len(i) == 1:
    #         all_paths.remove(i)

    # copy_all_paths = copy.deepcopy(all_paths)

    # total += num2
    # Ares_pos = (start_i, start_j)
    # # có số đường đi của hòn đá ứng với số hòn đá không
    # if is_answer:
    #     # Tìm list of list các cặp start và goal
    #     result = find_postion_for_Arex_to_push(all_paths, Ares_pos)
    #     for start_goal in result:
    #         # Tìm đường đi từ các cặp start và goal
    #         found, num3, sub_parent = bfs_from_Arex_to_switches(
    #             map_data, start_goal[0], start_goal[1], copy_all_paths
    #         )
    #         total += num3
    #         # Nếu không tìm được được đi của một trong số các cặp start và goal, nghĩa là không có đáp án
    #         if not found:
    #             return [], [], total, result, weight_of_rocks
    #         path = []
    #         current_pos = start_goal[1]
    #         while current_pos is not None:
    #             path.append(current_pos)
    #             current_pos = sub_parent[current_pos]
    #         path.reverse()  # Đảo ngược đường đi để từ start đến goal
    #         # nối các đường đi thành đường đi hoàn chỉnh
    #         path.pop(0)
    #         answer.extend(path)
    #         # answer.append(path)

    #     answer.insert(0, Ares_pos)
    #     return answer, all_paths, total, result, weight_of_rocks
    # else:
    #     return answer, all_paths, total, result, weight_of_rocks


# Dùng để in đáp án cần tìm
# input: bản đồ, list chứa trọng lượng của hòn đá
# ouput: Kết quả các chỉ số mong muốn
def printAnswer(map_data, rocks_data):
    answer_path = ""
    # Đo thời gian bắt đầu
    start_time = time.time()
    # Bắt đầu theo dõi bộ nhớ
    tracemalloc.start()
    path, all_paths, total, result, weight_of_rocks = BFS_find_path(
        map_data, rocks_data
    )
    # Lấy thông tin về bộ nhớ hiện tại và mức tiêu thụ cao nhất
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    # Đo thời gian kết thúc
    end_time = time.time()
    # Tính thời gian thực thi
    execution_time = (end_time - start_time) * 1000
    current_memory = current_memory / (1024 * 1024)
    # Kết thúc theo dõi bộ nhớ
    tracemalloc.stop()
    total_weight = 0
    # Tính tổng số cân nặng mà ta đẩy hòn đá dựa vào đường đi của từng hòn đá
    for rock_path in all_paths:
        total_weight += (len(rock_path) - 1) * weight_of_rocks[rock_path[0]]

    copy_all_paths = copy.deepcopy(all_paths)
    # Tính đường đi cho hòn đá từ list các tọa độ
    for i in range(len(path) - 1):
        if path[i][0] == path[i + 1][0] and path[i][1] < path[i + 1][1]:  # Đi sang phải
            # Dùng để xác định tọa độ có phải là di chuyển hòn đá không
            element = (path[i + 1][0], path[i + 1][1])
            found = False
            for i in range(len(all_paths)):
                if element == all_paths[i][0]:
                    found = True
                    del all_paths[i][0]
                    break
            if found:
                answer_path += "R"
            else:
                answer_path += "r"
        elif (
            path[i][0] == path[i + 1][0] and path[i][1] > path[i + 1][1]
        ):  # Đi sang trái
            element = (path[i + 1][0], path[i + 1][1])
            found = False
            for i in range(len(all_paths)):
                if element == all_paths[i][0]:
                    found = True
                    del all_paths[i][0]
                    break
            if found:
                answer_path += "L"
            else:
                answer_path += "l"
        elif (
            path[i][0] < path[i + 1][0] and path[i][1] == path[i + 1][1]
        ):  # Đi xuống dưới
            element = (path[i + 1][0], path[i + 1][1])
            found = False
            for i in range(len(all_paths)):
                if element == all_paths[i][0]:
                    found = True
                    del all_paths[i][0]
                    break
            if found:
                answer_path += "D"
            else:
                answer_path += "d"
        elif (
            path[i][0] > path[i + 1][0] and path[i][1] == path[i + 1][1]
        ):  # Đi lên trên
            element = (path[i + 1][0], path[i + 1][1])
            found = False
            for i in range(len(all_paths)):
                if element == all_paths[i][0]:
                    found = True
                    del all_paths[i][0]
                    break
            if found:
                answer_path += "U"
            else:
                answer_path += "u"
    # return answer_path, copy_all_paths, path, result, total, total_weight
    return answer_path, total_weight, total, execution_time, current_memory


# Tính chi phí
# Hàm sắp xếp sẽ dựa vào hoành độ trước, nếu hoành độ bằng nhau thì so sánh theo tung độ giảm dần
def sort_points(point):
    x, y = point
    return (x, y)


def main(in_filename, out_filename):
    rocks_data, map_data = read_map_file(in_filename)
    # Trả về kết quả
    answer_path, total_weight, total, execution_time, current_memory = printAnswer(
        map_data, rocks_data
    )
    # Ghi kết quả vào file output
    if answer_path == "":
        solution = "No solution"
    else:
        solution = answer_path
    data = (
        f"BFS\n"
        f"Steps: {len(answer_path)}, Weight: {total_weight}, Node: {total}, "
        f"Time (ms): {execution_time:.4f}, Memory (MB): {current_memory:.4f}\n"
        f"{solution}\n"
    )
    write_data(out_filename, data)


# Main


