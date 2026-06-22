import pygame
import sys

from settings import (
    SCREEN_W, SCREEN_H, FPS, TITLE,
    STARTING_LIVES, SPEED_UP_EVERY, SPEED_INCREMENT,
    DARK_BG, GRID_LINE, WHITE, RED, NEON_GREEN, YELLOW, ORANGE, NEON_BLUE
)
from game.paddle import Paddle
from game.ball   import Ball
from game.brick  import create_bricks


# ─────────────────────────────────────────
#  COLLISION: Ball vs Brick grid
# ─────────────────────────────────────────
def check_brick_collision(ball, bricks):
    ball_rect = ball.get_rect()
    for brick in bricks:
        if not brick.alive:
            continue
        if ball_rect.colliderect(brick.rect):
            destroyed = brick.hit()

            # Bounce direction
            overlap_x = (
                min(ball_rect.right,  brick.rect.right) -
                max(ball_rect.left,   brick.rect.left)
            )
            overlap_y = (
                min(ball_rect.bottom, brick.rect.bottom) -
                max(ball_rect.top,    brick.rect.top)
            )
            if overlap_x < overlap_y:
                ball.vx *= -1
            else:
                ball.vy *= -1

            return destroyed   # True = fully destroyed, False = just hit
    return None                # None  = no collision


# ─────────────────────────────────────────
#  DRAW HELPERS
# ─────────────────────────────────────────
def draw_background(surface):
    surface.fill(DARK_BG)
    for x in range(0, SCREEN_W, 40):
        pygame.draw.line(surface, GRID_LINE, (x, 0), (x, SCREEN_H))
    for y in range(0, SCREEN_H, 40):
        pygame.draw.line(surface, GRID_LINE, (0, y), (SCREEN_W, y))


def draw_hud(surface, score, lives, level_speed, font_big, font_small):
    # Score
    score_txt = font_big.render(f"SCORE  {score:04d}", True, NEON_GREEN)
    surface.blit(score_txt, (20, 14))

    # Lives (heart symbols)
    lives_txt = font_big.render("❤ " * lives, True, RED)
    surface.blit(lives_txt, (SCREEN_W - lives_txt.get_width() - 20, 14))

    # Speed indicator
    spd_txt = font_small.render(f"SPEED  {level_speed:.1f}", True, ORANGE)
    surface.blit(spd_txt, (SCREEN_W // 2 - spd_txt.get_width() // 2, 18))

    # Controls hint
    hint = font_small.render("← → / A D  move   |   SPACE  launch", True, (80, 80, 100))
    surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 24))


def draw_overlay(surface, lines, font_big, font_med):
    """Draw a semi-transparent overlay with multiple text lines."""
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    surface.blit(overlay, (0, 0))

    total_h = len(lines) * 60
    start_y = SCREEN_H // 2 - total_h // 2

    for i, (text, color, big) in enumerate(lines):
        font = font_big if big else font_med
        rendered = font.render(text, True, color)
        x = SCREEN_W // 2 - rendered.get_width() // 2
        y = start_y + i * 60
        surface.blit(rendered, (x, y))


# ─────────────────────────────────────────
#  MAIN GAME CLASS
# ─────────────────────────────────────────
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()

        self.font_big   = pygame.font.SysFont(None, 46, bold=True)
        self.font_med   = pygame.font.SysFont(None, 32)
        self.font_small = pygame.font.SysFont(None, 20)

        self.reset()

    # ── Reset everything ──────────────────
    def reset(self):
        self.paddle       = Paddle()
        self.ball         = Ball(self.paddle.rect)
        self.bricks       = create_bricks()
        self.score        = 0
        self.lives        = STARTING_LIVES
        self.bricks_hit   = 0          # tracks speed-up milestones
        self.state        = "playing"  # playing | lost_life | won | game_over

    # ── Respawn after losing a life ───────
    def respawn(self):
        self.paddle.reset()
        self.ball = Ball(self.paddle.rect)
        self.state = "playing"

    # ── Main loop ─────────────────────────
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    # ── Events ────────────────────────────
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Launch ball
                if event.key == pygame.K_SPACE:
                    if self.state == "playing" and not self.ball.launched:
                        self.ball.launch()
                    elif self.state == "lost_life":
                        self.respawn()

                # Restart after game over / win
                if event.key == pygame.K_r and self.state in ("won", "game_over"):
                    self.reset()

    # ── Update ────────────────────────────
    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        self.paddle.update(keys)
        self.ball.update(self.paddle.rect)
        self.ball.bounce_paddle(self.paddle.rect)

        # Brick collision
        result = check_brick_collision(self.ball, self.bricks)
        if result is True:       # brick destroyed
            self.score      += 10
            self.bricks_hit += 1
            # Speed up every N destroyed bricks
            if self.bricks_hit % SPEED_UP_EVERY == 0:
                self.ball.increase_speed(SPEED_INCREMENT)
        elif result is False:    # brick hit but not destroyed (2-HP brick)
            self.score += 5

        # Win check
        if all(not b.alive for b in self.bricks):
            self.state = "won"
            return

        # Ball out
        if self.ball.is_out():
            self.lives -= 1
            if self.lives <= 0:
                self.state = "game_over"
            else:
                self.state = "lost_life"

    # ── Draw ──────────────────────────────
    def draw(self):
        draw_background(self.screen)

        for brick in self.bricks:
            brick.draw(self.screen)

        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        draw_hud(
            self.screen, self.score, self.lives,
            self.ball.current_speed,
            self.font_big, self.font_small
        )

        # ── Overlays ──
        if self.state == "lost_life":
            draw_overlay(self.screen, [
                (f"❤  {self.lives} {'life' if self.lives == 1 else 'lives'} remaining", YELLOW, True),
                ("Press SPACE to continue", WHITE, False),
            ], self.font_big, self.font_med)

        elif self.state == "won":
            draw_overlay(self.screen, [
                ("🎉  YOU WIN!", NEON_GREEN, True),
                (f"Final Score:  {self.score}", WHITE, False),
                ("Press R to play again", NEON_BLUE, False),
            ], self.font_big, self.font_med)

        elif self.state == "game_over":
            draw_overlay(self.screen, [
                ("💀  GAME OVER", RED, True),
                (f"Final Score:  {self.score}", WHITE, False),
                ("Press R to try again", ORANGE, False),
            ], self.font_big, self.font_med)

        pygame.display.flip()