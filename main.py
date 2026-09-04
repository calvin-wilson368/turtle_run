import pygame
import sys
import json
import os

import math
import random
import hashlib

import player as plr
import enemy as en
import coin

import funcs



# File management
HIGHSCORE_FILE = "highscore.json"
USERS_FILE = "users.json"

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


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_user(username):
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                data = json.load(f)
                return next((u for u in data if u.get("username") == username), False)
        except:
            return False
    return False

def save_user(username, password):
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []  # Fallback if file was corrupted
    else:
        data = []

    data.append({"username": username, "password": hash_password(password), "data": 1})

    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


"""
if (username := input("Username: ")) and (password := input("Password: ")):
    user = load_user(username)
    if not user:
        print("Incorrect username or password")
        sys.exit()
        save_user(username, password)
    else:
         while True:
             if hash_password(password) == user["password"]:
                break
             print("Incorrect password")
             password = input("Password: ")"""


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

    inventory = {"amo": 0, "grenades": 0}

    immortal = False

    player = plr.Player(int(WIDTH / 20), int(WIDTH / 20), screen)

    player_group = pygame.sprite.GroupSingle(player)

    spawn_timer = 0
    spawn_time = 25

    enemies = pygame.sprite.Group()
    for _ in range(2):
        enemies.add(en.FollowEnemy(100, 100))
        enemies.add(en.RanEnemy(100, 100))

    coins = pygame.sprite.Group()
    for _ in range(5):
        coins.add(coin.Coin(100))



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

    text = font.render(f"Amo: {inventory["amo"]}", True, "white")
    text_rect = text.get_rect(bottomleft=(WIDTH / 2 - 400, HEIGHT - 40))
    screen.blit(text, text_rect)

    text = font.render(f"Grenades: {inventory['grenades']}", True, "white")
    text_rect = text.get_rect(bottomright=(WIDTH / 2 + 400, HEIGHT - 40))
    screen.blit(text, text_rect)

    funcs.fps()


def update(dt):
    global life, enemies, spawn_timer, spawn_time, score, score_text, high_score, high_score_text

    # Updates player movement coordinates and its tracking rect
    player_group.update(dt)

    if spawn_timer > spawn_time:
        enemies.add(en.FollowEnemy(100, 100))
        enemies.add(en.RanEnemy(100, 100))

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
            if random.randint(1, 3) == 1:
                inventory["grenades"] += 1
            else:
                inventory["amo"] += random.randint(1, 5)

    if random.random() < dt / 5:
        coins.add(coin.Coin(100))


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
                if event.key == pygame.K_p:
                    while pygame.key.get_pressed()[pygame.K_p]:
                        pass
                    while not pygame.key.get_pressed()[pygame.K_p]:
                        pass

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

    inventory = {"amo": 0, "grenades": 0}

    player.x = 0
    player.y = 0
    player.update_rect_position()

    spawn_timer = 0
    spawn_time = 25

    # Clear and recreate sprite groups cleanly on reset
    enemies.empty()
    for _ in range(2):
        enemies.add(en.FollowEnemy(100, 100))
        enemies.add(en.RanEnemy(100, 100))

    coins.empty()
    for _ in range(5):
        coins.add(coin.Coin(100))

pygame.quit()