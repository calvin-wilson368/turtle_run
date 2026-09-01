import math
import random
import time
import sys
import json
import os

import pygame

import player as plr
import enemy as en
import coin

# High score file management
HIGHSCORE_FILE = "highscore.json"


def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("highscore", 0)
        except:
            return 0
    return 0


def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"highscore": score}, f)
    except:
        pass


if True:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 1000

    running = True
    life = True

    score = 0
    high_score = load_highscore()
    font = pygame.font.Font(None, 100)
    score_text = font.render(f"Score: 0", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 235, 80))

    gameOverFont = pygame.font.Font(None, 500)

    inventory = {"amo": 0, "gruhnaids": 0}

    immortal = False

    player = plr.Player(int(WIDTH / 20), int(WIDTH / 20), screen)
    # Put player in its own group or handle individually
    player_group = pygame.sprite.GroupSingle(player)

    spawn_timer = 0
    spawn_time = 25

    enemy_args = (screen, player)

    enemies = pygame.sprite.Group()
    for _ in range(2):
        enemies.add(en.FollowEnemy(100, 100, *enemy_args))
        enemies.add(en.RanEnemy(100, 100, *enemy_args))

    coins = pygame.sprite.Group()
    for _ in range(5):
        coins.add(coin.Coin(100, screen))



def coordinates(target):
    font = pygame.font.Font(None, 100)
    lines = [f"x: {target.x:.0f}", f"y: {target.y:.0f}"]

    for i, line in enumerate(lines):
        text = font.render(line, True, "white")
        text_rect = text.get_rect(topright=(WIDTH - 40, 220 + i * 100))
        screen.blit(text, text_rect)
    pygame.display.flip()


def fps():
    text = font.render(f"FPS: {clock.get_fps():.0f}", True, "white")
    text_rect = text.get_rect(topright=(WIDTH - 40, 140))
    screen.blit(text, text_rect)


def draw():
    screen.fill((0, 0, 20))

    coins.draw(screen)
    player_group.draw(screen)
    enemies.draw(screen)

    screen.blit(score_text, (40, 40))
    screen.blit(high_score_text, (40, 140))


    text = font.render(f"{math.ceil(spawn_time - spawn_timer)}", True, "white")
    text_rect = text.get_rect(topright=(WIDTH - 40, 40))
    screen.blit(text, text_rect)

    fps()


def update(dt):
    global life, enemies, spawn_timer, spawn_time, score, score_text, high_score, high_score_text

    # Updates player movement coordinates and its tracking rect
    player_group.update(dt)

    if spawn_timer > spawn_time:
        enemies.add(en.FollowEnemy(100, 100, *enemy_args))
        enemies.add(en.RanEnemy(100, 100, *enemy_args))

        spawn_time *= 0.875
        spawn_timer = 0

    enemies.update(dt)

    for enemy in enemies:
        enemy.speed += 3 * dt

    # Check damage tracking via built-in sprite collision checking
    if not immortal:
        if pygame.sprite.spritecollideany(player, enemies):
            life = False

    # Check token pickups via built-in sprite collision group filters
    collected_coins = pygame.sprite.spritecollide(player, coins, True)

    for c in collected_coins:
        if c.type == "Yellow":
            score += 1
            score_text = font.render(f"Score: {score}", True, "white")
            if score > high_score:
                high_score = score
                high_score_text = font.render(f"High Score: {high_score}", True, (255, 235, 80))
        elif c.type == "Blue":
            inventory[random.choice(list(inventory.keys()))] += 1

    if random.random() < dt / 5:
        coins.add(coin.Coin(100, screen))


def game_loop():
    global life, spawn_timer

    while life:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        dt = clock.tick(FPS) / 1000
        spawn_timer += dt
        update(dt)
        if not life:
            break
        draw()
        pygame.display.flip()


while True:
    game_loop()

    # Save high score when game ends
    save_highscore(high_score)

    text = gameOverFont.render("GAME OVER!", True, "white")
    text_rect = text.get_rect(center=screen.get_rect().center)

    screen.blit(text, text_rect)
    pygame.display.flip()

    while not pygame.key.get_pressed()[pygame.K_SPACE]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

    life = True

    score = 0
    score_text = font.render(f"Score: 0", True, (255, 255, 255))

    inventory = {"amo": 0, "gruhnaids": 0}

    player.x = 0
    player.y = 0
    player.update_rect_position()

    spawn_timer = 0
    spawn_time = 25

    # Clear and recreate sprite groups cleanly on reset
    enemies.empty()
    for _ in range(2):
        enemies.add(en.FollowEnemy(100, 100, *enemy_args))
        enemies.add(en.RanEnemy(100, 100, *enemy_args))

    coins.empty()
    for _ in range(5):
        coins.add(coin.Coin(100, screen))

pygame.quit()