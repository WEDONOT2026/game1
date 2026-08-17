from collections import deque
from config import GRID_SIZE, W_GRID, H_GRID, INITIAL_LIVES, MAX_LIVES

class GameState:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = INITIAL_LIVES
        self.max_lives = MAX_LIVES
        self.food_count = 0
        self.foods = []
        # 初始方向改为向上，避免第一关直接撞右墙
        self.snake = [(W_GRID//2 * GRID_SIZE, H_GRID//2 * GRID_SIZE)]
        self.direction = (0, -GRID_SIZE)  # 向上
        self.next_dir = (0, -GRID_SIZE)   # 向上
        self.input_queue = deque(maxlen=2)
        self.game_over = False
        self.invincible = False
        self.invincible_timer = 0

    def reset_snake(self, spawn_pos, safe_dir):
        self.snake = [(spawn_pos[0], spawn_pos[1])]
        self.direction = safe_dir
        self.next_dir = safe_dir
        self.input_queue.clear()

    def reset_all(self, spawn_pos, safe_dir):
        self.level = 1
        self.score = 0
        self.lives = INITIAL_LIVES
        self.food_count = 0
        self.snake = [(spawn_pos[0], spawn_pos[1])]
        self.direction = safe_dir
        self.next_dir = safe_dir
        self.input_queue.clear()
        self.game_over = False
        self.invincible = False
        self.foods = []
