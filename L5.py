import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# read from txt input.txt
def read_input():
    with open('inputl5.txt', 'r') as f:
        # read the size of the board
        lines = f.readlines()
        
        size = {"x": int(lines[0].split(',')[0]), "y": int(lines[0].split(',')[1]), "z": int(lines[0].split(',')[2])}
        start = {"x": int(lines[1].split(',')[0]), "y": int(lines[1].split(',')[1]), "z": int(lines[1].split(',')[2])}
        goal = {"x": int(lines[1].split(',')[3]), "y": int(lines[1].split(',')[4]), "z": int(lines[1].split(',')[5])} 
        num_obstacles = int(lines[2])
        obstacles = []
    
        #Reading obstacle coordinates
        for i in range(3, 3 + num_obstacles):
            obstacle_line = lines[i].strip().split(',')
            obstacle_coords = [{"x": int(obstacle_line[j]), "y": int(obstacle_line[j+1]), "z": int(obstacle_line[j+2])} for j in range(0, len(obstacle_line), 3)]
            obstacles.append(obstacle_coords)
    
    return size, start, goal, num_obstacles, obstacles

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        # Vẽ các mặt của khối chướng ngại vật
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0) # Màu đỏ cho khối chướng ngại vật
        for i in range(len(obstacle)):
            glVertex3fv((obstacle[i]["x"], obstacle[i]["y"], obstacle[i]["z"]))
            glVertex3fv((obstacle[(i+1) % len(obstacle)]["x"], obstacle[(i+1) % len(obstacle)]["y"], obstacle[(i+1) % len(obstacle)]["z"]))
            glVertex3fv((obstacle[(i+1) % len(obstacle)]["x"], obstacle[(i+1) % len(obstacle)]["y"] + 1, obstacle[(i+1) % len(obstacle)]["z"]))
            glVertex3fv((obstacle[i]["x"], obstacle[i]["y"] + 1, obstacle[i]["z"]))
        glEnd()

def draw_axes():
    glBegin(GL_LINES)
    # X axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)

    # Y axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 10, 0)

    # Z axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 10)
    glEnd()

def main():
    size, start, goal, num_obstacles, obstacles = read_input()
    print("Size of the board:", size)
    print("Start point:", start)
    print("Goal point:", goal)
    print("Number of obstacles:", num_obstacles)
    print("Obstacle coordinates:")
    for i, obstacle in enumerate(obstacles):
        print("Obstacle", i+1, ":", obstacle)
    
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -30)

    rotation_speed = 22  # Tốc độ quay

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(rotation_speed, 0, 1, 0)
                elif event.key == pygame.K_RIGHT:
                    glRotatef(-rotation_speed, 0, 1, 0)
                elif event.key == pygame.K_UP:
                    glRotatef(rotation_speed, 1, 0, 0)
                elif event.key == pygame.K_DOWN:
                    glRotatef(-rotation_speed, 1, 0, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Vẽ các trục OXYZ
        draw_axes()
        
        # Vẽ các chướng ngại vật
        draw_obstacles(obstacles)

        pygame.display.flip()
        pygame.time.wait(10)
        clock.tick(30)

main()
