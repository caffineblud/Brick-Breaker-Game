# 🧱 Brick Breaker Game

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-22c55e?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.5-FF8C00?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square)

> A classic brick-breaker rebuilt in Python and pygame — neon dark-theme, 2-HP brick system, angle physics, particle engine, balanced power-ups, and a combo multiplier system that rewards continuous brick-breaking streaks.

---

## 📸 Preview

<p align="center">
  <img src="screenshots/V1.0.png" alt="Brick Breaker Gameplay" width="800"/>
</p>

---

## 🆕 What's New in V1.5

> V1.5 is the **scoring depth update** — a combo multiplier system rewards streaks, and a long-standing slow power-up bug is finally fixed at the root.

| # | Feature | Details |
|---|---|---|
| 🔥 | **Combo System** | Consecutive brick hits within the time window build a streak counter |
| ✖️ | **Score Multiplier** | Score scales as `points × combo` — breaking 3 bricks fast gives 3× score |
| ⏱️ | **Combo Reset Window** | `COMBO_RESET_TIME` in `settings.py` controls how long the streak stays alive |
| 📊 | **Live Combo HUD** | Active combo displayed as `COMBO x3` in real time during play |
| 💀 | **Ball-Out Combo Reset** | `self.combo = 0` on ball falling — losing a life breaks your streak |
| 🐛 | **Slow Power-Up Fix** | Restored velocity directly (`vx` / `vy`) instead of calling `ball.reset()` — ball no longer teleports to paddle on expiry |

---

## 📋 Full Version History

| Version | Theme | Highlights |
|---|---|---|
| **V1.0** | Base Game | 2-HP bricks, speed scaling, angle physics, neon UI, state machine |
| **V1.1** | Sound System | `pygame.mixer` integration, 4 `.wav` files |
| **V1.2** | Visual Polish | Particle engine — ball trail, paddle sparks, brick explosions + constants refactor |
| **V1.3** | Gameplay Expansion | Modular `powerup.py`, 3 power-up types, falling collectibles, color-coded rendering |
| **V1.4** | Gameplay Optimization | Timed effects, drop balancing, stack control, HUD indicators, crash fix |
| **V1.5** | Scoring Depth | Combo multiplier, streak HUD, inactivity reset, ball-out reset, slow fix |

---

## 🔥 Combo & Multiplier System

### How It Works

```
Brick destroyed
    │
    ├── Check pygame.time.get_ticks()
    │       │
    │       ├── Hit within COMBO_RESET_TIME window?
    │       │       └── self.combo += 1   ✅ streak continues
    │       │
    │       └── Too slow?
    │               └── self.combo = 1    ❌ streak broken
    │
    └── self.score += result * self.combo
```

### Combo Resets
| Trigger | Behaviour |
|---|---|
| Next brick hit too late | `combo` resets to `1` via timeout check in `update()` |
| Ball falls below screen | `combo = 0` — losing a life wipes the streak |

### Score Comparison

| Scenario | Without Combo | With Combo (×3) |
|---|---|---|
| 3 bricks destroyed | 30 pts | 90 pts |
| 5 bricks destroyed | 50 pts | 150 pts+ |
| 2-HP brick hit | 5 pts | 15 pts |

---

## 🔧 V1.5 Implementation Details

### New in `settings.py`
```python
COMBO_RESET_TIME = 1500   # milliseconds — combo window duration
```

### New in `game.py`
```python
self.combo = 1
self.last_brick_hit_time = 0
```

### Combo Logic in `update()`
```python
# On brick hit
now = pygame.time.get_ticks()
if now - self.last_brick_hit_time < COMBO_RESET_TIME:
    self.combo += 1
else:
    self.combo = 1
self.last_brick_hit_time = now
self.score += result * self.combo

# Inactivity reset
if pygame.time.get_ticks() - self.last_brick_hit_time > COMBO_RESET_TIME:
    self.combo = 1

# Ball out
self.combo = 0
```

### Slow Power-Up Fix
```python
# ❌ Old (V1.4) — teleported ball back to paddle on expiry
self.ball.reset(self.paddle.rect)

# ✅ New (V1.5) — restores velocity in place, ball keeps moving
self.ball.vx = self.ball.base_speed
self.ball.vy = -abs(self.ball.base_speed)
```

### Combo HUD in `draw()`
```python
combo_txt = font.render(f"COMBO x{self.combo}", True, YELLOW)
surface.blit(combo_txt, (x, y))
```

---

## ⚡ Power-Up System

| Power-Up | Color | Drop Rate | Effect | Duration |
|---|---|---|---|---|
| 🟢 **Expand Paddle** | Green | 12% | Increases paddle width | 8 seconds |
| 🔵 **Slow Ball** | Blue | 8% | Reduces ball speed | 6 seconds |
| 🔴 **Extra Life** | Red | 5% | +1 life | Permanent |

---

## ✨ Full Feature Set

| Feature | Description |
|---|---|
| 🔥 **Combo Multiplier** | Streak-based score scaling — consecutive hits multiply points |
| ⚡ **Power-Up System** | 3 types with timed effects, drop rates, and stack control |
| ✨ **Particle Engine** | Ball trail, paddle sparks, brick explosion effects |
| 🟥 **2-HP Brick System** | Top 3 rows take 2 hits — darken on first hit, dot indicators |
| 💥 **1-HP Bricks** | Bottom 3 rows shatter in one hit |
| ⚡ **Dynamic Speed Scaling** | Ball speeds up every 5 destroyed bricks |
| 🎮 **Angle Physics** | Paddle hit offset influences ball bounce angle |
| 🏆 **Scoring** | +10 destroyed, +5 partial hit — all scaled by combo multiplier |
| ❤️ **3 Lives** | Ball falling costs one life and resets combo |
| 🎨 **Neon Dark UI** | Dark grid background, neon bricks with shine strips |
| 📊 **Live HUD** | Score, lives, speed, power-up timers, and combo counter |
| 🔊 **Sound Feedback** | Sounds on paddle hit, brick destroy, life lost, and win |

---

## 🗂️ Project Structure

```
brick-breaker-game/
│
├── main.py              # 🚀 Entry point
├── settings.py          # ⚙️  Constants — including COMBO_RESET_TIME
├── requirements.txt
├── .gitignore
├── README.md
├── LICENSE
│
├── game/
│   ├── __init__.py
│   ├── game.py          # 🧠 Game loop, combo logic, HUD, state machine
│   ├── ball.py          # ⚽ Velocity, bounce, speed scaling, trail particles
│   ├── paddle.py        # 🏓 Movement, width control, spark particles
│   ├── brick.py         # 🧱 HP logic, darkening, dot indicators, explosions
│   └── powerup.py       # ⚡ Drop logic, falling mechanic, timed effects
│
├── sounds/
│   ├── paddle.wav
│   ├── brick.wav
│   ├── lose.wav
│   └── win.wav
│
├── screenshots/
│   └── V1.0.png
│
└── assets/               # 🔮 Future — boss sprites, level maps
```

---

## 🎮 Controls

| Key | Action |
|---|---|
| `← / A` | Move paddle left |
| `→ / D` | Move paddle right |
| `SPACE` | Launch ball / continue after life loss |
| `R` | Restart after win or game over |
| `ESC` | Quit |

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/caffineblud/Brick-Breaker-Game.git
cd Brick-Breaker-Game
pip install -r requirements.txt
python main.py
```

---

## 🔮 Planned for V1.6+

- [ ] 🏆 High score persistence (`scores.json`)
- [ ] 🗺️ Multiple levels with increasing difficulty
- [ ] 👾 Boss brick / special stages
- [ ] 🔫 Laser power-up
- [ ] 🌀 Multi-ball power-up

---

## 👨‍💻 Author

**Yash Kumar Singh**

[![GitHub](https://img.shields.io/badge/GitHub-caffineblud-181717?style=flat-square&logo=github)](https://github.com/caffineblud)

⭐ If you like this project, consider giving it a star.