import pygame
import sys
import subprocess
import queue
import time
window_width = 800
window_height = 600


window = pygame.display.set_mode((window_width + 200, window_height))


LIGHT_BLACK = (50, 50, 50)
LIGHT_BLUE = (48, 227, 202)
LIGHT_GRAY = (64, 81, 78)
LIGHT_WHITE = (228, 249, 245)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (78, 27, 202)


# Thêm trước khi sử dụng font
pygame.font.init()

# read from txt input.txt
def read_input():
    
    with open('input.txt', 'r') as f:
        # read the size of the board
        lines = f.readlines()
        
        size = {"x": int(lines[0].split(',')[0]), "y": int(lines[0].split(',')[1])}
        start = {"x": int(lines[1].split(',')[0]), "y": int(lines[1].split(',')[1])}
        goal = {"x": int(lines[1].split(',')[2]), "y": int(lines[1].split(',')[3])} 
        num_obstacles = int(lines[2])
        obstacles = []
    
        #Reading obstacle coordinates
        for i in range(3, 3 + num_obstacles):
            obstacle_line = lines[i].strip().split(',')
            obstacle_coords = [{"x": int(obstacle_line[j]), "y": int(obstacle_line[j+1])} for j in range(0, len(obstacle_line), 2)]
            obstacles.append(obstacle_coords)
    
    return size, start, goal, num_obstacles, obstacles


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

def points_on_polygon(polygons):
    points_list = []
    for polygon in polygons:
        points = []
        num_points = len(polygon)
        for i in range(num_points):
            x0, y0 = polygon[i].values()
            x1, y1 = polygon[(i + 1) % num_points].values()
            points.extend(draw_line(x0, y0, x1, y1))
        points = list(set(points))  # Remove duplicate points
        points_list.append(points)
    return points_list

size, start, goal, num_obstacles, obstacles = read_input()

cols = size["x"] + 1
rows = size["y"] + 1

box_width = window_width / cols
box_height = window_height / rows

grid = []
path = []

# Tìm các điểm nằm trên đa giác
points_on_obstacles = points_on_polygon(obstacles)


# Shortest Path using BFS algorithm
class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start = 0
        self.end = 0
        self.obstacle = 0
        self.color = LIGHT_BLACK
        self.visited = False
        self.queued = False
        self.neighbors = []
        self.previous = None
        self.goal = float('inf')  

         # Đánh số cho ô theo trục x và y mà không trùng lặp
        self.number = None
        
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
        if self.start == 1:  # Nếu ô là ô bắt đầu, vẽ ký tự 'S' lên ô
            font = pygame.font.Font(None, 36)  # Chọn font và kích thước
            text = font.render('S', True, LIGHT_BLACK)  # Tạo đối tượng văn bản
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  # Đặt vị trí văn bản ở giữa của ô
            window.blit(text, text_rect)

        if self.end == 1:  # Nếu ô là ô kết thúc, vẽ ký tự 'E' lên ô
            font = pygame.font.Font(None, 36)  # Chọn font và kích thước
            text = font.render('G', True, LIGHT_BLACK)  # Tạo đối tượng văn bản
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  # Đặt vị trí văn bản ở giữa của ô
            window.blit(text, text_rect)

        if self.number is not None:  # Nếu ô có số thứ tự
            font = pygame.font.Font(None, 24)  # Chọn font và kích thước
            text = font.render(str(self.number), True, (255, 255, 255))  # Tạo đối tượng văn bản
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  # Đặt vị trí văn bản ở giữa của ô
            window.blit(text, text_rect)

    
    def setStart(self):
        self.start = 1


    def setEnd(self):
        self.end = 1

    def setObstacle(self):
        self.obstacle = 1

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
        return self.goal < other.goal  # Compare boxes based on their accumulated cost

# Create Grid with 2D Array
for i in range(cols):
    arr = []  # Create empty array for each row in the grid
    for j in range(rows):
        # Append each box to the array for each row in the grid. This creates a 2D array of boxes that can be accessed by grid[i][j]
        arr.append(Box(i, j))
    grid.append(arr)  # Append the array to the grid


# set neighbours
for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbors()



def main():
    font = pygame.font.SysFont('Courier New', 20)
    
   
    ##################
    node_count  =0
    begin_search = False
    target_box = None
    searching = True
    start_box = None
    target_box = grid[goal["x"]][rows - 1 - goal["y"]]
    target_box.setEnd()
  
         
    start_box = grid[start["x"]][rows - 1 -start["y"]]
 

    start_box = grid[start["x"]][rows - 1 -start["y"]]
    start_box.setStart()
    start_box.visited = True
    start_box.queued = True
    start_box.goal = 0
    priority_queue = queue.PriorityQueue()
    priority_queue.put(start_box)

    # set obstacles
    for i, points in enumerate(points_on_obstacles):
        for point in points:
            x, y = point
            grid[x][rows - 1- y].setObstacle()
          

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

        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE] :
            begin_search = True
            start_time = time.time()

        if begin_search:
            if not priority_queue.empty():
                current_box = priority_queue.get()  
                current_box.visited = True
                    # if current_box.x == target_box.x and  current_box.y==target_box.y:
                if current_box==target_box:
                    while current_box != start_box:
                        path.append(current_box)
                        current_box = current_box.previous
                        node_count = node_count+1
                    searching = False
                    start_box.show(window, GREEN)
                    end_time = time.time()

                for neighbor in current_box.neighbors:
                        # time.sleep(0.1)

                            
                    if not neighbor.obstacle and not neighbor.visited:
                        neighbor.queued = True
                        new_cost = current_box.goal + 1  # Assuming uniform cost for all moves
                        if new_cost < neighbor.goal:  # If new path to neighbor is cheaper
                            check = False
                            for item in priority_queue.queue:
                                if item==neighbor:
                                    neighbor.goal = new_cost
                                    neighbor.previous = current_box
                                    priority_queue.queue.remove(item)
                                    priority_queue.put(neighbor)
                                    check = True
                            if check ==False:
                                neighbor.goal = new_cost
                                neighbor.previous = current_box
                                priority_queue.put(neighbor)

        for i in range(cols):
            for j in range(rows):
                # Get the box at the current position in the grid array and store it in the box variable
                box = grid[i][j]
                box.show(window, LIGHT_BLACK)
                if box.start == 1:
                    box.show(window, LIGHT_BLUE)  
                if box.obstacle == 1:
                    box.show(window, LIGHT_GRAY)  
                if box.end == 1:
                    box.show(window, LIGHT_WHITE) 
                if box.queued:
                    if box == start_box:
                        box.show(window, YELLOW) 
                    else:
                        box.show(window, RED) 
                if box.visited:
                    if box == start_box:
                        box.show(window, YELLOW) 
                    else:
                        box.show(window, GREEN)                 
                if box in path:
                    box.show(window, BLUE)  
                    
                    
                if not searching:
                    text_surface1 = font.render("Node count: "+ str(node_count-1), True, YELLOW)
                    text_surface2 = font.render("Time: "+ "{:.2f}".format(end_time - start_time) + "s", True, YELLOW)
                    text_rect1 = text_surface1.get_rect()
                    text_rect2 = text_surface2.get_rect()
                    # Đặt văn bản bên phải của cửa sổ
                    text_rect1.left = window_width 
                    text_rect2.left = window_width 
                    text_rect1.top = 50
                    text_rect2.top = 100
                    window.blit(text_surface1,text_rect1)
                    window.blit(text_surface2,text_rect2)
    
                    box.show(window, LIGHT_BLACK) 
                    if box in path:
                        box.show(window, BLUE) 
                    if box.queued:
                        if box == start_box:
                            box.show(window, GREEN) 
                    if box.obstacle == 1:
                        box.show(window, LIGHT_GRAY)  
                    if box.end == 1:
                        box.show(window, LIGHT_WHITE)  
                    

        pygame.display.flip()


main()