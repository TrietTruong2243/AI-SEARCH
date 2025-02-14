import pygame
import sys
import subprocess
import queue
import time
from math import*
window_width = 1024 -200
window_height = 700
window = pygame.display.set_mode((window_width + 200, window_height))
window = pygame.display.set_mode((window_width + 200, window_height))


LIGHT_BLACK = (50, 50, 50)
LIGHT_BLUE = (48, 227, 202)
LIGHT_GRAY = (64, 81, 78)
LIGHT_WHITE = (228, 249, 245)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (78, 27, 202)
if len(sys.argv) <3:
    subprocess.Popen(["python", "./menu.py"])  # Quay về menu.py
    pygame.quit()  # Thoát khỏi cửa sổ hiện tại
    sys.exit()
filename = sys.argv[1]
h = int(sys.argv[2])
# filename = "input4.txt"
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # Đặt sự kiện Timer mỗi 1000ms (1 giây)

# Thêm trước khi sử dụng font
pygame.font.init()
font = pygame.font.SysFont('Inter', 24) # Chọn font và kích thước

# read from txt input.txt
def read_input():
    
    with open(filename, 'r') as f:
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
path1 = []
path2 = []

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
        self.isObstacle1 = 0
        self.isObstacle2 =0
        # self.isObstacle = 0
        self.color = LIGHT_BLACK
        self.visited = False
        self.queued1 = False        
        self.queued2 = False

        self.neighbors = []
        self.previous1 = None
        self.previous2 = None
        self.goal = float('inf')  

        # self.goal1 = float('inf')  
        # self.goal2 = float('inf')  

        self.heuristic = 0
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
            self.isObstacle1 = 1
            self.isObstacle2 = 1

          

    def show(self, window, color):
        pygame.draw.rect(window, color, (self.x * box_width,
                         self.y * box_height, box_width - 2, box_height - 2))
        if self.start == 1:  # Nếu ô là ô bắt đầu, vẽ ký tự 'S' lên ô
            text = font.render('S', True, LIGHT_BLACK)  # Tạo đối tượng văn bản
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  # Đặt vị trí văn bản ở giữa của ô
            window.blit(text, text_rect)

        if self.end == 1:  # Nếu ô là ô kết thúc, vẽ ký tự 'E' lên ô
            text = font.render('G', True, LIGHT_BLACK)  # Tạo đối tượng văn bản
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  # Đặt vị trí văn bản ở giữa của ô
            window.blit(text, text_rect)

        if self.number is not None:  # Nếu ô có số thứ tự
            text = font.render(str(self.number), True, (255, 255, 255))  # Tạo đối tượng văn bản
            text_rect = text.get_rect(center=(self.x * box_width + box_width // 2, self.y * box_height + box_height // 2))  # Đặt vị trí văn bản ở giữa của ô
            window.blit(text, text_rect)

    
    def setStart(self):
        self.start = 1


    def setEnd(self):
        self.end = 1

    def setObstacle(self):
        self.obstacle = 1
        # self.isObstacle = 1
    def setObstacle1(self):
        self.isObstacle1 = 1
    def setObstacle2(self):
        self.isObstacle2 = 1
    def removeObstacle(self):
        self.obstacle = 0
    def addNeighbors(self):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
    def setHeuristic(self, target_box):
        self.heuristic = abs(self.x - target_box.x) + abs(self.y-target_box.y) #eucildian
        # self.heuristic = sqrt((self.x - target_box.x)**2 + (self.y - target_box.y)**2) #mahhatan

    def __lt__(self, other):
        if (self.goal + self.heuristic) == (other.goal + other.heuristic):
            return False
        return (self.goal + self.heuristic) < (other.goal + other.heuristic)


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
    # Load background image
    temp = 0
    start_time =0 
    background_image = pygame.image.load("./images/frameGame.png")
    window.blit(background_image, (0, 0))
    time_counter =0 
    visited_count = 0  # Biến đếm số ô đã visited
    result = "Target Not Found!"

    node_count  =0
    begin_search = False
    target_box = None
    searching1 = True
    searching2 = True
    start_box = None
    target_box = grid[goal["x"]][rows - 1 - goal["y"]]
    target_box.setEnd()
  
         
    start_box = grid[start["x"]][rows - 1 -start["y"]]
 

    start_box = grid[start["x"]][rows - 1 -start["y"]]
    start_box.setStart()
    # start_box.visited = True
    start_box.queued1 = True
    start_box.queued2 = True
    start_box.goal = 0
    # start_box.goal1 = 0
    # start_box.goal2 = 0

    start_box.setHeuristic(target_box)
    open1 = []
    open2  = []
    open1.append(start_box)
    open2.append(start_box)
    # set obstacles
    for i, points in enumerate(points_on_obstacles):
        for point in points:
            x, y = point
            tempt = x+h
            grid[x][rows - 1- y].setObstacle()
            grid[x][rows - 1- y].setObstacle1()
            if (tempt < cols):
                grid[tempt][rows - 1- y].setObstacle2()

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
            if event.type == TIMER_EVENT:  # Xử lý sự kiện Timer
                for i, points in enumerate(points_on_obstacles):
                    for point in points:
                        x, y = point
                        if time_counter % 2 ==0:
                            grid[x][rows - 1- y].removeObstacle()
                        else:
                            tempt = x+h
                            if (tempt < cols):

                                grid[tempt][rows - 1- y].removeObstacle()

                for i, points in enumerate(points_on_obstacles):
                    for point in points:
                        x, y = point
                        if time_counter % 2 ==0:
                            tempt = x+h
                            if (tempt < cols):
                                grid[tempt][rows - 1- y].setObstacle()
                        else:
                            grid[x][rows - 1- y].setObstacle()

                time_counter +=1
                print("Thời gian đã trôi qua:", time_counter, "giây")
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if  start_time ==0: 
            if keys[pygame.K_SPACE ] and (temp < 1)  :
                begin_search = True
                start_time = time.time()

        if begin_search:
            if len(open1) > 0 and searching1:
                current_box = min(open1)  # Get the box with the minimum total cost
                if current_box == target_box:
                    result = "Target Found!"
                    searching1 = False
                    # temp = temp +1

                    end_time = time.time()
                    # Generate path back to start box
                    while current_box != start_box:
                        path1.append(current_box)
                        current_box = current_box.previous1
                else:
                    open1.remove(current_box)
                    # current_box.visited = True
                    visited_count += 1

                    for neighbor in current_box.neighbors:
                        if not neighbor.isObstacle1 and not neighbor.queued1:
                            neighbor.queued1 = True
                            neighbor.previous1 = current_box
                            neighbor.goal = current_box.goal + 1  # Assuming uniform cost for all moves
                            neighbor.setHeuristic(target_box)
                            open1.append(neighbor)
            if not searching1 or (len(open1)==0):
                if len(open2) > 0 and searching2:
                    current_box = min(open2)  # Get the box with the minimum total cost
                    print(current_box.goal + current_box.heuristic)

                    if current_box == target_box:
                        result = "Target Found!"
                        searching2 = False
                        # temp = temp +1

                        end_time = time.time()
                        # Generate path back to start box
                        while current_box != start_box:
                            path2.append(current_box)
                            current_box = current_box.previous2
                    else:
                        open2.remove(current_box)
                        # current_box.visited = True
                        visited_count += 1

                        for neighbor in current_box.neighbors:
                            if not neighbor.isObstacle2 and not neighbor.queued2:
                                neighbor.queued2 = True
                                neighbor.previous2 = current_box
                                neighbor.goal = current_box.goal + 1  # Assuming uniform cost for all moves
                                neighbor.setHeuristic(target_box)
                                open2.append(neighbor)    
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
                if box.queued1 or box.queued2:
                    if box == start_box:
                        box.show(window, YELLOW) 
                    else:
                        box.show(window, RED) 
                if box.visited:
                    if box == start_box:
                        box.show(window, YELLOW) 
                    else:
                        box.show(window, GREEN) 
                if box.obstacle == 1:
                    box.show(window, LIGHT_GRAY)                  
                # if box in path1:
                #     box.show(window, BLUE)  
                    
                # if (len(open1) == 0 and searching1 == True):
                #     text_surface = font.render("Result: ", False, RED)
                #     text_rect = text_surface.get_rect()
                #     # Đặt văn bản bên phải của cửa sổ
                #     text_rect.left = window_width  + 8
                #     text_rect.top = 200
                #     window.blit(text_surface,text_rect)
                #     text_surface1 = font.render(result, False, RED)
                #     text_rect1 = text_surface1.get_rect()
                #     # Đặt văn bản bên phải của cửa sổ
                #     text_rect1.left = window_width  + 8
                #     text_rect1.top = 250 
                #     window.blit(text_surface1,text_rect1)
                #     box.show(window, LIGHT_BLACK) 
                #     if time_counter % 2 ==0:
                #         if box in path1:
                #             box.show(window, BLUE) 
                #     else:
                #         if box in path2:
                #             box.show(window, BLUE) 
                #     if box.queued1 or box.queued2:
                #         if box == start_box:
                #             box.show(window, GREEN) 
                #     if box.obstacle == 1:
                #         box.show(window, LIGHT_GRAY)  
                #     if box.end == 1:
                #         box.show(window, LIGHT_WHITE)      
                if (not searching1 or len(open1)==0)and (len(open2)==0 or not searching2):
                    text_surface1 = font.render("Path length : " + str(len(path2)), False, LIGHT_BLACK)
                    text_surface2 = font.render("Visited box : " + str(visited_count), False, LIGHT_BLACK)
                    # text_surface3 = font.render("Time: " +"{:.2f}".format(end_time - start_time) + "s", False, LIGHT_BLACK)
                    text_surface4 = font.render("Result: " + result, False, RED)
                    text_surface5 = font.render("Note: When searching1, boxes highlighted in green are boxes that have been considered, boxes highlighted in red are boxes that have been added to the priority queue." , False, RED)

                    text_rect1 = text_surface1.get_rect()
                    text_rect2 = text_surface2.get_rect()
                    # text_rect3 = text_surface3.get_rect()
                    text_rect4 = text_surface4.get_rect()
                    text_rect5 = text_surface5.get_rect()

                    # Đặt văn bản bên phải của cửa sổ
                    text_rect1.left = window_width + 8
                    text_rect2.left = window_width + 8
                    # text_rect3.left = window_width + 8
                    text_rect4.left = window_width + 8
                    text_rect5.left = window_width + 8

                    text_rect1.top = 150 
                    text_rect2.top = 200 
                    # text_rect3.top = 250 
                    text_rect4.top = 300 
                    # text_rect5.top = 350
                    
                    # window.blit(text_surface1,text_rect1)
                    # window.blit(text_surface2,text_rect2)
                    # window.blit(text_surface3,text_rect3)
                    window.blit(text_surface4,text_rect4)
                    # window.blit(text_surface5,text_rect5)

    
                    box.show(window, LIGHT_BLACK) 
                    if time_counter % 2 ==0:
                        if box in path1:
                            box.show(window, BLUE) 
                    else:
                        if box in path2:
                            box.show(window, BLUE) 
                    
                    if box.queued1 or box.queued2:
                        if box == start_box:
                            box.show(window, GREEN) 
                    if box.end == 1:
                        box.show(window, LIGHT_WHITE)  
                    if box.obstacle == 1:
                        box.show(window, LIGHT_GRAY)  
                   
        pygame.display.flip()


main()
