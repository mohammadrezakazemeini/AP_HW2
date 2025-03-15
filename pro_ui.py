import pygame
import time
import os
import sys
from data_handler import *
from game_logic import *

pygame.init()
WINDOW_SIZE = 500
INFO_BAR_HEIGHT = 50
CELL_SIZE = (WINDOW_SIZE - INFO_BAR_HEIGHT) // 4
screen = pygame.display.set_mode((CELL_SIZE * 4, WINDOW_SIZE))
pygame.display.set_caption("2048")
icon_path = "src/images/2048-icon.png"
icon_image = pygame.image.load(icon_path)
pygame.display.set_icon(icon_image)
FONT_SIZE = 36
FONT = pygame.font.Font(None, FONT_SIZE)

TILE_COLORS = {
    2:(0, 13, 255),
    4:(119,0,228),
    8:(156,0,191),
    16:(177,0,164),
    32:(193,0,144),
    64:(206,0,128),
    128:(218,0,112),
    256:(230,0,96),
    512:(241,0,77),
    1024:(252,0,51),
    2048:(255,0,0)
}
BACKGROUND_COLOR = (224, 255, 219)

def draw_board(screen, board, tile_colors, start_time, score):
    screen.fill(BACKGROUND_COLOR)
    for row in range(4):
        for col in range(4):
            y = row * CELL_SIZE
            x = col * CELL_SIZE + INFO_BAR_HEIGHT
            value = board[row][col]
            title_color = tile_colors.get[value,  (205, 193, 180)]
            pygame.draw.rect(screen, title_color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
            if value != 0:
                text = FONT.render(str(value), True, (120, 110, 100))
                text_rect = text.get_rect(center= (x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)
    pygame.draw.rect(screen, (190,170,160), (0,0,WINDOW_SIZE,INFO_BAR_HEIGHT))
    score_text = FONT.render(f"Score: {score}", True, (120, 110, 100))
    screen.blit(score_text, (10, 10))

    time_elapsed = int(time.time()-start_time)
    time_text = FONT.render(f"Time: {time_elapsed}", True, (120, 110, 100))
    screen.blit(time_text, (10,10))
    pygame.display.update()

def handle_game_events(board, start_time, data, score):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_data(board, start_time, data, score)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass



def save_game_data(board, start_time, data, score):
    game_state = {
        "grid": board,
        "score": score,
        "start_time": start_time,
    }
    save_data([game_state], file_path= 'data.txt')

def check_game_status(board, start_time):
    for row in board:
        if 2048 in row:
            show_message(screen, f"YOU WIN!")
            return True
    return False

def game_loop(board=None):
    if board is None:
        board = [[0]* 4 for _ in range(4)]
    score = 0
    start_time = time.time()

    while True:
        draw_board(screen, board, TILE_COLORS, start_time, score)
        handle_game_events(board, start_time, board, score)
        if check_game_status(board, start_time):
            break
        time.sleep(0.1)

def homepage_loop():
    menu_options = {"START GAME", "VIEW RECORDS", "EXIT"}
    while True:
        display_menu(menu_options)
        handle_homepage_events(menu_options, music_enabled=False , data=None)

def setup_music(music_enabled):
    if music_enabled:
        pygame.mixer.music.load("A Lil BIT [acx-FPUKVl4].mp3")
        pygame.mixer.music.play(-1, 0.0)
    else:
        pygame.mixer.music.stop()
def draw_button(screen, text, font, color, hover_color, rect, hovered):
    color = hover_color if hovered else color
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (225, 225, 225))
    text_rect = text_surface.get_rect((text_surface.get_width()//2, text_surface.get_height()//2))
    screen.blit(text_surface, text_rect)

def clear_screen():
    screen.fill(BACKGROUND_COLOR)

def display_title(title, font_size=72):
    title_font = pygame.font.Font("none", font_size)
    title_surface = title_font.render(title, True, (225, 225, 225))
    title_rect = title_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//4))
    screen.blit(title_surface, title_rect)

def display_menu(menu_options):
    clear_screen()
    display_title("2048", font_size=72 )

    button_height = 50
    for index, option in enumerate(menu_options):
        rect = pygame.Rect(150, 150 + (index * (button_height+20)) , 200, button_height)
        draw_button(screen, option, FONT, (0,122, 204), (0,225,225),rect, False)
    pygame.display.update()

def display_music_status(music_enabled):
    music_text = "MUSIC : ON" if music_enabled else "MUSIC : OFF"
    music_surface = FONT.render(music_text, True, (225, 225, 225))
    music_rect = music_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE - 40))
    screen.blit(music_surface, music_rect)
    pygame.display.update()

def get_text_rect(text, font, x, y):
    text_surface = font.render(text, True, (225, 225, 225))
    text_rect = text_surface.get_rect(center=(x, y))
    return text_rect

def handle_homepage_events(menu_options, music_enabled, data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 150 <= event.pos[0] <= 350:
                if 150 <= event.pos[1] <= 200:
                    game_loop()
                elif 200 <= event.pos[1] <= 250:
                    records_loop()


def records_loop():
    top_scores= load_data(file_path= 'data.txt' )
    while True:
        display_records(top_scores)
        handle_records_events()

def display_records(top_scores):
    clear_screen()
    display_title("HIGH SCORES")
    y_offset = 150
    for scores in top_scores:
        score_text = FONT.render(f"{scores}", True, (225, 225, 225))
        screen.blit(score_text, (WINDOW_SIZE//2- score_text.get_width()//2, y_offset))
        y_offset += 40
    pygame.display.update()

def display_back_button():
    rect = pygame.Rect(10, WINDOW_SIZE-50, 100, 40)
    draw_button(screen, "Back", FONT, (0,122, 204), (0,225,225),rect, False)

def handle_records_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def show_message(screen, message):
    message_text = FONT.render(message, True, (225, 225, 225))
    message_rect = message_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
    screen.blit(message_text, message_rect)
    pygame.display.update()
    time.sleep(2)

def handle_menu_selection(selected_option):
    if selected_option == "Start Game":
        game_loop()
    elif selected_option == "View Records":
        records_loop()
    elif selected_option == "Exit":
        pygame.quit()
        sys.exit()