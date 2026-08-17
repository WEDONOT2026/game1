import json
import os
from config import GRID_SIZE, W_GRID, H_GRID

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_FILE = os.path.join(BASE_DIR, "maps.json")

class MapManager:
    def __init__(self):
        self.map_data = None
        self.obstacles = []
        self.wall_mode = False
        self.current_map_info = {}
        self.load_maps()

    def load_maps(self):
        try:
            with open(MAPS_FILE, "r", encoding="utf-8") as f:
                self.map_data = json.load(f)
        except FileNotFoundError:
            print("Map file not found: " + MAPS_FILE)
            self.map_data = {"maps": [{"id": 0, "name": "Right", "food_count": 10, "wall_mode": False, "obstacles": []}]}
        except Exception as e:
            print("Load map failed: " + str(e))
            self.map_data = {"maps": [{"id": 0, "name": "Right", "food_count": 10, "wall_mode": False, "obstacles": []}]}

    def get_map_by_level(self, level):
        maps = self.map_data.get("maps", [])
        if not maps:
            return {"id": 0, "name": "Right", "food_count": 10, "wall_mode": False, "obstacles": []}
        map_index = min((level - 1) // 10, len(maps) - 1)
        return maps[map_index]

    def generate_map(self, level):
        self.obstacles = []
        map_info = self.get_map_by_level(level)
        self.current_map_info = map_info
        self.wall_mode = map_info.get("wall_mode", False)

        for obs in map_info.get("obstacles", []):
            col = obs.get("col", 0)
            row = obs.get("row", 0)
            if 0 <= col < W_GRID and 0 <= row < H_GRID:
                self.obstacles.append((col * GRID_SIZE, row * GRID_SIZE))
        return map_info

    def get_food_count(self, level):
        map_info = self.get_map_by_level(level)
        return map_info.get("food_count", 10)

    def get_current_name(self):
        return self.current_map_info.get("name", "Unknown")

    def is_obstacle(self, pos):
        return pos in self.obstacles

    def is_wall_collision(self, pos, wall_mode):
        if not wall_mode:
            return False
        x, y = pos
        return x < 0 or x >= 600 or y < 0 or y >= 600
