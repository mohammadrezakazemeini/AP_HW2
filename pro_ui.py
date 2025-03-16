import pygame
import time
import os
import sys
from data_handler import *
from game_logic import *

pygame.init()  # تنظیمات اولیه pygame
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

BACKGROUND_COLOR = (187, 173, 160)


def draw_board(screen, board, tile_colors, start_time, score):
    """رسم صفحه بازی و نوار اطلاعات."""
    screen.fill(BACKGROUND_COLOR)
    for i in range(4):
        for j in range(4):
            tile_value = board[i][j]
            color = tile_colors.get(tile_value, (0, 0, 0))
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE + INFO_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            if tile_value != 0:
                text = FONT.render(str(tile_value), True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2 + INFO_BAR_HEIGHT))
                screen.blit(text, text_rect)

    # Draw info bar
    info_bar_rect = pygame.Rect(0, 0, WINDOW_SIZE, INFO_BAR_HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), info_bar_rect)
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    time_text = FONT.render(f"Time: {int(time.time() - start_time)}s", True, (0, 0, 0))
    screen.blit(time_text, (WINDOW_SIZE - 150, 10))
    pygame.display.flip()


def handle_game_events(board, start_time, data, score):
    """مدیریت رویدادهای بازی."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_data(board, start_time, data, score)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up(board, score)
            elif event.key == pygame.K_DOWN:
                move_down(board, score)
            elif event.key == pygame.K_LEFT:
                move_left(board , score)
            elif event.key == pygame.K_RIGHT:
                move_right(board , score)
            add_new_tile(board)  # Add a new tile after each move
            if check_game_status(board, start_time) == "lose":
                show_message(screen, "You Lose!")
                time.sleep(2)
                homepage_loop()


def save_game_data(board, start_time, data, score):
    """ذخیره اطلاعات بازی."""
    data["last_board"] = board
    data["last_score"] = score
    data["last_time"] = time.time() - start_time
    save_data(data)


def check_game_status(board, start_time):
    """بررسی وضعیت بازی (برد یا باخت)."""
    if any(2048 in row for row in board):
        return "win"
    if not any(0 in row for row in board) and not any_merges_possible(board):
        return "lose"
    return "continue"


def game_loop(board=None):
    """حلقه اصلی بازی."""
    if board is None:
        board = [[0] * 4 for _ in range(4)]
        add_new_tile(board)
        add_new_tile(board)
    start_time = time.time()
    score = 0
    data = load_data()
    while True:
        draw_board(screen, board, TILE_COLORS, start_time, score)
        handle_game_events(board, start_time, data, score)


def homepage_loop():
    """حلقه اصلی صفحه اصلی بازی."""
    menu_options = ["Start Game", "Records", "Quit"]
    music_enabled = True
    data = load_data()
    while True:
        clear_screen()
        display_title("2048")
        display_menu(menu_options)
        display_music_status(music_enabled)
        handle_homepage_events(menu_options, music_enabled, data)
        pygame.display.flip()


def setup_music(music_enabled):
    """تنظیمات موسیقی."""
    if music_enabled:
        pygame.mixer.music.load("src/sounds/A Lil BIT [acx-FPUKVl4].mp3")
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def draw_button(screen, text, font, color, hover_color, rect, hovered):
    """رسم دکمه با قابلیت hover."""
    button_color = hover_color if hovered else color
    pygame.draw.rect(screen, button_color, rect)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def clear_screen():
    """پاک کردن صفحه."""
    screen.fill(BACKGROUND_COLOR)


def display_title(title, font_size=72):
    """نمایش عنوان بازی."""
    title_font = pygame.font.Font(None, font_size)
    title_surface = title_font.render(title, True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
    screen.blit(title_surface, title_rect)


def display_menu(menu_options):
    """نمایش گزینه‌های منو."""
    menu_font = pygame.font.Font(None, 48)
    for i, option in enumerate(menu_options):
        text_surface = menu_font.render(option, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + i * 50))
        screen.blit(text_surface, text_rect)


def display_music_status(music_enabled):
    """نمایش وضعیت موسیقی."""
    status = "ON" if music_enabled else "OFF"
    status_font = pygame.font.Font(None, 36)
    status_surface = status_font.render(f"Music: {status}", True, (0, 0, 0))
    status_rect = status_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - 50))
    screen.blit(status_surface, status_rect)


def get_text_rect(text, font, x, y):
    """محاسبه موقعیت متن."""
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface.get_rect(center=(x, y))


def handle_homepage_events(menu_options, music_enabled, data):
    """مدیریت رویدادهای کاربر."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, option in enumerate(menu_options):
                text_rect = get_text_rect(option, pygame.font.Font(None, 48), WINDOW_SIZE // 2,
                                          WINDOW_SIZE // 2 + i * 50)
                if text_rect.collidepoint(mouse_pos):
                    handle_menu_selection(option)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                music_enabled = not music_enabled
                setup_music(music_enabled)


def records_loop():
    """حلقه صفحه رکوردها."""
    data = load_data()
    top_scores = data.get("top_scores", [])
    while True:
        clear_screen()
        display_title("Records")
        display_records(top_scores)
        display_back_button()
        handle_records_events()
        pygame.display.flip()


def display_records(top_scores):
    """نمایش رکوردها."""
    records_font = pygame.font.Font(None, 36)
    for i, score in enumerate(top_scores):
        text_surface = records_font.render(f"{i + 1}. {score}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + i * 40))
        screen.blit(text_surface, text_rect)


def display_back_button():
    """نمایش دکمه برگشت به خانه و بررسی کلیک روی آن."""
    back_font = pygame.font.Font(None, 36)
    back_text = "Back"
    text_surface = back_font.render(back_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - 50))
    screen.blit(text_surface, text_rect)
    mouse_pos = pygame.mouse.get_pos()
    if text_rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            homepage_loop()


def handle_records_events():
    """مدیریت رویدادهای صفحه رکوردها (مانند بستن پنجره)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def show_message(screen, message):
    """نمایش پیام روی صفحه."""
    message_font = pygame.font.Font(None, 48)
    message_surface = message_font.render(message, True, (0, 0, 0))
    message_rect = message_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(message_surface, message_rect)
    pygame.display.flip()


def handle_menu_selection(selected_option):
    """مدیریت انتخاب گزینه."""
    if selected_option == "Start Game":
        game_loop()
    elif selected_option == "Records":
        records_loop()
    elif selected_option == "Quit":
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    homepage_loop()