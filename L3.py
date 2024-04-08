import pygame
import sys
import subprocess
import queue
import math

window_width = 1024 - 200
window_height = 768

window = pygame.display.set_mode((window_width + 200, window_height))

# Màu sắc
LIGHT_BLACK = (50, 50, 50)
LIGHT_BLUE = (48, 227, 202)
LIGHT_GRAY = (64, 81, 78)
LIGHT_WHITE = (228, 249, 245)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (78, 27, 202)

# Font
pygame.font.init()
font = pygame.font.SysFont('Inter', 24)

# Đọc dữ liệu từ tệp tin input.txt
def read_input():
    with open('input_lv3.txt', 'r') as f:
        lines = f.readlines()
        
        size = {"x": int(lines[0].split(',')[0]), "y": int(lines[0].split(',')[1])}
        start = {"x": int(lines[1].split(',')[0]), "y": int(lines[1].split(',')[1])}
        goal = {"x": int(lines[1].split(',')[2]), "y": int(lines[1].split(',')[3])} 
        num_obstacles = int(lines[2])
        obstacles = []
    
        for i in range(3, 3 + num_obstacles):
            obstacle_line = lines[i].strip().split(',')
            obstacle_coords = [{"x": int(obstacle_line[j]), "y": int(obstacle_line[j+1])} for j in range(0, len(obstacle_line), 2)]
            obstacles.append(obstacle_coords)
        pick_up_points = []
        pick_up_line = lines[3 + num_obstacles].strip().split(',')
        for j in range(0, len(pick_up_line), 2):
            pick_up_points.append({"x": int(pick_up_line[j]), "y": int(pick_up_line[j+1])})
    return size, start, goal, num_obstacles, obstacles, pick_up_points

# Tính khoảng cách Euclid giữa hai ô
def euclidean_distance(box1, box2):
    return math.sqrt((box1.x - box2.x) ** 2 + (box1.y - box2.y) ** 2)

# Vẽ đường thẳng giữa hai điểm
def draw_line(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    points = []

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return points

# Tìm các điểm nằm trên đa giác
def points_on_polygon(polygons):
    points_list = []
    for polygon in polygons:
        points = []
        num_points = len(polygon)
        for i in range(num_points):
            x0, y0 = polygon[i].values()
            x1, y1 = polygon[(i + 1) % num_points].values()
            points.extend(draw_line(x0, y0, x1, y1))
        points = list(set(points))  # Loại bỏ các điểm trùng lặp
        points_list.append(points)
    return points_list

# Đọc dữ liệu và khởi tạo grid
size, start, goal, num_obstacles, obstacles, pick_up_points = read_input()

cols = size["x"] + 1
rows = size["y"] + 1

box_width = window_width / cols
box_height = window_height / rows

grid = []

# Tìm các điểm nằm trên các đa giác
points_on_obstacles = points_on_polygon(obstacles)

# Class Box đại diện cho mỗi ô trên lưới
class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start = 0
        self.end = 0
        self.baseStart = 0
        self.baseEnd= 0
        self.pick_up_point = 0
        self.obstacle = 0
        self.color = LIGHT_BLACK
        self.visited = False
        self.queued = False
        self.neighbors = []
        self.previous = None
        self.goal = float('inf')  

         # Đánh số cho ô theo trục x và y mà không trùng lặp
        self.number = None
        
        if self.x == 0 and self.y != 0:  # Các ô ở vị trí x = 0, ngoại trừ ô gốc (0, 0)
            self.number = size['y'] - self.y 
        elif self.y == size["y"] and self.x != 0:  # Các ô ở vị trí y = 0, ngoại trừ ô gốc (0, 0)
            self.number = self.x 
        if self.x == 0 and self.y == 0:
            self.number = size['y']

        # Kiểm tra nếu ô có số thứ tự, thì đánh dấu là rào cản
        if self.number is not None:
            self.obstacle = 1
          

    def show(self, window, color):
        pygame.draw.rect(window, color, (self.x * box_width,
                         self.y * box_height, box_width - 2, box_height - 2))
        
        if self.baseStart == 1 :  # Nếu ô là ô bắt đầu, vẽ ký tự 'S' lên ô
            text = font.render('S', True, LIGHT_BLACK)  
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  
            window.blit(text, text_rect)

        if self.baseEnd == 1:  
            text = font.render('G', True, LIGHT_BLACK)  
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  
            window.blit(text, text_rect)

        if self.pick_up_point == 1:
            text = font.render('P', True, LIGHT_BLACK)  
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  
            window.blit(text, text_rect)

        if self.number is not None:  
            text = font.render(str(self.number), True, (255, 255, 255))  
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  
            window.blit(text, text_rect)


    def setStart(self):
        self.start = 1

    def setEnd(self):
        self.end = 1
    def setBaseStart(self):
        self.baseStart = 1

    def setBaseEnd(self):
        self.baseEnd = 1

    def setObstacle(self):
        self.obstacle = 1

    def setPickUpPoint(self):
        self.pick_up_point = 1

    def addNeighbors(self):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
    def __lt__(self, other):
        if self.goal==other.goal:
            return False
        return self.goal < other.goal  

# Create Grid with 2D Array
for i in range(cols):
    arr = []  
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)  

# Set neighbors
for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbors()

# Hàm tìm đường đi ngắn nhất từ một điểm đến một điểm khác
def find_shortest_path(start_point, end_point):
    path = []
    start_box = grid[start_point["x"]][rows - 1 - start_point["y"]]
    end_box = grid[end_point["x"]][rows - 1 - end_point["y"]]

    start_box.setStart()
    end_box.setEnd()

    open_set = queue.PriorityQueue()
    open_set.put((0, start_box))  # Thêm điểm bắt đầu vào open set với ưu tiên là 0

    came_from = {}
    g_score = {box: float('inf') for row in grid for box in row}
    g_score[start_box] = 0

    while not open_set.empty():
        current_box = open_set.get()[1]

        if current_box == end_box:  # Nếu đã đến được điểm cuối, thoát vòng lặp
            break

        for neighbor in current_box.neighbors:
            if neighbor.obstacle == 1:  # Nếu ô láng giềng là vật cản, bỏ qua
                continue

            temp_g_score = g_score[current_box] + 1  # Ước lượng chi phí từ điểm bắt đầu đến ô láng giềng là 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_box
                g_score[neighbor] = temp_g_score
                priority = temp_g_score + euclidean_distance(neighbor, end_box)  # Ưu tiên = chi phí thực tế + ước lượng chi phí từ điểm hiện tại đến điểm cuối
                open_set.put((priority, neighbor))

    # Xác định đường đi bằng cách lùi lại từ điểm cuối
    current_box = end_box
    while current_box in came_from:
        path.insert(0, current_box)
        current_box = came_from[current_box]
    path.insert(0, start_box)
    return path



def main():
    # Load background image
    background_image = pygame.image.load("frameGame.png")
    window.blit(background_image, (0, 0))
    
    path = []
    target_box = grid[goal["x"]][rows - 1 - goal["y"]]
    target_box.setBaseEnd()

    start_box = grid[start["x"]][rows - 1 -start["y"]]
    start_box.setBaseStart()

    # set obstacles
    for i, points in enumerate(points_on_obstacles):
        for point in points:
            x, y = point
            grid[x][rows - 1- y].setObstacle()
    # set pick up points
    for pick_up_point in pick_up_points:
        grid[pick_up_point["x"]][rows - 1 - pick_up_point["y"]].setPickUpPoint()
    
    pick_up_points.append(goal)
    pick_up_points.insert(0, start)
    # Chạy thuật toán tìm đường đi ngắn nhất cho mỗi cặp điểm đón và điểm cuối
    for i in range(len(pick_up_points) - 1):
        start_point = pick_up_points[i]
        end_point = pick_up_points[i + 1]
        path += find_shortest_path(start_point, end_point)

    # Vẽ lưới và đường đi
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Kiểm tra nếu phím "E" được nhấn
                    # Thực hiện hành động để quay lại menu ở đây
                    print("Exit!")
                    subprocess.Popen(["python", "menu.py"])  # Gọi hàm để quay lại menu
                    pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                    sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE]:
            break
        
        for i in range(cols):
            for j in range(rows):
                # Get the box at the current position in the grid array and store it in the box variable
                box = grid[i][j]
                box.show(window, LIGHT_BLACK)
                if box in path:
                    box.show(window, BLUE)

                if box.baseStart == 1:
                    box.show(window, GREEN)  
                if box.obstacle == 1:
                    box.show(window, LIGHT_GRAY)  

                if box.baseEnd == 1:
                    box.show(window, LIGHT_WHITE) 
                
                if box.pick_up_point == 1:
                    box.show(window, YELLOW)

               

        pygame.display.flip()  

main()
