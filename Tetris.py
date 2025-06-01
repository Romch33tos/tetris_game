import tkinter as tk
import random

# Параметры игры
WIDTH = 300
HEIGHT = 600
BLOCK_SIZE = 30  # Размер блока
COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
SPEED = 400  # Скорость падения блоков

# Яркие цвета фигур
COLORS = ['cyan', 'blue', 'orange', 'yellow', 'lime', 'purple3', 'red']

# Фигуры
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]]   # Z
]

class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("Тетрис")
        self.root.resizable(0,0)
        
        self.score = 0
        self.score_label = tk.Label(root, text=f"Счёт: {self.score}")
        self.score_label.pack(side = "top", pady = 5)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        

        self.current_piece = None
        self.current_piece_color = None
        self.current_x = 0
        self.current_y = 0

        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<Down>', self.drop_fast)
        self.root.bind('<Up>', self.rotate)

        # Создаем кнопки
        self.btn_frame = tk.Frame(root)
        

        self.btn_left = tk.Button(self.btn_frame, text="←", command=self.move_left, width = 2, height = 2)
        self.btn_left.pack(side= "left", padx = 5, pady = 10)

        self.btn_right = tk.Button(self.btn_frame, text="→", command=self.move_right, width = 2, height = 2)
        self.btn_right.pack(side = "right", padx = 5, pady = 10)

        self.btn_rotate = tk.Button(self.btn_frame, text="↺", command=self.rotate, width = 2, height = 2)
        self.btn_rotate.pack(side = "top", padx = 5, pady = 10)
        self.btn_fast_drop = tk.Button(self.btn_frame, text="↓", command=self.drop_fast, width = 2, height = 2)
        self.btn_fast_drop.pack(side = "bottom", padx = 5, pady = 10)
        self.btn_frame.pack()

        self.spawn_piece()
        self.update()

    def spawn_piece(self):
        index = random.randint(0, len(SHAPES) - 1)
        self.current_piece = SHAPES[index]
        self.current_piece_color = COLORS[index]
        self.current_x = COLS // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0

        # Проверка на коллизию перед тем, как разместить новую фигуру
        if self.check_collision(self.current_x, self.current_y):
            self.game_over()

    def game_over(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="white", font=("Arial", 10))
        self.root.after_cancel(self.after_id)

    def check_collision(self, x_offset, y_offset):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    board_x = x + x_offset
                    board_y = y + y_offset
                    if (board_x < 0 or board_x >= COLS or 
                        board_y >= ROWS or (board_y >= 0 and self.board[board_y][board_x])):
                        return True
        return False

    def rotate(self):
        self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]
        if self.check_collision(self.current_x, self.current_y):
            self.current_piece = [list(row) for row in zip(*self.current_piece)][::-1]  # Возврат на место

    def move_left(self, event=None):
        if not self.check_collision(self.current_x - 1, self.current_y):
            self.current_x -= 1

    def move_right(self, event=None):
        if not self.check_collision(self.current_x + 1, self.current_y):
            self.current_x += 1

    def drop_fast(self, event=None):
        while not self.check_collision(self.current_x, self.current_y + 1):
            self.current_y += 1
        self.merge_piece()

    def merge_piece(self):
        
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_y + y][self.current_x + x] = self.current_piece_color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        lines_to_clear = []
        for y in range(ROWS):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0 for _ in range(COLS)])
                       
            self.score += 100  # Увеличен счет за линию

        self.score_label.config(text=f"Счёт: {self.score}")

    def draw_board(self):
        self.canvas.delete(tk.ALL)
        for y in range(ROWS):
            for x in range(COLS):
                color = self.board[y][x]
                if color:
                    self.canvas.create_rectangle(x * BLOCK_SIZE, y * BLOCK_SIZE, 
                                                  x * BLOCK_SIZE + BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE, 
                                                  fill=color, outline='gray')

        # Рисуем текущую фигуру
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle((self.current_x + x) * BLOCK_SIZE, 
                                                  (self.current_y + y) * BLOCK_SIZE,
                                                  (self.current_x + x + 1) * BLOCK_SIZE, 
                                                  (self.current_y + y + 1) * BLOCK_SIZE,
                                                  fill=self.current_piece_color, outline='gray')

    def update(self):
        # Плавное падение блока
        if not self.check_collision(self.current_x, self.current_y + 1):
            self.current_y += 1
        else:
            self.merge_piece()

        self.draw_board()
        self.after_id = self.root.after(SPEED, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = Tetris(root)
    root.mainloop()
    