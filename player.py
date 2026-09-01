import math

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, screen):
        super().__init__()

        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen = screen

        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.speed = 1

        # 2. Create the visual surface for the sprite
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Draw the rounded green rectangle directly onto this surface once
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, self.width, self.height), border_radius=10)

        # 3. Create the required rect attribute using your custom centering math
        self.rect = self.image.get_rect()
        self.update_rect_position()

    def update_rect_position(self):
        """Helper to sync Pygame's rect with your custom central coordinate system."""
        self.rect.x = int(self.x + self.WIDTH / 2 - self.width / 2)
        self.rect.y = int(-self.y + self.HEIGHT / 2 - self.height / 2)

    def update(self, dt):
        """Handles movement and automatically updates the sprite's screen position."""
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
            # Horizontal movement & screen bounding
            self.x += dx / distance * speed
            if abs(self.x) + self.width / 2 > self.WIDTH / 2:
                self.x -= dx / distance * speed

            # Vertical movement & screen bounding
            self.y += dy / distance * speed
            if abs(self.y) + self.height / 2 > self.HEIGHT / 2:
                self.y -= dy / distance * speed

        # Keep the drawing rect synchronized with the new x and y values
        self.update_rect_position()
