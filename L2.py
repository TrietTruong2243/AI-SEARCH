import pygame
import sys
import subprocess

# Các màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (64, 164, 223)
RED = (255, 0, 0)

# Kích thước cửa sổ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def draw_menu(window):
    window.fill(GRAY)
    font_title = pygame.font.SysFont('comicsansms', 70)
    font_option = pygame.font.SysFont('Courier New', 40)
    
    # Vẽ tiêu đề
    title_text = font_title.render("ALGORITHM", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    window.blit(title_text, title_rect)
    
    # Vẽ các lựa chọn
    options = ["DFS", "USC", "A*", "Exit"]
    row1 = options[:2]
    row2 = options[2:]
    
    for i, option in enumerate(row1):
        text_color = BLACK
        if option == "Exit":
            text_color = RED
        text = font_option.render(option, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2 - 100, 250 + i * 80))
        window.blit(text, text_rect)
    
    for i, option in enumerate(row2):
        text_color = BLACK
        if option == "Exit":
            text_color = RED
        text = font_option.render(option, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2 + 100, 250 + i * 80))
        window.blit(text, text_rect)
    
    pygame.display.flip()

def main_menu():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Main Menu")
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Kiểm tra nút được nhấp
                    mouse_pos = pygame.mouse.get_pos()
                    if 210 <= mouse_pos[1] <= 290:
                        if 150 <= mouse_pos[0] <= 350:
                            print("DFS!")
                            subprocess.Popen(["python", "DFS.py"]) 
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 450 <= mouse_pos[0] <= 650:
                            print("A*!")
                            subprocess.Popen(["python", "A.py"])
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                    elif 310 <= mouse_pos[1] <= 390:
                        if 150 <= mouse_pos[0] <= 350:
                            print("USC!")
                            subprocess.Popen(["python", "USC.py"])
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 450 <= mouse_pos[0] <= 650:
                            # Nút "Quay lại" được nhấp
                            print("Exit!")
                            subprocess.Popen(["python", "menu.py"])  # Chạy level1.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
        
        draw_menu(window)
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
