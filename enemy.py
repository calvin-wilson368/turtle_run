import math
import random

import pygame


class Enemy:
    def __init__(self, width, height, color, screen, player, enemies):
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen = screen
        self.player = player
        self.enemies = enemies

        self.width = width
        self.height = height
        self.color = color
        self.reset()

    def bound_rect(self):
        return pygame.Rect(self.x + self.WIDTH/2 - self.width/2, -self.y + self.HEIGHT/2 - self.height/2, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.bound_rect(), border_radius=10)
    def update(self, dt):
        pass
    # def collision(self, dt, dx, dy, distance):
    #     speed = self.speed * dt
    #     adj_dx = dx / distance * speed
    #     adj_dy = dy / distance * speed
    #     pos = self.bound_rect()
    #     for enemy in enemies:
    #         if enemy == self:
    #             continue
    #         if not pygame.Rect(pos.x + adj_dx, pos.y + adj_dy, pos.width, pos.height).colliderect(enemy.bound_rect()):
    #             # adding dx dy does not collide
    #             continue
    #         # elif not pygame.Rect(pos.x, pos.y + adj_dy, pos.width, pos.height).colliderect(enemy.bound_rect()):
    #         #     # adding dy does not collide
    #         #     adj_dx = 0
    #         # elif not pygame.Rect(pos.x + adj_dx, pos.y, pos.width, pos.height).colliderect(enemy.bound_rect()):
    #         #     # adding dx does not collide
    #         #     adj_dy = 0
    #         else:
    #             adj_dx = 0
    #             adj_dy = 0
    #     print(pos, adj_dx, adj_dy)
    #     self.x += adj_dx
    #     self.y += adj_dy
    #     return False
    def collision(self, dt, dx, dy, distance):
        speed = self.speed * dt

        # Normalized direction toward target
        dir_x = dx / distance
        dir_y = dy / distance

        move_x = dir_x * speed
        move_y = dir_y * speed

        pos = self.bound_rect()

        def blocked(test_x, test_y):
            test_rect = pygame.Rect(
                pos.x + test_x,
                pos.y + test_y,
                pos.width,
                pos.height
            )

            for enemy in self.enemies:
                if enemy == self:
                    continue

                if test_rect.colliderect(enemy.bound_rect()):
                    return True

            return False

        # --------------------------------------------------
        # 1. Try moving directly toward the player
        # --------------------------------------------------

        if not blocked(move_x, move_y):
            self.x += move_x
            self.y += move_y
            return False

        # --------------------------------------------------
        # 2. Direct path blocked.
        #    Try moving perpendicular to the player direction.
        # --------------------------------------------------

        # Perpendicular direction #1
        side1_x = -dir_y * speed
        side1_y = dir_x * speed

        # Perpendicular direction #2
        side2_x = dir_y * speed
        side2_y = -dir_x * speed

        side1_blocked = blocked(side1_x, side1_y)
        side2_blocked = blocked(side2_x, side2_y)

        # One side is free
        if not side1_blocked:
            self.x += side1_x
            self.y += side1_y
            return True

        if not side2_blocked:
            self.x += side2_x
            self.y += side2_y
            return True

        # --------------------------------------------------
        # 3. Both sides are blocked.
        #    Try sliding horizontally / vertically.
        # --------------------------------------------------

        if not blocked(move_x, 0):
            self.x += move_x
            return True

        if not blocked(0, move_y):
            self.y += move_y
            return True

        # --------------------------------------------------
        # 4. Completely surrounded.
        #    Push away from nearby enemies.
        # --------------------------------------------------

        push_x = 0
        push_y = 0

        for enemy in self.enemies:
            if enemy == self:
                continue

            other = enemy.bound_rect()

            # Distance between centers
            enemy_dx = self.x - enemy.x
            enemy_dy = self.y - enemy.y

            dist = math.hypot(enemy_dx, enemy_dy)

            # If they are touching/overlapping
            min_dist_x = (self.width + enemy.width) / 2
            min_dist_y = (self.height + enemy.height) / 2

            if abs(enemy_dx) < min_dist_x and abs(enemy_dy) < min_dist_y:

                if dist > 0:
                    push_x += enemy_dx / dist
                    push_y += enemy_dy / dist
                else:
                    # Exact same position -- choose random direction
                    angle = random.random() * math.pi * 2
                    push_x += math.cos(angle)
                    push_y += math.sin(angle)

        push_distance = speed * 2

        push_length = math.hypot(push_x, push_y)

        if push_length > 0:
            push_x /= push_length
            push_y /= push_length

            self.x += push_x * push_distance
            self.y += push_y * push_distance

        return True

    def reset(self):
        while True:
            self.x = random.randint(round(-self.WIDTH / 2 + self.width), round(self.WIDTH / 2 - self.width))
            self.y = random.randint(round(-self.HEIGHT / 2 + self.height), round(self.HEIGHT / 2 - self.height))
            if abs(self.x) + abs(self.y) > self.WIDTH / 4:
                break
        self.speed = 400

class FollowEnemy(Enemy):
    def __init__(self,width, height, screen, player, enemies):
        super().__init__(width, height, "Red", screen, player, enemies)
        self.reset()
    def update(self, dt):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.collision(dt, dx, dy, distance)

class RanEnemy(Enemy):
    def __init__(self, width, height, screen, player, enemies):
        super().__init__(width, height, "Blue", screen, player, enemies)
        self.reset()
    def update(self, dt):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > self.width / 2:
            if self.collision(dt, dx, dy, distance):
                self.target_x = random.randint(-self.WIDTH // 2 + self.width, self.WIDTH // 2 - self.width)
                self.target_y = random.randint(-self.HEIGHT // 2 + self.height, self.HEIGHT // 2 - self.height)
        else:
            self.target_x = random.randint(-self.WIDTH // 2 + self.width, self.WIDTH // 2 - self.width)
            self.target_y = random.randint(-self.HEIGHT // 2 + self.height, self.HEIGHT // 2 - self.height)
    def reset(self):
        super().reset()
        self.target_x = random.randint(-self.WIDTH // 2 + self.width, self.WIDTH // 2 - self.width)
        self.target_y = random.randint(-self.HEIGHT // 2 + self.height, self.HEIGHT // 2 - self.height)

class ExplodeEnemy(RanEnemy):
    def __init__(self, width, height, screen, player, enemies):
        super().__init__(width, height, screen, player, enemies)
        self.color = "Yellow"
    def update(self, dt):
        super().update(dt)
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.hypot(dx, dy)

        if distance < 500:

            return True
        return False