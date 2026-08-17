import pygame
import sys
import time

from config import *
from env_detect import detect_environment, setup_display
from game_state import GameState
from map_manager import MapManager
from save_manager import SaveManager
from snake_logic import *
from ui_render import render_game, render_load_screen

def main():
    env = setup_display()
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    state = GameState()
    map_mgr = MapManager()
    save_mgr = SaveManager()

    map_mgr.generate_map(state.level)

    if not state.snake:
        spawn_pos, safe_dir = find_safe_spawn(map_mgr.obstacles, state.snake, state.foods, map_mgr.wall_mode)
        state.snake = [(spawn_pos[0], spawn_pos[1])]
        state.direction = safe_dir
        state.next_dir = safe_dir

    init_foods(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr)

    if save_mgr.has_save():
        render_load_screen(screen, True)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        result = save_mgr.load_progress(state)
                        if result:
                            obs, foods, wm = result
                            map_mgr.obstacles = obs
                            map_mgr.wall_mode = wm
                            state.foods = foods
                            if not state.snake:
                                spawn_pos, safe_dir = find_safe_spawn(map_mgr.obstacles, state.snake, state.foods, map_mgr.wall_mode)
                                state.snake = [(spawn_pos[0], spawn_pos[1])]
                                state.direction = safe_dir
                                state.next_dir = safe_dir
                            print("Save loaded successfully")
                            waiting = False
                        else:
                            print("Load failed, starting new game")
                            map_mgr.generate_map(state.level)
                            spawn_pos, safe_dir = find_safe_spawn(map_mgr.obstacles, state.snake, state.foods, map_mgr.wall_mode)
                            state.snake = [(spawn_pos[0], spawn_pos[1])]
                            state.direction = safe_dir
                            state.next_dir = safe_dir
                            init_foods(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr)
                            waiting = False
                    elif event.key == pygame.K_n:
                        save_mgr.delete_save()
                        map_mgr.generate_map(state.level)
                        spawn_pos, safe_dir = find_safe_spawn(map_mgr.obstacles, state.snake, state.foods, map_mgr.wall_mode)
                        state.snake = [(spawn_pos[0], spawn_pos[1])]
                        state.direction = safe_dir
                        state.next_dir = safe_dir
                        init_foods(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr)
                        print("New game started")
                        waiting = False
    else:
        map_mgr.generate_map(state.level)
        spawn_pos, safe_dir = find_safe_spawn(map_mgr.obstacles, state.snake, state.foods, map_mgr.wall_mode)
        state.snake = [(spawn_pos[0], spawn_pos[1])]
        state.direction = safe_dir
        state.next_dir = safe_dir
        init_foods(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr)
        print("New game started")

    running = True
    while running:
        current_time = time.time()
        if state.invincible and current_time - state.invincible_timer > INVINCIBLE_DURATION:
            state.invincible = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_mgr.save_progress(state, map_mgr.obstacles, map_mgr.wall_mode, map_mgr.get_food_count(state.level))
                print("Progress saved")
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    save_mgr.save_progress(state, map_mgr.obstacles, map_mgr.wall_mode, map_mgr.get_food_count(state.level))
                    print("Progress saved, exiting")
                    running = False
                elif event.key == pygame.K_r and state.game_over:
                    state.level = 1
                    state.score = 0
                    state.lives = INITIAL_LIVES
                    state.food_count = 0
                    state.game_over = False
                    state.invincible = False
                    map_mgr.generate_map(state.level)
                    spawn_pos, safe_dir = find_safe_spawn(map_mgr.obstacles, state.snake, state.foods, map_mgr.wall_mode)
                    state.snake = [(spawn_pos[0], spawn_pos[1])]
                    state.direction = safe_dir
                    state.next_dir = safe_dir
                    state.input_queue.clear()
                    init_foods(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr)
                    print("Game reset")
                elif event.key == pygame.K_s:
                    if save_mgr.save_progress(state, map_mgr.obstacles, map_mgr.wall_mode, map_mgr.get_food_count(state.level)):
                        print("Progress saved")
                elif not state.game_over and not state.invincible:
                    if event.key == pygame.K_UP and state.direction != (0, GRID_SIZE):
                        if not state.input_queue or state.input_queue[-1] != (0, -GRID_SIZE):
                            state.input_queue.append((0, -GRID_SIZE))
                    elif event.key == pygame.K_DOWN and state.direction != (0, -GRID_SIZE):
                        if not state.input_queue or state.input_queue[-1] != (0, GRID_SIZE):
                            state.input_queue.append((0, GRID_SIZE))
                    elif event.key == pygame.K_LEFT and state.direction != (GRID_SIZE, 0):
                        if not state.input_queue or state.input_queue[-1] != (-GRID_SIZE, 0):
                            state.input_queue.append((-GRID_SIZE, 0))
                    elif event.key == pygame.K_RIGHT and state.direction != (-GRID_SIZE, 0):
                        if not state.input_queue or state.input_queue[-1] != (GRID_SIZE, 0):
                            state.input_queue.append((GRID_SIZE, 0))

        if not state.game_over and not state.invincible:
            if state.input_queue:
                new_dir = state.input_queue[0]
                if (new_dir[0] != -state.direction[0] or new_dir[1] != -state.direction[1]):
                    state.direction = new_dir
                state.input_queue.popleft()

            head = state.snake[0]
            new_head = (head[0] + state.direction[0], head[1] + state.direction[1])

            if map_mgr.is_wall_collision(new_head, map_mgr.wall_mode):
                if not state.invincible:
                    state.lives -= 1
                    if state.lives <= 0:
                        state.game_over = True
                        save_mgr.add_death()
                    else:
                        state.foods = reset_snake_position(state, map_mgr.obstacles, state.foods, map_mgr.wall_mode, map_mgr)
                        print(f"HIT WALL! Lives left: {state.lives}")
                continue

            if not map_mgr.wall_mode:
                if new_head[0] < 0:
                    new_head = ((W_GRID - 1) * GRID_SIZE, new_head[1])
                elif new_head[0] >= W:
                    new_head = (0, new_head[1])
                if new_head[1] < 0:
                    new_head = (new_head[0], (H_GRID - 1) * GRID_SIZE)
                elif new_head[1] >= H - 50:
                    new_head = (new_head[0], 0)

            if map_mgr.is_obstacle(new_head):
                if not state.invincible:
                    state.lives -= 1
                    if state.lives <= 0:
                        state.game_over = True
                        save_mgr.add_death()
                    else:
                        state.foods = reset_snake_position(state, map_mgr.obstacles, state.foods, map_mgr.wall_mode, map_mgr)
                        print(f"HIT OBSTACLE! Lives left: {state.lives}")
                continue

            ate = False
            for food in state.foods[:]:
                if new_head == food:
                    state.foods.remove(food)
                    state.foods.append(spawn_food(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr))
                    state.score += state.level
                    state.food_count += 1
                    ate = True
                    if state.level % 10 == 0:
                        state.level += 1
                        map_mgr.generate_map(state.level)
                        init_foods(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr)
                        print(f"NEW LEVEL! Current level: {state.level} Map: {map_mgr.get_current_name()}")
                    else:
                        state.level += 1
                        if len(state.foods) < map_mgr.get_food_count(state.level):
                            state.foods.append(spawn_food(state.snake, state.foods, map_mgr.obstacles, map_mgr.wall_mode, state.level, map_mgr))
                    break

            if not ate:
                state.snake.pop()
            state.snake.insert(0, new_head)

            if new_head in state.snake[1:]:
                if not state.invincible:
                    state.lives -= 1
                    if state.lives <= 0:
                        state.game_over = True
                        save_mgr.add_death()
                    else:
                        state.foods = reset_snake_position(state, map_mgr.obstacles, state.foods, map_mgr.wall_mode, map_mgr)
                        print(f"HIT SELF! Lives left: {state.lives}")

        render_game(screen, state, map_mgr.obstacles, map_mgr.wall_mode, map_mgr.get_current_name(), save_mgr.death_count, env, map_mgr.get_food_count(state.level))
        clock.tick(5 + state.level * 1.5)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
