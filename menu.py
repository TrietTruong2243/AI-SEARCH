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
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

def draw_menu(window):
        # Load background image
    background_image = pygame.image.load("background.png")
    window.blit(background_image, (0, 0))



    font_option = pygame.font.SysFont('Courier New', 40)
    # Vẽ các lựa chọn
    options = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Quit"]
    row1 = options[:2]  # Split options into two rows
    row2 = options[2:4]
    row3 = options[4:]
    for i, option in enumerate(row1):
        text = font_option.render(option, True, BLACK)
        text_rect = text.get_rect(center=(330 - 150 ,375 + i * 120 + i*15))
        window.blit(text, text_rect)
    for i, option in enumerate(row2):
        text = font_option.render(option, True, BLACK)
        text_rect = text.get_rect(center=(485 , 375 + i * 120 + i*15))
        window.blit(text, text_rect)
    for i, option in enumerate(row3):
        text_color = BLACK
        if option == "Quit":
            text_color = WHITE
        text = font_option.render(option, True, text_color)
        text_rect = text.get_rect(center=(465 + 325, 375 + i * 120 + i*15))
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
                    print(mouse_pos)
                    if 335 <= mouse_pos[1] <= 410:
                        if 90 <= mouse_pos[0] <= 270:  # Check first row
                            print("Level 1!")
                            subprocess.Popen(["python", "L1_BFS.py"])  # Chạy L1.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 395 <= mouse_pos[0] <= 570:  # Second option
                            print("Level 3!")
                            subprocess.Popen(["python", "L3.py"])  # Chạy L3.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()

                        elif 700 <= mouse_pos[0] <= 880:  # Check second row
                            print("Level 5!")
                            subprocess.Popen(["python", "L5.py"])  # Chạy L5.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                    elif 470 <= mouse_pos[1] <= 545:
                        if 90 <= mouse_pos[0] <= 270:  # Check first row
                            print("Level 2!")
                            subprocess.Popen(["python", "L2.py"])  # Chạy L2.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 395 <= mouse_pos[0] <= 575:  # Second option
                            print("Level 4!")
                            subprocess.Popen(["python", "L4.py"])  # Chạy L4.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 700 <= mouse_pos[0] <= 800:  # Check second row
                            print("Quit game!")
                            pygame.quit()
                            sys.exit()
                            
        draw_menu(window)
        clock.tick(60)

if __name__ == "__main__":
    main()
