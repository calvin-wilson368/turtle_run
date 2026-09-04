import math
import random

import pygame



class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()

        self.width = width
        self.height = height
        self.color = color

        # Pre-render the shape onto a transparent sprite canvas
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color(self.color), (0, 0, self.width, self.height), border_radius=10)
        self.rect = self.image.get_rect()

        self.x = 0
        self.y = 0
        self.speed = 400
        self.reset()

    def update_rect_position(self):
        from main import WIDTH, HEIGHT
        """Syncs the display box with engine variables exactly once per frame."""
        self.rect.x = int(self.x + WIDTH / 2 - self.width / 2)
        self.rect.y = int(-self.y + HEIGHT / 2 - self.height / 2)

    def collision(self, dt, dx, dy, distance):
        from main import WIDTH, HEIGHT
        speed = self.speed * dt
        dir_x, dir_y = dx / distance, dy / distance
        move_x, move_y = dir_x * speed, dir_y * speed

        # Extract individual sprites from whatever groups this enemy belongs to
        all_enemies = []
        if self.groups():
            for g in self.groups():
                all_enemies.extend(g.sprites())
        # Remove duplicates
        all_enemies = list(set(all_enemies))

        w_half, h_half = self.width / 2, self.height / 2
        s_width, s_height = self.width, self.height
        w_center, h_center = WIDTH / 2, HEIGHT / 2

        def blocked(test_x, test_y):
            test_rect = pygame.Rect(
                int(self.x + test_x + w_center - w_half),
                int(-(self.y + test_y) + h_center - h_half),
                s_width,
                s_height
            )
            for enemy in all_enemies:
                if enemy is self:
                    continue
                if test_rect.colliderect(enemy.rect):
                    return True
            return False

        # 1. Standard directional advance
        if not blocked(move_x, move_y):
            self.x += move_x
            self.y += move_y
            return False

        # 2. Left and Right flanking routes
        side1_x, side1_y = -dir_y * speed, dir_x * speed
        side2_x, side2_y = dir_y * speed, -dir_x * speed

        if not blocked(side1_x, side1_y):
            self.x += side1_x
            self.y += side1_y
            return True
        if not blocked(side2_x, side2_y):
            self.x += side2_x
            self.y += side2_y
            return True

        # 3. Horizontal and Vertical sliding
        if not blocked(move_x, 0):
            self.x += move_x
            return True
        if not blocked(0, move_y):
            self.y += move_y
            return True

        # 4. Crowd congestion separation
        push_x, push_y = 0, 0
        for enemy in all_enemies:
            if enemy is self:
                continue
            enemy_dx = self.x - enemy.x
            enemy_dy = self.y - enemy.y
            dist = math.hypot(enemy_dx, enemy_dy)

            if abs(enemy_dx) < (s_width + enemy.width) / 2 and abs(enemy_dy) < (s_height + enemy.height) / 2:
                if dist > 0:
                    push_x += enemy_dx / dist
                    push_y += enemy_dy / dist

        push_length = math.hypot(push_x, push_y)
        if push_length > 0:
            push_distance = speed * 2
            self.x += (push_x / push_length) * push_distance
            self.y += (push_y / push_length) * push_distance

        return True

    def reset(self):
        from main import WIDTH, HEIGHT, player
        while True:
            self.x = random.randint(round(-WIDTH / 2 + self.width), round(WIDTH / 2 - self.width))
            self.y = random.randint(round(-HEIGHT / 2 + self.height), round(HEIGHT / 2 - self.height))
            if math.hypot(self.x - player.x, self.y - player.y) > WIDTH / 4:
                break
        self.update_rect_position()


class FollowEnemy(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "Red")

    def update(self, dt):
        from main import player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.collision(dt, dx, dy, distance)
        self.update_rect_position()


class RanEnemy(Enemy):
    def __init__(self, width, height, color="Blue"):
        super().__init__(width, height, color)

    def update(self, dt):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > self.width / 2:
            if self.collision(dt, dx, dy, distance):
                self.get_new_target()
        else:
            self.get_new_target()
        self.update_rect_position()

    def get_new_target(self):
        from main import WIDTH, HEIGHT
        self.target_x = random.randint(-WIDTH // 2 + self.width, WIDTH // 2 - self.width)
        self.target_y = random.randint(-HEIGHT // 2 + self.height, HEIGHT // 2 - self.height)

    def reset(self):
        super().reset()
        self.get_new_target()


class ExplodeEnemy(RanEnemy):
    def __init__(self, width, height, screen, player):
        super().__init__(width, height, color="Yellow")

    def update(self, dt):
        from main import player
        super().update(dt)
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance < 500:
            self.kill()
            return True
        return False
