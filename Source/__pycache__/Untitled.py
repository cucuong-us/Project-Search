data = list(map(int, input().split()))

n = data[0]  # Количество шариков
balls = data[1:]  # Цвета шариков

# Инициализация переменной для подсчета уничтоженных шариков
destroyed = 0

# Проверяем непрерывные цепочки
i = 0
while True:
        n = len(data)
        i = 0
        found = False  # Kiểm tra xem có chuỗi nào bị phá hủy không

        # Duyệt qua chuỗi để tìm các nhóm liên tiếp cùng màu
        while i < n:
            j = i
            # Xác định độ dài của chuỗi bóng cùng màu
            while j < n and data[j] == data[i]:
                j += 1
        
            # Nếu có ít nhất 3 quả bóng cùng màu liên tiếp, loại bỏ chúng
            if j - i >= 3:
                destroyed += (j - i)  # Cộng số bóng bị phá hủy
                data = data[:i] + data[j:]  # Cập nhật chuỗi sau khi phá hủy
                found = True  # Đánh dấu tìm thấy chuỗi cần phá hủy
                break  # Thoát ra để bắt đầu duyệt lại từ đầu
            
            i = j  # Tiếp tục duyệt từ vị trí mới

        # Nếu không tìm thấy chuỗi nào cần phá hủy, dừng vòng lặp
        if not found:
            break

# Выводим результат
print(destroyed)