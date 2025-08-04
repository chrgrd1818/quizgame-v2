from ._anvil_designer import GameFormTemplate
from anvil import *
from ..game_classes import Dino, Cactus, Star, GROUND_Y
import random

class GameForm(GameFormTemplate):
  
  FRAME_RATE     = 1/60
  SCORE_START    = 12
  STAR_POINT = 1
  CACTUS_POINT = 2
  
  def __init__(self, **properties):
    self.init_components(**properties)

    # base frame intervals at level 1
    self.SPAWN_BASE   = 80    # cactus
    self.STAR_BASE    = 200   # star
    # clamps to avoid absurdly fast or slow spawns
    self.SPAWN_MIN    = 20
    self.STAR_MAX     = 400
    self.INTERVAL_MODIFIER = 5
    # Base scroll settings
    self.scroll_speed = 6
    # Level‐up every N frames
    self.LEVEL_UP_INTERVAL = 1000
    # How much speed increases per level
    self.SPEED_INCREMENT = 1
    # Track frames and levels
    self.frame_count = 0
    self.level = 1

    # Canvas setup
    self.canvas_1.width      = 1000
    self.canvas_1.height     = 400
    self.canvas_1.background = "#555555"

    # Game state
    self.dino       = Dino()
    self.cacti      = []
    self.stars      = []
    self.score      = self.SCORE_START
    self.game_over  = False
    self.frame_count = 0
    self.paused = False

    # Start timer
    self.timer_1.interval = self.FRAME_RATE
    self.timer_1.enabled  = True

  def timer_1_tick(self, **event_args):
    if not self.game_over:
      self._update_game()
    self._draw_game()

  def btn_jump_click(self, **event_args):
    if not self.game_over:
      self.dino.jump()
    else:
      open_form('GameForm')  # restart

  def _update_game(self):
    if self.paused:
      return
    self.frame_count += 1

    spawn_interval = max(self.SPAWN_MIN,
                         self.SPAWN_BASE - (self.level - 1) * self.INTERVAL_MODIFIER)

    star_interval = min(self.STAR_MAX,
                        self.STAR_BASE + (self.level - 1) * self.INTERVAL_MODIFIER)

    # Check for leveling up
    if self.frame_count % self.LEVEL_UP_INTERVAL == 0:
      self.level += 1
      self.scroll_speed += self.SPEED_INCREMENT
      # Optional: print or draw the new level
      print(f"Level up! Now at level {self.level}, speed={self.scroll_speed}")
      self.score += self.SCORE_START 
      
    # Update Dino
    self.dino.update()

    # Spawn obstacles
    if self.frame_count % spawn_interval == 0:
      self.cacti.append(Cactus(self.canvas_1.width))
    if self.frame_count % star_interval == 0:
      # star appears betwwen 100 and 120px above ground
      y = GROUND_Y - random.randint(100, 120)
      self.stars.append(Star(self.canvas_1.width, y))

      # Move & cull off-screen
    for lst in (self.cacti, self.stars):
      for obj in lst:
        obj.update()
    self.cacti = [c for c in self.cacti if not c.is_off_screen()]
    self.stars = [s for s in self.stars if not s.is_off_screen()]

    # Handle collisions
    self._handle_collisions()

    # Check Game Over
    if self.score < 1:
      self.game_over = True

  def _handle_collisions(self):
    dino_rect = self.dino.get_rect()

    # Cactus collisions
    survivors = []
    for c in self.cacti:
      if self._collide(dino_rect, c.get_rect()):
        self.score -= self.CACTUS_POINT
      else:
        survivors.append(c)
    self.cacti= survivors

    # Star collisions
    survivors = []
    for s in self.stars:
      if self._collide(dino_rect, s.get_rect()):
        self.score += self.STAR_POINT
      else:
        survivors.append(s)
    self.stars = survivors

  def _draw_game(self):
    ctx = self.canvas_1
    w, h = ctx.width, ctx.height

    # Clear & sky
    ctx.reset_context()
    ctx.clear_rect(0, 0, w, h)
    ctx.fill_style = "#CEF1F5"
    ctx.fill_rect(0, 0, w, h)

    # Ground line
    ctx.begin_path()
    ctx.stroke_style = "#4D4825"
    ctx.line_width   = 5
    ctx.move_to(0, GROUND_Y)
    ctx.line_to(w, GROUND_Y)
    ctx.stroke()

    # Draw all objects (they each set their own fill_style)
    for c in self.cacti:
      c.draw(ctx)

    for s in self.stars:
      s.draw(ctx)

    self.dino.draw(ctx)

    # UI: score & game over & levels
    ctx.fill_style = "#222222"
    ctx.font        = "36px sans-serif"
    ctx.fill_text(f"Points: {self.score}", 30, 50)

    ctx.fill_style = "#222222"
    ctx.font        = "36px sans-serif"
    ctx.fill_text(f"Level: {self.level}", 300, 50)

    if self.game_over:
      ctx.font = "50px sans-serif"
      ctx.fill_text("GAME OVER! Click Jump to Restart", 250, 250)

  @staticmethod
  def _collide(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw  < bx or
                bx + bw < ax or
                ay + ah  < by or
                by + bh < ay)

  def link_home_click(self, **event_args):
    open_form('QuizHome')

  def btn_pause_click(self, **event_args):
    # Flip state
    self.paused = not self.paused
    # Update button label
    self.btn_pause.text = "RESUME" if self.paused else "PAUSE"


