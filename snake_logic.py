import random
import time
from config import GRID_SIZE, W_GRID, H_GRID, INVINCIBLE_DURATION

def find_safe_spawn(obstacles, snake, foods, wall_mode):
    def is_obstacle(pos):
        return pos in obstacles

    def is_safe_position(pos):
        x, y = pos
        if x < 0 or x >= 600 or y < 0 or y >= 600:
            return False
        if is_obstacle(pos):
            return False
        return True

    center_x = W_GRID//2 * GRID_SIZE
    center_y = (H_GRID//2) * GRID_SIZE
    for radius in range(0, 15):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = center_x + dx * GRID_SIZE
                y = center_y + dy * GRID_SIZE
                pos = (x, y)
                if is_safe_position(pos):
                    safe_dirs = []
                    for d in [(GRID_SIZE,0), (-GRID_SIZE,0), (0,GRID_SIZE), (0,-GRID_SIZE)]:
                        neighbor = (x + d[0], y + d[1])
                        if is_safe_position(neighbor):
                            safe_dirs.append(d)
                    if safe_dirs:
                        return pos, safe_dirs[0]
    for x in range(0, 600, GRID_SIZE):
        for y in range(0, 600, GRID_SIZE):
            pos = (x, y)
            if is_safe_position(pos):
                return pos, (0, -GRID_SIZE)  # 默认向上
    return (GRID_SIZE, GRID_SIZE), (0, -GRID_SIZE)  # 默认向上

def spawn_food(snake, foods, obstacles, wall_mode, level, map_manager):
    for _ in range(200):
        x = random.randint(0, W_GRID - 1) * GRID_SIZE
        y = random.randint(0, H_GRID - 1) * GRID_SIZE
        if wall_mode and (x == 0 or x == 600 - GRID_SIZE or y == 0 or y == 600 - GRID_SIZE):
            continue
        if (x, y) not in snake and (x, y) not in foods and not map_manager.is_obstacle((x, y)):
            return (x, y)
    for x in range(0, 600, GRID_SIZE):
        for y in range(0, 600, GRID_SIZE):
            if wall_mode and (x == 0 or x == 600 - GRID_SIZE or y == 0 or y == 600 - GRID_SIZE):
                continue
            if (x, y) not in snake and (x, y) not in foods and not map_manager.is_obstacle((x, y)):
                return (x, y)
    return (GRID_SIZE, GRID_SIZE)

def init_foods(snake, foods, obstacles, wall_mode, level, map_manager):
    foods.clear()
    food_target = map_manager.get_food_count(level)
    for _ in range(food_target):
        foods.append(spawn_food(snake, foods, obstacles, wall_mode, level, map_manager))
    return foods

def reset_snake_position(state, obstacles, foods, wall_mode, map_manager):
    current_len = len(state.snake) if state.snake else 3
    spawn_pos, safe_dir = find_safe_spawn(obstacles, state.snake, foods, wall_mode)
    new_snake = []
    for i in range(current_len):
        new_snake.append((spawn_pos[0] - i * GRID_SIZE, spawn_pos[1]))
    state.snake = new_snake
    state.direction = safe_dir
    state.next_dir = safe_dir
    state.input_queue.clear()
    state.invincible = True
    state.invincible_timer = time.time()
    return foods
