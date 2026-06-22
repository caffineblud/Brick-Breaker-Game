import pygame
from settings import (
    WIDTH,
    HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    WHITE,
)


NEON_BLUE = (0, 255, 255)
PADDLE_Y_OFFSET = 40


class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(
            (WIDTH - PADDLE_WIDTH) // 2,
            HEIGHT - PADDLE_Y_OFFSET,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )
        self.color = NEON_BLUE

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PADDLE_SPEED

        # Clamp inside screen
        self.rect.x = max(0, min(WIDTH - PADDLE_WIDTH, self.rect.x))

    update = move

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
        self.rect.x = (WIDTH - PADDLE_WIDTH) // 2