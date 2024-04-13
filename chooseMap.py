import pygame
import sys
import subprocess
import sys

# Các màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (64, 164, 223)
RED = (255, 0, 0)

# Kích thước cửa sổ
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
if len(sys.argv) <2:
    subprocess.Popen(["python", "menu.py"])  # Quay về menu.py
    pygame.quit()  # Thoát khỏi cửa sổ hiện tại
    sys.exit()
file = sys.argv[1]
def draw_menu(window):
    # Load background image
    background_image = pygame.image.load("chooseMapBg.png")
    window.blit(background_image, (0, 0))
    

    font_option = pygame.font.SysFont('Courier New', 40)
      
    
    # Vẽ các lựa chọn
    options = ["Map 1", "Map 2", "Map 3", "Exit"]
    row1 = options[:2]
    row2 = options[2:]
    
    for i, option in enumerate(row1):
        text_color = BLACK
        if option == "Exit":
            text_color = RED
        text = font_option.render(option, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2 - 230, 378 + i * 132))
        window.blit(text, text_rect)
    
    for i, option in enumerate(row2):
        text_color = BLACK
        if option == "Exit":
            text_color = WHITE
        text = font_option.render(option, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2 + 230, 378 + i * 132))
        window.blit(text, text_rect)

    font_option = pygame.font.SysFont('Courier New', 25)
    text = font_option.render("No Padding", True, BLACK)
    text_rect = text.get_rect(center=(515,  613))
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
                    print(mouse_pos)
                    
                    if 338 <= mouse_pos[1] <= 412:
                        if 198 <= mouse_pos[0] <= 376:
                            print("Map 1!")
                            subprocess.Popen(["python",file, "input1.txt"]) 
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 647 <= mouse_pos[0] <= 823:
                            print("Map 3!")
                            subprocess.Popen(["python", file,"input3.txt"])
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                    
                    elif 474 <= mouse_pos[1] <= 539:
                        if 198 <= mouse_pos[0] <= 376:
                            print("Map 2!")
                            subprocess.Popen(["python", file,"input2.txt"])
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()
                        elif 647 <= mouse_pos[0] <= 823:
                            # Nút "Quay lại" được nhấp
                            print("Exit!")
                            subprocess.Popen(["python", "menu.py"])  # Quay về menu.py
                            pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                            sys.exit()

                    elif 575 <= mouse_pos[1] <= 647:
                         if 424 <= mouse_pos[0] <= 601 :
                            print("No Padding!")
                            subprocess.Popen(["python", file,"no_padding.txt"])
                            pygame.quit()
                            sys.exit()
                         
        
        draw_menu(window)
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
