# ─────────────────────────────────────────
#  SETTINGS — All constants in one place
# ─────────────────────────────────────────

# Screen
SCREEN_W  = 800
SCREEN_H  = 600
FPS       = 60
TITLE     = "🧱 Brick Breaker — Stage 2"

# Paddle
PADDLE_W      = 110
PADDLE_H      = 14
PADDLE_SPEED  = 7
PADDLE_Y_OFF  = 50      # distance from bottom

# Ball
BALL_RADIUS   = 9
BALL_SPEED    = 5
SPEED_UP_EVERY = 5      # increase speed every N bricks broken
SPEED_INCREMENT = 0.3   # how much to add each time

# Bricks
BRICK_ROWS  = 6
BRICK_COLS  = 10
BRICK_W     = 68
BRICK_H     = 24
BRICK_PAD   = 6
BRICK_TOP   = 60

# Lives
STARTING_LIVES = 3

# Colors
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
GRAY        = (40,  40,  40)
DARK_BG     = (8,   8,   18)
GRID_LINE   = (18,  18,  32)

NEON_BLUE   = (0,   200, 255)
NEON_GREEN  = (0,   255, 150)
YELLOW      = (255, 220, 50)
ORANGE      = (255, 140, 0)
RED         = (255, 60,  60)
PINK        = (255, 80,  180)
PURPLE      = (180, 80,  255)

# Row configs: (color, hp)
# Top rows are harder (2 HP), bottom rows are easier (1 HP)
ROW_CONFIG = [
    (RED,       2),
    (PINK,      2),
    (ORANGE,    2),
    (YELLOW,    1),
    (NEON_GREEN,1),
    (NEON_BLUE, 1),
]