import pygame
from settings import SCREEN_W, SCREEN_H, BALL_RADIUS, BALL_SPEED, WHITE


class Ball:
    def __init__(self, paddle_rect):
        self.radius   = BALL_RADIUS
        self.base_speed = BALL_SPEED
        self.current_speed = BALL_SPEED
        self.reset(paddle_rect)

    def reset(self, paddle_rect):
        """Place ball on top of paddle, wait for launch."""
        self.x        = float(paddle_rect.centerx)
        self.y        = float(paddle_rect.top - self.radius - 2)
        self.vx       = self.current_speed
        self.vy       = -self.current_speed
        self.launched = False

    def launch(self):
        self.launched = True

    def increase_speed(self, increment):
        """Gradually speed up the ball."""
        self.current_speed += increment
        # Keep direction, scale velocity to new speed
        import math
        mag = math.hypot(self.vx, self.vy)
        if mag > 0:
            self.vx = (self.vx / mag) * self.current_speed
            self.vy = (self.vy / mag) * self.current_speed

    def update(self, paddle_rect):
        if not self.launched:
            self.x = float(paddle_rect.centerx)
            self.y = float(paddle_rect.top - self.radius - 2)
            return

        self.x += self.vx
        self.y += self.vy

        # Left / right walls
        if self.x - self.radius <= 0:
            self.x  = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= SCREEN_W:
            self.x  = SCREEN_W - self.radius
            self.vx = -abs(self.vx)

        # Top wall
        if self.y - self.radius <= 0:
            self.y  = self.radius
            self.vy = abs(self.vy)

    def bounce_paddle(self, paddle_rect):
        """Reflect off paddle; angle depends on hit position."""
        if self.vy > 0 and self.get_rect().colliderect(paddle_rect):
            self.vy = -abs(self.vy)
            offset  = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
            self.vx = offset * self.current_speed * 1.2

    def get_rect(self):
        return pygame.Rect(
            int(self.x) - self.radius,
            int(self.y) - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def is_out(self):
        """Returns True when ball falls below the screen."""
        return self.y - self.radius > SCREEN_H

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)
        # Tiny shine dot
        pygame.draw.circle(
            surface, (200, 240, 255),
            (int(self.x) - 3, int(self.y) - 3), 3
        )