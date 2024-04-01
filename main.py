import matplotlib.pyplot as plt

def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Đọc kích thước không gian
        space_limit = list(map(int, lines[0].strip().split(',')))
        
        # Đọc tọa độ điểm bắt đầu
        start_point = list(map(int, lines[1].strip().split(',')))
        
        # Đọc tọa độ điểm kết thúc (nếu có)
        end_point = []
        if len(lines) > 2:
            end_point = list(map(int, lines[2].strip().split(',')))
        
        return space_limit, start_point, end_point

# Sử dụng hàm read_input để đọc dữ liệu từ tệp input.txt
input_filename = 'input.txt'
space_limit, start_point, end_point = read_input(input_filename)

# Tạo đồ thị
# Tạo đồ thị và đặt tên cho figure
plt.figure(num='Do an Search_N12', figsize=(8, 8))
plt.xlim(0, space_limit[0])
plt.ylim(0, space_limit[1])

# Vẽ điểm bắt đầu và kết thúc
plt.scatter(start_point[0], start_point[1], color='blue', label='Start Point')
plt.scatter(end_point[0], end_point[1], color='red', label='End Point')

# Đặt tên cho các trục và tiêu đề của đồ thị
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Representation of Start and End Points') #Để tên thuật toán ở đây

# Hiển thị chú thích
plt.legend()

# Hiển thị đồ thị
plt.grid(True)
plt.show()
