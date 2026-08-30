import math
import random
import time

import pygame

import player as plr
import enemy as en
import coin

if True:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 240

    running = True
    life = True

    score = 0
    font = pygame.font.Font(None, 100)
    score_text = font.render(f"Score: 0", True, (255, 255, 255))

    gameOverFont = pygame.font.Font(None, 500)

    effects = []
    GreenEffectList = ("p speed 1", "e slow 1", "p small 1", "e small 1")
    BlueEffectList = ("p speed 2", "e slow 2", "p small 2", "e small 2", "p slow 2", "e speed 2", "p big 2", "e big 2", "e reset_speed 1", "p immortal 1", "p immortal 2")
    RedEffectList = ("p slow 1", "e speed 1", "p big 1", "e big 1")

    immortal = False

    player = plr.Player(int(WIDTH/20), int(WIDTH/20), screen)

    spawn_timer = 0
    spawn_level = 1

    enemy_args = (screen, player, [])
    enemies = [en.FollowEnemy(100, 100, *enemy_args) for _ in range(2)] + [en.RanEnemy(100, 100, *enemy_args) for _ in range(2)]
    for enemy in enemies:
        enemy.enemies = enemies

    coins = [coin.Coin(100, screen) for _ in range(10)]


def coordinates(target):
    font = pygame.font.Font(None, 100)
    lines = [f"x: {target.x:.0f}", f"y: {target.y:.0f}"]

    for i, line in enumerate(lines):
        text = font.render(line, True, "white")
        text_rect = text.get_rect(topleft=(20, 20 + i * 100))
        screen.blit(text, text_rect)
    pygame.display.flip()


def effect_update(effect, undo=False):
    target_type, effect_type, strength_text = effect.split(" ")
    strength = int(strength_text)
    multiplier = 1 + strength * 0.5

    def effect_check(target):
        match effect_type:
            case "speed":
                target.speed *= 1 / multiplier if undo else multiplier
            case "slow":
                target.speed *= multiplier if undo else 1 / multiplier

            case "small":
                target.width *= strength + 1 if undo else 1 / (strength + 1)
                target.height *= strength + 1 if undo else 1 / (strength + 1)
                target.speed /= strength + 1 if undo else 1 / (strength + 1)

                while abs(target.x) + target.width / 2 > WIDTH / 2:
                    target.x -= target.x / abs(target.x)

                while abs(target.y) + target.height / 2 > HEIGHT / 2:
                    target.y -= target.y / abs(target.y)
            case "big":
                target.width *= 1 / multiplier if undo else multiplier
                target.height *= 1 / multiplier if undo else multiplier
                target.speed /= 1 / multiplier if undo else multiplier

                while abs(target.x) + target.width / 2 > WIDTH / 2:
                    target.x -= target.x / abs(target.x)

                while abs(target.y) + target.height / 2 > HEIGHT / 2:
                    target.y -= target.y / abs(target.y)

            case "reset_speed":
                if not undo and type(target) == plr.Player:
                    target.speed = 1
                elif type(target) == en.Enemy:
                    target.speed = 400
            case "immortal":
                if type(target) == plr.Player:
                    global immortal
                    immortal = True
                    if undo:
                        immortal = False
                    elif strength > 1:
                        for enemy in enemies:
                            enemy.speed = -enemy.speed

    if target_type == "e":
        for enemy in enemies:
            effect_check(enemy)
    elif target_type == "p":
        effect_check(player)

def check_effect():
    for effect_type, effect_time in effects[:]:
        if time.time() > effect_time + 5:
            effects.remove((effect_type, effect_time))
            effect_update(effect_type, undo=True)

def draw():
    screen.fill((0, 0, 20))
    for c in coins:
        c.draw()
    player.draw()
    for enemy in enemies:
        enemy.draw()

    screen.blit(score_text, (20, 20))
    font = pygame.font.Font(None, 100)

    for i, (effect, _) in enumerate(effects):
        target, name, strength = effect.split(" ")
        target_name = "Player" if target == "p" else "Enemy"
        effect_name = name.replace("_", " ").capitalize()
        effect_text = font.render(f"{target_name}: {effect_name} {strength}", True, "white")
        text_rect = effect_text.get_rect(topleft=(20, 200 + i * 100))
        screen.blit(effect_text, text_rect)
    text = font.render(f"{math.ceil(10 * spawn_level - spawn_timer)}", True, "white")
    text_rect = text.get_rect(topright=(WIDTH-40, 40))
    screen.blit(text, text_rect)

    #coordinates(player)

def update(dt):
    global life, enemies, spawn_level

    check_effect()

    player.update(dt)

    if spawn_timer > 10 * spawn_level:
        spawn_count = int(2 ** (spawn_level * 0.5))

        for _ in range(spawn_count):
            enemies.append(en.FollowEnemy(100, 100, *enemy_args))
            enemies.append(en.RanEnemy(100, 100, *enemy_args))

        for enemy in enemies:
            enemy.enemies = enemies

        spawn_level += 1

    for enemy in enemies:
        enemy.update(dt)
        enemy.speed += 5 * dt

        if player.bound_rect().colliderect(enemy.bound_rect()) and immortal == False:
            life = False

    global score, score_text
    collected_coins = []
    for c in coins:
        if player.bound_rect().colliderect(c.bound_rect()):
            collected_coins.append(c)
            if c.type == "Yellow":
                score += 1
                score_text = font.render(f"Score: {score}", True, "white")
            """
            elif c.type == "Green":
                effect = random.choice(GreenEffectList)
                effects.append((effect, time.time()))
                effect_update(effect)
            elif c.type == "Blue":
                effect = random.choice(BlueEffectList)
                effects.append((effect, time.time()))
                effect_update(effect)
            elif c.type == "Red":
                effect = random.choice(RedEffectList)
                effects.append((effect, time.time()))
                effect_update(effect)"""

    for c in collected_coins:
        coins.remove(c)
    if random.random() < dt/5:
        coins.append(coin.Coin(100, screen))

def game_loop():
    global life, spawn_timer

    while life:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
        spawn_timer += dt
        draw()
        update(dt)


while True:
    game_loop()

    text = gameOverFont.render("GAME OVER!", True, "white")
    text_rect = text.get_rect(center=screen.get_rect().center)

    screen.blit(text, text_rect)
    pygame.display.flip()

    while not pygame.key.get_pressed()[pygame.K_SPACE]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        clock.tick(FPS)


    life = True

    score = 0
    score_text = font.render(f"Score: 0", True, (255, 255, 255))

    player.x = 0
    player.y = 0

    immortal = False

    for effect, _ in effects:
        effect_update(effect, undo=True)

    spawn_timer = 0
    spawn_level = 1

    enemies = ([en.FollowEnemy(100, 100, *enemy_args) for _ in range(2)] +
               [en.RanEnemy(100, 100, *enemy_args) for _ in range(2)])

    for enemy in enemies:
        enemy.enemies = enemies

    coins = [coin.Coin(100, screen) for _ in range(10)]

pygame.quit()