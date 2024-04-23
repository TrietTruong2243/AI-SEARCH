# import pygame
# import sys
# import subprocess
# import pygame.font
# import time

# # Khởi tạo Pygame
# pygame.init()

# # Màu sắc
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (200, 200, 200)

# # Cấu hình cửa sổ
# WINDOW_WIDTH = 400
# WINDOW_HEIGHT = 150
# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption("Nhập tốc độ (h tọa độ/s)")
# if len(sys.argv) <2:
#     subprocess.Popen(["python", "menu.py"])  # Quay về menu.py
#     pygame.quit()  # Thoát khỏi cửa sổ hiện tại
#     sys.exit()
# filename = sys.argv[1]
# # Font
# pygame.font.init()
# font = pygame.font.SysFont('Inter', 24) # Chọn font và kích thước
# def main():
#     input_rect = pygame.Rect(150, 50, 140, 32)
#     button_rect = pygame.Rect(300, 50, 80, 32)
#     input_text = ''
    
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     if input_text.isdigit() and int(input_text) > 0:
#                         print("Giá trị đã nhập:", input_text)
#                     else:
#                         print("Vui lòng chỉ nhập số dương.")
#                 elif event.key == pygame.K_BACKSPACE:
#                     input_text = input_text[:-1]
#                 elif event.unicode.isdigit():  # Chỉ cho phép nhập số
#                     input_text += event.unicode
#             # Xử lý sự kiện khi người dùng nhấn vào nút "Chọn"
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if button_rect.collidepoint(event.pos):
#                     subprocess.Popen(["python", "L4_v2.py",filename,input_text])
#                     pygame.quit()  # Thoát khỏi cửa sổ hiện tại
#                     sys.exit()
#                     # if input_text.isdigit() and int(input_text) > 0:
#                     #     print("Giá trị đã nhập:", input_text)
#                     # else:
#                     #     print("Vui lòng chỉ nhập số dương.")
#         # Vẽ màn hình
#         window.fill(WHITE)
        
#         # Vẽ dòng chữ "Nhập tốc độ (h tọa độ/s)"
#         label_surface = font.render("Speed:", False, BLACK)
#         window.blit(label_surface, (50, input_rect.y + 5))
        
#         pygame.draw.rect(window, GRAY, input_rect)
#         pygame.draw.rect(window, BLACK, input_rect, 2)
#         pygame.draw.rect(window, GRAY, button_rect)
#         pygame.draw.rect(window, BLACK, button_rect, 2)
        
#         text_surface = font.render(input_text, False, BLACK)
#         window.blit(text_surface, (input_rect.x + 5, input_rect.y + 8))
        
#         button_text = font.render("Choose", False, BLACK)
#         window.blit(button_text, (button_rect.x + 10, button_rect.y + 8))
        
#         pygame.display.flip()

# if __name__ == "__main__":
#     main()
import pygame
import sys
import subprocess
import pygame.font

# Khởi tạo Pygame
pygame.init()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Cấu hình cửa sổ
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Nhập tốc độ (h tọa độ/s)")

# Font
pygame.font.init()
font = pygame.font.SysFont('Inter', 24) # Chọn font và kích thước
if len(sys.argv) <2:
    subprocess.Popen(["python", "menu.py"])  # Quay về menu.py
    pygame.quit()  # Thoát khỏi cửa sổ hiện tại
    sys.exit()
filename = sys.argv[1]
def main():
    input_rect = pygame.Rect(150, 50, 140, 32)
    # button_rect = pygame.Rect(300, 50, 80, 32)
    type1_button_rect = pygame.Rect(50, 100, 100, 32)
    type2_button_rect = pygame.Rect(200, 100, 100, 32)
    input_text = ''
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit() and int(input_text) > 0:
                        print("Giá trị đã nhập:", input_text)
                    else:
                        print("Vui lòng chỉ nhập số dương.")
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():  # Chỉ cho phép nhập số
                    input_text += event.unicode
            # Xử lý sự kiện khi người dùng nhấn vào nút "Chọn"
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if button_rect.collidepoint(event.pos):
                #     if input_text.isdigit() and int(input_text) > 0:
                #         print("Giá trị đã nhập:", input_text)
                #         # Thực hiện xử lý tại đây khi nhấn nút "Chọn"
                #     else:
                #         print("Vui lòng chỉ nhập số dương.")
                # Xử lý sự kiện khi người dùng nhấn vào nút "Type1"
                if type1_button_rect.collidepoint(event.pos):
                    print("Đã chọn Type1")
                    # Thực hiện xử lý tương ứng cho Type1
                    subprocess.Popen(["python", "L4.py",filename,input_text])
                    pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                    sys.exit()
                # Xử lý sự kiện khi người dùng nhấn vào nút "Type2"
                elif type2_button_rect.collidepoint(event.pos):
                    print("Đã chọn Type2")
                    # Thực hiện xử lý tương ứng cho Type2
                    subprocess.Popen(["python", "L4_v2.py",filename,input_text])
                    pygame.quit()  # Thoát khỏi cửa sổ hiện tại
                    sys.exit()
        # Vẽ màn hình
        window.fill(WHITE)
        
        # Vẽ dòng chữ "Nhập tốc độ (h tọa độ/s)"
        label_surface = font.render("Speed:", False, BLACK)
        window.blit(label_surface, (50, input_rect.y + 5))
        
        pygame.draw.rect(window, GRAY, input_rect)
        pygame.draw.rect(window, BLACK, input_rect, 2)
        # pygame.draw.rect(window, GRAY, button_rect)
        # pygame.draw.rect(window, BLACK, button_rect, 2)
        pygame.draw.rect(window, GRAY, type1_button_rect)
        pygame.draw.rect(window, BLACK, type1_button_rect, 2)
        pygame.draw.rect(window, GRAY, type2_button_rect)
        pygame.draw.rect(window, BLACK, type2_button_rect, 2)
        
        text_surface = font.render(input_text, False, BLACK)
        window.blit(text_surface, (input_rect.x + 5, input_rect.y + 8))
        
        button_text = font.render("Choose", False, BLACK)
        # window.blit(button_text, (button_rect.x + 10, button_rect.y + 8))
        
        type1_button_text = font.render("Type 1", False, BLACK)
        window.blit(type1_button_text, (type1_button_rect.x + 24, type1_button_rect.y + 8))
        
        type2_button_text = font.render("Type 2", False, BLACK)
        window.blit(type2_button_text, (type2_button_rect.x + 24, type2_button_rect.y + 8))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
