import pygame
import sys
import subprocess
import queue
import math
import time
from itertools import permutations

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
filename = sys.argv[1]

# Font
pygame.font.init()
font = pygame.font.SysFont('Inter', 24)

# Đọc dữ liệu từ tệp tin input.txt
def read_input():
    with open(filename, 'r') as f:
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
        pick_up_line = lines[1].strip().split(',')
        for j in range(4, len(pick_up_line), 2):
            pick_up_points.append({"x": int(pick_up_line[j]), "y": int(pick_up_line[j+1]),"distance":0})
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
    check = False
    start_box.setStart()
    end_box.setEnd()

    open_set = queue.PriorityQueue()
    open_set.put((0, start_box))  # Thêm điểm bắt đầu vào open set với ưu tiên là 0

    came_from = {}
    g_score = {box: float('inf') for row in grid for box in row}
    g_score[start_box] = 0

    while not open_set.empty():
        current_box = open_set.get()[1]
        current_box.visited = True
        if current_box == end_box:  # Nếu đã đến được điểm cuối, thoát vòng lặp
            check = True
            break
        else:
            for neighbor in current_box.neighbors:
                neighbor.queued = True
                if neighbor.obstacle == 1:  # Nếu ô láng giềng là vật cản, bỏ qua
                    continue
                else:
                    temp_g_score = g_score[current_box] + 1  # Ước lượng chi phí từ điểm bắt đầu đến ô láng giềng là 1
                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current_box
                        g_score[neighbor] = temp_g_score
                        priority = temp_g_score + euclidean_distance(neighbor, end_box)  # Ưu tiên = chi phí thực tế + ước lượng chi phí từ điểm hiện tại đến điểm cuối
                        open_set.put((priority, neighbor))
        
    current_box = end_box

    if (check ==True):
        while current_box in came_from:
            path.insert(0, current_box)
            current_box = came_from[current_box]
        # path.insert(0, start_box)
    for i in range(cols-1):
            for j in range(rows-1):
                # Get the box at the current position in the grid array and store it in the box variable
                check1 = i+1
                box = grid[check1][j]
                box.queued = False
                box.visited = False
    pygame.display.flip()
    return path,check
def getAllPath( start, target, pickUpPoints):
    allPath = [['inf'] * len(pickUpPoints) for i in range(len(pickUpPoints))] 
    startPath = [['inf'] for i in range(len(pickUpPoints)) ]
    targetPath = [['inf']  for i in range(len(pickUpPoints))  ]
    
    for i in range(len(pickUpPoints)):
        startPath[i] = find_shortest_path(start, pickUpPoints[i])[0]
        targetPath[i] = find_shortest_path(pickUpPoints[i], target)[0]
        
    for m in range(len(pickUpPoints)):
        for n in range(len(pickUpPoints)):
            allPath[m][n] = find_shortest_path(pickUpPoints[m], pickUpPoints[n])[0]
    return (startPath,targetPath,allPath)
def findShortestPath( start, target, pickUpPoints):
    startPath, targetPath, allPath = getAllPath(start,target,pickUpPoints)
    shortest_length = float('inf')
    shortest_path = []
    for permutation in permutations(range(len(pickUpPoints))):
        path = []        
        path =path+ startPath[permutation[0]]
        for i in range(len(pickUpPoints) - 1):
            path = path + allPath[permutation[i]][permutation[i + 1]]
        path = path + targetPath[permutation[len(pickUpPoints) - 1]]
        length = len(path)
        if(length < shortest_length):
            shortest_length = length
            shortest_path = path
        for i in range(cols-1):
            for j in range(rows-1):
                # Get the box at the current position in the grid array and store it in the box variable
                check1 = i+1
                box = grid[check1][j]
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
                if box.obstacle == 1:
                    box.show(window, LIGHT_GRAY)
        pygame.display.flip()
        path = []
    return shortest_path

def updatePickUpPoints(pick_up_points1, start_box):
    updatePoints = []
    unvaiablePoint = 0
    temp = []
    for i in pick_up_points1:
        temp.append(i)
    first = start_box
    for i in temp:
        tempt = find_shortest_path(first,i)
        i["distance"] = tempt[1]
           
    for i in temp[:]:
        if (i["distance"]==False):
            unvaiablePoint = unvaiablePoint+1
        else:
            updatePoints.append(i)    
    return updatePoints,unvaiablePoint

def main():
    # Load background image
    checkDone = False
    background_image = pygame.image.load("frameGame.png")
    window.blit(background_image, (0, 0))
    checkRun = -1
    path = []
    updatePoints1 = pick_up_points
    target_box = grid[goal["x"]][rows - 1 - goal["y"]]
    target_box.setBaseEnd()
    
    start_box = grid[start["x"]][rows - 1 -start["y"]]
    start_box.setBaseStart()
    # updatePickUpPoints(pick_up_points,start)
  
    # set obstacles
    for i, points in enumerate(points_on_obstacles):
        for point in points:
            x, y = point
            grid[x][rows - 1- y].setObstacle()
    # set pick up points
    for pick_up_point in pick_up_points:
        grid[pick_up_point["x"]][rows - 1 - pick_up_point["y"]].setPickUpPoint()
    #test- get out
    
   
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
            if (checkRun==-1): 
                checkRun = checkRun+1
                text_surface4 = font.render("On search..." , False, RED)
                text_rect4 = text_surface4.get_rect()          
                text_rect4.left = window_width  + 8              
                text_rect4.top = 100 
                window.blit(text_surface4,text_rect4)
                pygame.display.flip()  

                start_time = time.time()
                updatePoints1, unavailblePoint = updatePickUpPoints(pick_up_points,start)
                checkRun = checkRun+1
                print("Start")
                if (find_shortest_path(start,goal)[1]==False):
                    result = "Target Not Found!"
                    checkDone = True

                elif len(updatePoints1)==0:
                    path = find_shortest_path(start,goal)[0]
                    result = "Target Found!"
                    checkDone = True


                else:
                    print("check")
                    path = findShortestPath(start,goal,updatePoints1)
                    result = "Target Found!"
                    checkDone = True

                end_time = time.time()
       
        for i in range(cols):
            for j in range(rows):
                # Get the box at the current position in the grid array and store it in the box variable
                box = grid[i][j]
                if (checkDone == True):
                    if (result =="Target Found!"):
                        if unavailblePoint ==0:
                            text_surface1 = font.render("Path length : " + str(len(path)), False, LIGHT_BLACK)
                            text_surface2 = font.render("Points not passed: " + str(unavailblePoint), False, LIGHT_BLACK)
                            text_surface3 = font.render("Time: " +"{:.2f}".format(end_time - start_time) + "s", False, LIGHT_BLACK)
                            text_surface4 = font.render("Result:" + result, False, RED)

                            text_rect1 = text_surface1.get_rect()
                            text_rect2 = text_surface2.get_rect()
                            text_rect3 = text_surface3.get_rect()
                            text_rect4 = text_surface4.get_rect()
                                # Đặt văn bản bên phải của cửa sổ
                            text_rect1.left = window_width + 8
                            text_rect2.left = window_width + 8
                            text_rect3.left = window_width  + 8
                            text_rect4.left = window_width  + 8

                            text_rect1.top = 150 
                            text_rect2.top = 200 
                            text_rect3.top = 250 
                            text_rect4.top = 300 

                            window.blit(text_surface1,text_rect1)
                            window.blit(text_surface2,text_rect2)
                            window.blit(text_surface3,text_rect3)
                            window.blit(text_surface4,text_rect4)
                            
                        else:
                            text_surface1 = font.render("Path length : " + str(len(path)), False, LIGHT_BLACK)
                            text_surface2 = font.render("Points not passed: " + str(unavailblePoint), False, LIGHT_BLACK)
                            text_surface3 = font.render("Time: " +"{:.2f}".format(end_time - start_time) + "s", False, LIGHT_BLACK)
                            text_surface4 = font.render("Result:", False, RED)
                            text_surface5 = font.render("Target found with some", False, RED)
                            text_surface6 = font.render("points not passed!", False, RED)

                            text_rect1 = text_surface1.get_rect()
                            text_rect2 = text_surface2.get_rect()
                            text_rect3 = text_surface3.get_rect()
                            text_rect4 = text_surface4.get_rect()
                            text_rect5 = text_surface5.get_rect()
                            text_rect6 = text_surface6.get_rect()

                                # Đặt văn bản bên phải của cửa sổ
                            text_rect1.left = window_width + 8
                            text_rect2.left = window_width + 8
                            text_rect3.left = window_width  + 8
                            text_rect4.left = window_width  + 8
                            text_rect5.left = window_width  + 8
                            text_rect6.left = window_width  + 8

                            text_rect1.top = 150 
                            text_rect2.top = 200 
                            text_rect3.top = 250 
                            text_rect4.top = 300 
                            text_rect5.top = 350 
                            text_rect6.top = 400 

                            window.blit(text_surface1,text_rect1)
                            window.blit(text_surface2,text_rect2)
                            window.blit(text_surface3,text_rect3)
                            window.blit(text_surface4,text_rect4)
                            window.blit(text_surface5,text_rect5)
                            window.blit(text_surface6,text_rect6)
                    else:
                            text_surface4 = font.render("Result:" , False, RED)
                            text_surface5 = font.render( result, False, RED)

                            
                            text_rect4 = text_surface4.get_rect()
                            text_rect5 = text_surface5.get_rect()
                           
                            text_rect4.left = window_width  + 8
                            text_rect5.left = window_width  + 8

                            
                            text_rect4.top = 250 
                            text_rect5.top = 300 

                            
                            window.blit(text_surface4,text_rect4)
                            window.blit(text_surface5,text_rect5)

                            path = []
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
