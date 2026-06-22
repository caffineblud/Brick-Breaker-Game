import math
import pygame
from settings import WIDTH, HEIGHT, BALL_RADIUS, BALL_SPEED, WHITE


class Ball:
    def __init__(self, paddle_rect):
        self.radius = BALL_RADIUS
        self.base_speed = BALL_SPEED
        self.current_speed = BALL_SPEED
        self.launched = False
        self.reset(paddle_rect)

    def reset(self, paddle_rect):
        """Place ball on top of paddle, wait for launch."""
        self.x = float(paddle_rect.centerx)
        self.y = float(paddle_rect.top - self.radius - 2)
        self.vx = self.current_speed
        self.vy = -self.current_speed
        self.launched = False

    def launch(self):
        self.launched = True

    def increase_speed(self, increment):
        """Gradually speed up the ball."""
        self.current_speed += increment
        mag = math.hypot(self.vx, self.vy)
        if mag > 0:
            self.vx = (self.vx / mag) * self.current_speed
            self.vy = (self.vy / mag) * self.current_speed

    def move(self, paddle_rect):
        if not self.launched:
            self.x = float(paddle_rect.centerx)
            self.y = float(paddle_rect.top - self.radius - 2)
            return

        self.x += self.vx
        self.y += self.vy

        # Left / right walls
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -abs(self.vx)

        # Top wall
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = abs(self.vy)

    update = move

    def bounce_paddle(self, paddle_rect):
        """Reflect off paddle; angle depends on hit position."""
        if self.vy > 0 and self.rect.colliderect(paddle_rect):
            self.vy = -abs(self.vy)
            offset = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
            self.vx = offset * self.current_speed * 1.2

    @property
    def rectify(self):
        return pygame.Rect(
            int(self.x) - self.radius,
            int(self.y) - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    @property
    def rect(self):
        return self.rectify

    def is_out(self):
        """Returns True when ball falls below the screen."""
        return self.y - self.radius > HEIGHT

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)
        # Tiny shine dot
        pygame.draw.circle(
            surface, (200, 240, 255),
            (int(self.x) - 3, int(self.y) - 3), 3
        )