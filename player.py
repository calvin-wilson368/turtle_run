import math

import pygame

class Player:
    def __init__(self,width, height, screen):
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen = screen

        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.speed = 1

    def bound_rect(self):
        return pygame.Rect(self.x + self.WIDTH / 2 - self.width / 2, -self.y + self.HEIGHT / 2 - self.height / 2, self.width,
                           self.height)

    def draw(self):
        pygame.draw.rect(self.screen, (0, 255, 0), self.bound_rect(), border_radius=10)
    def update(self, dt):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        speed = max(self.width, self.height) * 6 * dt * self.speed

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx += -speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy += speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += -speed

        distance = math.hypot(dx, dy)
        if distance > 0:
            self.x += dx / distance * speed
            if abs(self.x) + self.width / 2 > self.WIDTH / 2:
                self.x -= dx / distance * speed

            self.y += dy / distance * speed
            if abs(self.y) + self.height / 2 > self.HEIGHT / 2:
                self.y -= dy / distance * speed