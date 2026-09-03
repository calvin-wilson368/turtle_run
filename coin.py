import random

import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, diameter, screen):
        # 1. Initialize the parent Sprite class
        super().__init__()

        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen = screen

        self.type = random.choice(("Blue", "Yellow", "Yellow", "Yellow"))

        # Keep diameter size matching your design parameters
        self.diameter = 100 if self.type != "Yellow" else 50

        # 2. Create the graphic asset surface
        self.image = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)

        # Render a centered circle onto the local surface using Pygame's string matching color rules
        pygame.draw.circle(
            self.image,
            pygame.Color(self.type),
            (self.diameter / 2, self.diameter / 2),
            self.diameter / 2
        )

        # 3. Formulate the required engine drawing box tracker
        self.rect = self.image.get_rect()

        self.x = 0
        self.y = 0
        self.reset()

    def update_rect_position(self):
        """Helper to accurately sync screen rect mapping based on custom coordinates."""
        self.rect.x = int(self.x + self.WIDTH / 2 - self.diameter / 2)
        self.rect.y = int(-self.y + self.HEIGHT / 2 - self.diameter / 2)

    def reset(self):
        """Randomizes position and automatically updates rect coordinates."""
        self.x = random.randint(-self.WIDTH // 2 + self.diameter, self.WIDTH // 2 - self.diameter)
        self.y = random.randint(-self.HEIGHT // 2 + self.diameter, self.HEIGHT // 2 - self.diameter)
        self.update_rect_position()
