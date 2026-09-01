effects = []
GreenEffectList = ("p speed 1", "e slow 1", "p small 1", "e small 1")
BlueEffectList = ("p speed 2", "e slow 2", "p small 2", "e small 2", "p slow 2", "e speed 2", "p big 2", "e big 2",
                  "e reset_speed 1", "p immortal 1", "p immortal 2")
RedEffectList = ("p slow 1", "e speed 1", "p big 1", "e big 1")

immortal = False

for i, (effect, _) in enumerate(effects):
    target, name, strength = effect.split(" ")
    target_name = "Player" if target == "p" else "Enemy"
    effect_name = name.replace("_", " ").capitalize()
    effect_text = font.render(f"{target_name}: {effect_name} {strength}", True, "white")
    text_rect = effect_text.get_rect(topleft=(40, 200 + i * 100))
    screen.blit(effect_text, text_rect)

"""elif c.type == "Green":
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


for effect, _ in effects:
    effect_update(effect, undo=True)