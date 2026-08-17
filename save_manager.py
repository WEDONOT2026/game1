import json
import os
from config import GRID_SIZE, W_GRID, H_GRID

SAVE_FILE = "/data/data/com.termux/files/home/save.json"
DEATH_FILE = "/data/data/com.termux/files/home/deaths.json"

class SaveManager:
    def __init__(self):
        self.death_count = 0
        self.load_deaths()

    def load_deaths(self):
        try:
            with open(DEATH_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.death_count = data.get("deaths", 0)
        except:
            self.death_count = 0

    def save_deaths(self):
        try:
            with open(DEATH_FILE, "w", encoding="utf-8") as f:
                json.dump({"deaths": self.death_count}, f, indent=2)
        except:
            pass

    def add_death(self):
        self.death_count += 1
        self.save_deaths()

    def save_progress(self, state, obstacles, wall_mode, food_count):
        data = {
            "level": state.level,
            "score": state.score,
            "lives": state.lives,
            "max_lives": state.max_lives,
            "food_count": state.food_count,
            "snake": [(x//GRID_SIZE, y//GRID_SIZE) for x, y in state.snake],
            "direction": (state.direction[0]//GRID_SIZE, state.direction[1]//GRID_SIZE),
            "next_dir": (state.next_dir[0]//GRID_SIZE, state.next_dir[1]//GRID_SIZE),
            "obstacles": [(x//GRID_SIZE, y//GRID_SIZE) for x, y in obstacles],
            "foods": [(x//GRID_SIZE, y//GRID_SIZE) for x, y in state.foods],
            "game_over": state.game_over,
            "wall_mode": wall_mode,
            "food_count_per_level": food_count
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False

    def load_progress(self, state):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not data:
                return False
            state.level = data.get("level", 1)
            state.score = data.get("score", 0)
            state.lives = data.get("lives", 3)
            state.max_lives = data.get("max_lives", 3)
            state.food_count = data.get("food_count", 0)
            state.game_over = data.get("game_over", False)
            state.snake = [(x * GRID_SIZE, y * GRID_SIZE) for x, y in data.get("snake", [(W_GRID//2, H_GRID//2)])]
            d = data.get("direction", (1, 0))
            state.direction = (d[0] * GRID_SIZE, d[1] * GRID_SIZE)
            nd = data.get("next_dir", (1, 0))
            state.next_dir = (nd[0] * GRID_SIZE, nd[1] * GRID_SIZE)
            state.input_queue.clear()
            obstacles = [(x * GRID_SIZE, y * GRID_SIZE) for x, y in data.get("obstacles", [])]
            foods = [(x * GRID_SIZE, y * GRID_SIZE) for x, y in data.get("foods", [])]
            state.invincible = False
            wall_mode = data.get("wall_mode", False)
            return obstacles, foods, wall_mode
        except:
            return None

    def has_save(self):
        return os.path.exists(SAVE_FILE) and os.path.getsize(SAVE_FILE) > 10

    def delete_save(self):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
