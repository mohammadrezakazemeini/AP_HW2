import random

def set_board(size):
    """
    ایجاد صفحه بازی با اندازه مشخص و پر کردن دو خانه اول.
    """
    # Create an empty board
    board = [[0] * size for _ in range(size)]
    # Add two initial tiles (2 or 4)
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    """
    Adds a new tile (either 2 or 4) to a random empty cell on the board.
    """
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])  # 90% chance for 2, 10% for 4

def fill_board(board):
    """
    پر کردن خانه‌های خالی با یک عدد جدید (2 یا 4).
    """
    empty_cells = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])  # 90% chance for 2, 10% for 4

def move_left(board, score):
    """
    حرکت به چپ و ادغام خانه‌های مشابه.
    """
    for row in board:
        # Remove zeros
        non_zero_tiles = [tile for tile in row if tile != 0]
        # Merge tiles
        merged_tiles = []
        i = 0
        while i < len(non_zero_tiles):
            if i + 1 < len(non_zero_tiles) and non_zero_tiles[i] == non_zero_tiles[i + 1]:
                merged_tiles.append(non_zero_tiles[i] * 2)
                score += non_zero_tiles[i] * 2  # Update score
                i += 2
            else:
                merged_tiles.append(non_zero_tiles[i])
                i += 1
        # Fill the rest with zeros
        merged_tiles += [0] * (len(row) - len(merged_tiles))
        # Update the row
        row[:] = merged_tiles
    return score

def move_right(board, score):
    """
    حرکت به راست و ادغام خانه‌های مشابه.
    """
    for row in board:
        # Remove zeros
        non_zero_tiles = [tile for tile in row if tile != 0]
        # Merge tiles
        merged_tiles = []
        i = len(non_zero_tiles) - 1
        while i >= 0:
            if i - 1 >= 0 and non_zero_tiles[i] == non_zero_tiles[i - 1]:
                merged_tiles.insert(0, non_zero_tiles[i] * 2)
                score += non_zero_tiles[i] * 2  # Update score
                i -= 2
            else:
                merged_tiles.insert(0, non_zero_tiles[i])
                i -= 1
        # Fill the rest with zeros
        merged_tiles = [0] * (len(row) - len(merged_tiles)) + merged_tiles
        # Update the row
        row[:] = merged_tiles
    return score

def move_up(board, score):
    """
    حرکت به بالا و ادغام خانه‌های مشابه.
    """
    for col in range(len(board[0])):
        # Extract the column
        column = [board[row][col] for row in range(len(board))]
        # Remove zeros
        non_zero_tiles = [tile for tile in column if tile != 0]
        # Merge tiles
        merged_tiles = []
        i = 0
        while i < len(non_zero_tiles):
            if i + 1 < len(non_zero_tiles) and non_zero_tiles[i] == non_zero_tiles[i + 1]:
                merged_tiles.append(non_zero_tiles[i] * 2)
                score += non_zero_tiles[i] * 2  # Update score
                i += 2
            else:
                merged_tiles.append(non_zero_tiles[i])
                i += 1
        # Fill the rest with zeros
        merged_tiles += [0] * (len(column) - len(merged_tiles))
        # Update the column
        for row in range(len(board)):
            board[row][col] = merged_tiles[row]
    return score

def move_down(board, score):
    """
    حرکت به پایین و ادغام خانه‌های مشابه.
    """
    for col in range(len(board[0])):
        # Extract the column
        column = [board[row][col] for row in range(len(board))]
        # Remove zeros
        non_zero_tiles = [tile for tile in column if tile != 0]
        # Merge tiles
        merged_tiles = []
        i = len(non_zero_tiles) - 1
        while i >= 0:
            if i - 1 >= 0 and non_zero_tiles[i] == non_zero_tiles[i - 1]:
                merged_tiles.insert(0, non_zero_tiles[i] * 2)
                score += non_zero_tiles[i] * 2  # Update score
                i -= 2
            else:
                merged_tiles.insert(0, non_zero_tiles[i])
                i -= 1
        # Fill the rest with zeros
        merged_tiles = [0] * (len(column) - len(merged_tiles)) + merged_tiles
        # Update the column
        for row in range(len(board)):
            board[row][col] = merged_tiles[row]
    return score

def board_completed(board):
    """
    بررسی پر شدن صفحه (عدم وجود خانه خالی).
    """
    for row in board:
        if 0 in row:
            return False
    return True

def any_move(board):
    """
    بررسی امکان حرکت بیشتر (ادغام خانه‌های مشابه).
    """
    size = len(board)
    for i in range(size):
        for j in range(size):
            if j + 1 < size and board[i][j] == board[i][j + 1]:
                return True
            if i + 1 < size and board[i][j] == board[i + 1][j]:
                return True
    return False

def any_merges_possible(board):
    """
    بررسی امکان ادغام خانه‌های مشابه در صفحه.
    """
    size = len(board)
    for i in range(size):
        for j in range(size):
            # Check right neighbor
            if j + 1 < size and board[i][j] == board[i][j + 1]:
                return True
            # Check bottom neighbor
            if i + 1 < size and board[i][j] == board[i + 1][j]:
                return True
    return False

def win(board):
    """
    بررسی برد (وجود خانه با مقدار 2048).
    """
    for row in board:
        if 2048 in row:
            return True
    return False