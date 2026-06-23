import pygame
import random


class PowerUp:
    TYPES = ["expand", "slow", "life"]

    def __init__(self, x, y):
        self.type = random.choice(self.TYPES)

        self.rect = pygame.Rect(
            x,
            y,
            25,
            25
        )

        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        colors = {
            "expand": (0, 255, 0),
            "slow": (0, 0, 255),
            "life": (255, 0, 0)
        }

        pygame.draw.rect(
            screen,
            colors[self.type],
            self.rect
        )