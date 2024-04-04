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
    font_title_large = pygame.font.SysFont('Franklin Gothic Medium', 70)
    font_title_small = pygame.font.SysFont('Courier New', 30)

    title_text_large = font_title_large.render("AI_SEARCH", True, BLACK)
    title_rect_large = title_text_large.get_rect(center=(WINDOW_WIDTH // 2, 100))
    window.blit(title_text_large, title_rect_large)

    title_text_small = font_title_small.render("Nhóm 12_MainMenu", True, BLUE)
    title_rect_small = title_text_small.get_rect(center=(WINDOW_WIDTH // 2, 200))
    window.blit(title_text_small, title_rect_small)
    
    font_option = pygame.font.SysFont('Courier New', 40)
    # Vẽ các lựa chọn
    options = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Quit"]
    row1 = options[:len(options) // 2]  # Split options into two rows
    row2 = options[len(options) // 2:]
    for i, option in enumerate(row1):
        text = font_option.render(option, True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 4, 250 + i * 80))
        window.blit(text, text_rect)
    
    for i, option in enumerate(row2):
        text_color = BLACK
        if option == "Quit":
            text_color = RED
        text = font_option.render(option, True, text_color)
        text_rect = text.get_rect(center=(3 * WINDOW_WIDTH // 4, 250 + i * 80))
        window.blit(text, text_rect)
    
    pygame.display.flip()

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Nhóm 12")
    
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
                    if 150 <= mouse_pos[0] <= 350:
                        if 210 <= mouse_pos[1] <= 290:
                            # Nút "Level 1" được nhấp
                            print("Level 1!")
                            subprocess.Popen(["python", "L1_BFS.py"])  # Chạy L1.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 310 <= mouse_pos[1] <= 390:
                            # Nút "Level 2" được nhấp
                            print("Level 2!")
                            subprocess.Popen(["python", "L2.py"])  # Chạy L2.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 410 <= mouse_pos[1] <= 490:
                            # Nút "Level 3" được nhấp
                            print("Level 3!")
                            subprocess.Popen(["python", "L3.py"])  # Chạy L3.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                    elif 450 <= mouse_pos[0] <= 650:
                        if 210 <= mouse_pos[1] <= 290:
                            # Nút "Level 4" được nhấp
                            print("Level 4!")
                            subprocess.Popen(["python", "L4.py"])  # Chạy L4.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 310 <= mouse_pos[1] <= 390:
                            # Nút "Level 5" được nhấp
                            print("Level 5!")
                            subprocess.Popen(["python", "L5.py"])  # Chạy L5.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 410 <= mouse_pos[1] <= 490:
                            # Nút "Quit" được nhấp
                            print("Quit game!")
                            pygame.quit()
                            sys.exit()
        
        draw_menu(window)
        clock.tick(60)

if __name__ == "__main__":
    main()
