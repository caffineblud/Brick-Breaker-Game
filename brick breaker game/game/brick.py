import pygame
from settings import (
    BRICK_W, BRICK_H, BRICK_PAD, BRICK_TOP,
    BRICK_ROWS, BRICK_COLS,
    ROW_CONFIG, GRAY, WHITE
)


class Brick:
    def __init__(self, row, col):
        self.row   = row
        self.col   = col

        color, hp       = ROW_CONFIG[row % len(ROW_CONFIG)]
        self.color      = color
        self.max_hp     = hp
        self.hp         = hp
        self.alive      = True

        self.rect = pygame.Rect(
            col * (BRICK_W + BRICK_PAD) + BRICK_PAD + 3,
            row * (BRICK_H + BRICK_PAD) + BRICK_TOP,
            BRICK_W,
            BRICK_H,
        )

    def hit(self):
        """Reduce HP; returns True if brick is destroyed."""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def _get_draw_color(self):
        """Darken color when brick has been hit once (HP=1, max=2)."""
        if self.max_hp == 2 and self.hp == 1:
            r, g, b = self.color
            return (max(r - 80, 0), max(g - 80, 0), max(b - 80, 0))
        return self.color

    def draw(self, surface):
        if not self.alive:
            return

        color = self._get_draw_color()
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, GRAY,  self.rect, 2, border_radius=5)

        # Shine strip
        shine = pygame.Rect(
            self.rect.x + 4, self.rect.y + 4,
            self.rect.width - 8, 4
        )
        shine_surf = pygame.Surface((shine.width, shine.height), pygame.SRCALPHA)
        shine_surf.fill((255, 255, 255, 60))
        surface.blit(shine_surf, (shine.x, shine.y))

        # HP indicator dots for 2-HP bricks
        if self.max_hp == 2:
            dot_color = WHITE if self.hp == 2 else (80, 80, 80)
            for i in range(self.max_hp):
                cx = self.rect.right - 10 - i * 12
                cy = self.rect.centery
                pygame.draw.circle(surface, dot_color, (cx, cy), 4)


def create_bricks():
    return [Brick(r, c) for r in range(BRICK_ROWS) for c in range(BRICK_COLS)]