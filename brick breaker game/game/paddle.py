import pygame
from settings import (
    SCREEN_W, SCREEN_H,
    PADDLE_W, PADDLE_H, PADDLE_SPEED, PADDLE_Y_OFF,
    NEON_BLUE, WHITE
)


class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(
            (SCREEN_W - PADDLE_W) // 2,
            SCREEN_H - PADDLE_Y_OFF,
            PADDLE_W,
            PADDLE_H,
        )
        self.color = NEON_BLUE

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PADDLE_SPEED
        # Clamp inside screen
        self.rect.x = max(0, min(SCREEN_W - PADDLE_W, self.rect.x))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=7)
        # Glowing highlight stripe
        highlight = pygame.Rect(
            self.rect.x + 6, self.rect.y + 3,
            self.rect.width - 12, 4
        )
        pygame.draw.rect(surface, WHITE, highlight, border_radius=3)

    def reset(self):
        """Re-center paddle (called on life loss)."""
        self.rect.x = (SCREEN_W - PADDLE_W) // 2