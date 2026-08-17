import pygame
import os
import time
from config import *

def get_font(size):
    paths = [
        "/system/fonts/NotoSansCJK-Regular.ttc",
        "/system/fonts/DroidSansFallback.ttf",
        "/data/data/com.termux/files/home/NotoSansCJK-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return pygame.font.Font(p, size)
            except:
                continue
    return pygame.font.Font(None, size)

def render_game(screen, state, obstacles, wall_mode, map_name, death_count, env, food_target):
    font = get_font(22)
    font_big = get_font(40)
    font_small = get_font(18)

    screen.fill(BLACK)

    for x in range(0, W, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, H - 50))
    for y in range(0, H - 50, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (W, y))

    for obs in obstacles:
        color = ORANGE if wall_mode else BLUE
        pygame.draw.rect(screen, color, (obs[0], obs[1], GRID_SIZE, GRID_SIZE))
        if wall_mode:
            pygame.draw.rect(screen, (200,100,0), (obs[0]+2, obs[1]+2, GRID_SIZE-4, GRID_SIZE-4))
        else:
            pygame.draw.rect(screen, DARK_BLUE, (obs[0]+2, obs[1]+2, GRID_SIZE-4, GRID_SIZE-4))

    for food in state.foods:
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, (200,0,0), (food[0]+2, food[1]+2, GRID_SIZE-4, GRID_SIZE-4))

    for i, seg in enumerate(state.snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (seg[0], seg[1], GRID_SIZE, GRID_SIZE))
        if i == 0:
            pygame.draw.rect(screen, (0, 150, 0), (seg[0]+2, seg[1]+2, GRID_SIZE-4, GRID_SIZE-4), 1)

    pygame.draw.line(screen, GRAY, (0, H - 50), (W, H - 50), 2)

    lives_str = "O" * state.lives + "o" * (state.max_lives - state.lives)
    wall_indicator = " [W]" if wall_mode else " [P]"
    hud = f"Level:{state.level} {map_name}{wall_indicator}  Score:{state.score}  Lives:{lives_str}  Food:{len(state.foods)}/{food_target}"
    screen.blit(font.render(hud, True, WHITE), (10, 10))

    death_text = f"Deaths: {death_count}"
    screen.blit(font.render(death_text, True, YELLOW), (10, H - 40))

    tip_text = "S=Save | Q=Quit | R=Reset"
    screen.blit(font_small.render(tip_text, True, GRAY), (W - 180, H - 40))

    env_text = f"Env: {env}"
    screen.blit(font_small.render(env_text, True, GRAY), (W - 100, 10))

    if state.invincible:
        remaining = max(0, INVINCIBLE_DURATION - (time.time() - state.invincible_timer))
        inv_text = font_big.render(f"Shield {remaining:.1f}s", True, (0, 255, 255))
        screen.blit(inv_text, (W//2 - 80, H//2 - 40))

    if state.game_over:
        screen.blit(font_big.render("WHY CONTINUE?", True, RED), (W//2-140, H//2-40))

    pygame.display.flip()

def render_load_screen(screen, has_save):
    font = get_font(22)
    font_big = get_font(40)
    font_small = get_font(18)

    screen.fill(BLACK)
    title = font_big.render("Save Manager", True, WHITE)
    screen.blit(title, (W//2 - title.get_width()//2, 150))
    msg1 = font.render("Press Y to load save", True, GREEN)
    screen.blit(msg1, (W//2 - msg1.get_width()//2, 250))
    msg2 = font.render("Press N to new game", True, RED)
    screen.blit(msg2, (W//2 - msg2.get_width()//2, 300))
    if has_save:
        info = font_small.render("Save file detected", True, YELLOW)
    else:
        info = font_small.render("No save file found", True, GRAY)
    screen.blit(info, (W//2 - info.get_width()//2, 360))
    pygame.display.flip()
