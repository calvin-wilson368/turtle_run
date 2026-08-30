import random

import pygame

class Coin:
    def __init__(self, diameter, screen):
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen = screen

        self.type = random.choice(("Green", "Blue", "Red", "Yellow", "Yellow"))
        self.diameter = 100 if self.type != "Yellow" else 50
        self.reset()
    def bound_rect(self):
        return pygame.Rect(self.x + self.WIDTH/2 - self.diameter/2, -self.y + self.HEIGHT/2 - self.diameter/2, self.diameter, self.diameter)

    def draw(self):
        pygame.draw.circle(self.screen, self.type, (round(self.x + self.WIDTH / 2), round(-self.y + self.HEIGHT / 2)), self.diameter / 2)
    def reset(self):
        self.x = random.randint(-self.WIDTH // 2 + self.diameter, self.WIDTH // 2 - self.diameter)
        self.y = random.randint(-self.HEIGHT // 2 + self.diameter, self.HEIGHT // 2 - self.diameter)