import pygame
from settings import (
    BRICK_WIDTH,
    BRICK_HEIGHT,
    BRICK_ROWS,
    BRICK_COLS,
    BRICK_PADDING,
    BRICK_OFFSET_TOP,
    WHITE,
)


GRAY = (140, 140, 140)
ROW_CONFIG = [
    ((255, 100, 100), 2),
    ((255, 180, 80), 2),
    ((255, 255, 120), 1),
    ((120, 220, 255), 1),
    ((120, 255, 140), 1),
    ((200, 120, 255), 2),
]


class Brick:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.color, hp = ROW_CONFIG[row % len(ROW_CONFIG)]
        self.max_hp = hp
        self.hp = hp
        self.alive = True

        self.rect = pygame.Rect(
            col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING + 3,
            row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_OFFSET_TOP,
            BRICK_WIDTH,
            BRICK_HEIGHT,
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
        pygame.draw.rect(surface, GRAY, self.rect, 2, border_radius=5)

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


def check_brick_collision(ball, bricks):
    for brick in bricks[:]:
        if ball.rect.colliderect(brick.rect):
            overlap_x = min(ball.rect.right, brick.rect.right) - max(ball.rect.left, brick.rect.left)
            overlap_y = min(ball.rect.bottom, brick.rect.bottom) - max(ball.rect.top, brick.rect.top)

            if overlap_x < overlap_y:
                ball.vx *= -1
            else:
                ball.vy *= -1

            if brick.hit():
                bricks.remove(brick)
                return 10

            return 5

    return None