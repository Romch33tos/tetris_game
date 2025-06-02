import tkinter as tk
import random

WIDTH = 300
HEIGHT = 600
BLOCK_SIZE = 25
COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
SPEED = 400
FAST_DROP_SPEED = 50
MOVE_SPEED = 50

COLORS = ['cyan', 'blue', 'orange', 'yellow', 'lime', 'purple3', 'red']

SHAPES = [
  [[1, 1, 1, 1]],
  [[1, 1, 1], [0, 0, 1]],
  [[1, 1, 1], [1, 0, 0]],
  [[1, 1], [1, 1]],
  [[0, 1, 1], [1, 1, 0]],
  [[1, 1, 1], [0, 1, 0]],
  [[1, 1, 0], [0, 1, 1]]
]

class Tetris:
  def __init__(self, root):
    self.root = root
    self.root.title("Тетрис")
    self.root.resizable(0, 0)
    self.main_frame = tk.Frame(root)
    self.main_frame.pack()
    self.game_frame = tk.Frame(self.main_frame)
    self.game_frame.pack(side='left')
    self.canvas = tk.Canvas(self.game_frame, width=WIDTH, height=HEIGHT, bg='black')
    self.canvas.pack()
    self.next_frame = tk.Frame(self.main_frame)
    self.next_frame.pack(side='left', padx=20)
    self.next_label = tk.Label(self.next_frame, text="Следующий блок", font=("Calibri", 14))
    self.next_label.pack(pady=5)
    self.next_piece_canvas = tk.Canvas(self.next_frame, width=BLOCK_SIZE*4, height=BLOCK_SIZE*4, bg='black')
    self.next_piece_canvas.pack()
    self.score = 0
    self.score_label = tk.Label(self.root, text=f"Счёт: {self.score}", font=("Calibri", 16))
    self.score_label.place(relx=0.98, rely=0.01, anchor='ne')
    self.current_piece = None
    self.current_piece_color = None
    self.current_x = 0
    self.current_y = 0
    self.fast_drop_enabled = True
    self.game_over_flag = False
    self.is_fast_dropping = False
    self.game_over_text = None
    self.start_text = None
    self.start_text = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Нажми, чтобы начать игру!", fill="white", font=("Calibri", 16))
    self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    self.root.bind('<Left>', self.move_left)
    self.root.bind('<Right>', self.move_right)
    self.root.bind('<Down>', self.start_fast_drop)
    self.root.bind('<Up>', self.rotate)
    self.canvas.bind("<Button-1>", self.start_game)
    self.current_speed = SPEED
    self.update_score_label()

  def update_score_label(self):
    self.score_label.config(text=f"Счёт: {self.score}")

  def update_next_piece(self):
    index = random.randint(0, len(SHAPES) - 1)
    self.next_piece = SHAPES[index]
    self.next_piece_color = COLORS[index]
    self.draw_next_piece()

  def draw_next_piece(self):
    self.next_piece_canvas.delete(tk.ALL)
    piece_width = len(self.next_piece[0]) * BLOCK_SIZE
    piece_height = len(self.next_piece) * BLOCK_SIZE
    offset_x = (self.next_piece_canvas.winfo_width() - piece_width) // 2
    offset_y = (self.next_piece_canvas.winfo_height() - piece_height) // 2
    for y, row in enumerate(self.next_piece):
      for x, cell in enumerate(row):
        if cell:
          self.next_piece_canvas.create_rectangle(
            offset_x + x * BLOCK_SIZE,
            offset_y + y * BLOCK_SIZE,
            offset_x + x * BLOCK_SIZE + BLOCK_SIZE,
            offset_y + y * BLOCK_SIZE + BLOCK_SIZE,
            fill=self.next_piece_color, outline='gray'
          )

  def start_game(self, event):
    if self.start_text:
      self.canvas.delete(self.start_text)
      self.start_text = None
    self.next_piece = None
    self.next_piece_color = None
    self.update_next_piece()
    self.spawn_piece()
    self.update()
    self.canvas.unbind("<Button-1>")
    self.canvas.bind("<Button-1>", self.restart_game)

  def spawn_piece(self):
    if self.next_piece is None:
      self.update_next_piece()
    self.current_piece = self.next_piece
    self.current_piece_color = self.next_piece_color
    self.current_x = COLS // 2 - len(self.current_piece[0]) // 2
    self.current_y = 0
    self.update_next_piece()
    if self.check_collision(self.current_x, self.current_y):
      self.game_over()

  def game_over(self):
    self.canvas.create_rectangle(0, HEIGHT // 2 - 20, WIDTH, HEIGHT // 2 + 20, fill='black')
    self.game_over_text = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Конец игры!", fill="white", font=("Calibri", 18))
    if hasattr(self, 'after_id'):
      self.root.after_cancel(self.after_id)
    self.game_over_flag = True

  def restart_game(self, event):
    if self.game_over_flag:
      self.score = 0
      self.update_score_label()
      self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
      self.game_over_flag = False
      self.current_speed = SPEED
      self.spawn_piece()
      self.update()
      if self.game_over_text:
        self.canvas.delete(self.game_over_text)
        self.game_over_text = None

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

  def rotate(self, event=None):
    original_piece = self.current_piece
    self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]
    if self.check_collision(self.current_x, self.current_y):
      self.current_piece = original_piece

  def move_left(self, event=None):
    if not self.check_collision(self.current_x - 1, self.current_y):
      self.current_x -= 1
      self.draw_board()

  def move_right(self, event=None):
    if not self.check_collision(self.current_x + 1, self.current_y):
      self.current_x += 1
      self.draw_board()

  def start_fast_drop(self, event=None):
    if self.fast_drop_enabled and not self.game_over_flag:
      self.fast_drop_enabled = False
      self.is_fast_dropping = True
      self.fast_drop_animation()

  def fast_drop_animation(self):
    if not self.check_collision(self.current_x, self.current_y + 1):
      self.current_y += 1
      self.draw_board()
      self.root.after(FAST_DROP_SPEED, self.fast_drop_animation)
    else:
      self.merge_piece()

  def merge_piece(self):
    for y, row in enumerate(self.current_piece):
      for x, cell in enumerate(row):
        if cell:
          self.board[self.current_y + y][self.current_x + x] = self.current_piece_color
    self.clear_lines()
    self.fast_drop_enabled = True
    self.spawn_piece()
    self.is_fast_dropping = False

  def clear_lines(self):
    lines_to_clear = []
    for y in range(ROWS):
      if all(self.board[y]):
        lines_to_clear.append(y)
    for y in lines_to_clear:
      del self.board[y]
      self.board.insert(0, [0 for _ in range(COLS)])
      self.score += 100
      if self.score // 100 > (self.score - 100) // 100:
        self.current_speed = self.current_speed - 10
    self.update_score_label()

  def draw_board(self):
    self.canvas.delete(tk.ALL)
    for y in range(ROWS):
      for x in range(COLS):
        color = self.board[y][x]
        if color:
          self.canvas.create_rectangle(
            x * BLOCK_SIZE, y * BLOCK_SIZE,
            (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE,
            fill=color, outline='gray'
          )
    for y, row in enumerate(self.current_piece):
      for x, cell in enumerate(row):
        if cell:
          self.canvas.create_rectangle(
            (self.current_x + x) * BLOCK_SIZE,
            (self.current_y + y) * BLOCK_SIZE,
            (self.current_x + x + 1) * BLOCK_SIZE,
            (self.current_y + y + 1) * BLOCK_SIZE,
            fill=self.current_piece_color, outline='gray'
          )
    if self.game_over_flag and self.game_over_text:
      self.canvas.create_rectangle(0, HEIGHT // 2 - 20, WIDTH, HEIGHT // 2 + 20, fill='black')
      self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Конец игры!", fill="white", font=("Calibri", 18))

  def update(self):
    if not self.game_over_flag:
      if not self.is_fast_dropping:
        if not self.check_collision(self.current_x, self.current_y + 1):
          self.current_y += 1
        else:
          self.merge_piece()
      self.draw_board()
      self.after_id = self.root.after(self.current_speed, self.update)

if __name__ == "__main__":
  root = tk.Tk()
  game = Tetris(root)
  root.mainloop()
