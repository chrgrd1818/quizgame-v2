from ._anvil_designer import GameFormTemplate
from anvil import *
from ..game_classes import Dino, Platform, Cactus, Star, Level

class GameForm(GameFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)

    self.canvas_1.width = 1000
    self.canvas_1.height = 400
    self.canvas_1.background = "#555555"
    self.canvas_1.role = "game-canvas"

    # 1) Game objects
    self.dino         = Dino()
    self.score        = 10
    self.game_over    = False
    self.scroll_speed = 1

    # 2) Build levels
    # Constants
    BASE_Y    = 300               # all platforms share this y
    STAR_Y    = BASE_Y - 60       # stars float 60px above ground
    CACTUS_Y  = BASE_Y - 50       # cactus sprite is 50px tall
    LEVEL_GAP = 1000              # separation between level start points
    
    # Level 1
    lvl1_p = [
      Platform(0,   BASE_Y, 600),
    ]
    lvl1_c = [
      Cactus(200,   CACTUS_Y),
      Cactus(450,   CACTUS_Y),
    ]
    lvl1_s = [
      Star(550,     STAR_Y),
    ]
    
    # Level 2 (positions are relative; Level’s x_offset shifts them all by +LEVEL_GAP)
    lvl2_p = [
      Platform(0,   BASE_Y, 250),
      Platform(400, BASE_Y, 200),
    ]
    lvl2_c = [
      Cactus(100,   CACTUS_Y),
      Cactus(450,   CACTUS_Y),
    ]
    lvl2_s = [
      Star(650,     STAR_Y),
    ]
    
    # Level 3
    lvl3_p = [
      Platform(0,   BASE_Y, 150),
      Platform(300, BASE_Y, 200),
      Platform(700, BASE_Y, 150),
    ]
    lvl3_c = [
      Cactus(50,    CACTUS_Y),
      Cactus(450,   CACTUS_Y),
      Cactus(750,   CACTUS_Y),
    ]
    lvl3_s = [
      Star(900,     STAR_Y),
    ]
    
    # Assemble with x-offsets built into each Level
    self.levels = [
      Level(0 * LEVEL_GAP, lvl1_p, lvl1_c, lvl1_s),
      Level(1 * LEVEL_GAP, lvl2_p, lvl2_c, lvl2_s),
      Level(2 * LEVEL_GAP, lvl3_p, lvl3_c, lvl3_s),
    ]
    # 3) Hook up Timer
    #self.timer_1.interval = 1000/60   # ~16ms
    self.timer_1.enabled  = True

  # 4) Timer tick event
  def timer_1_tick(self, **event_args):
    if not self.game_over:
      #print("⏱ tick") 
      self._update_game()
    self._draw_game()

  # 5) Jump button
  def btn_jump_click(self, **event_args):
    if not self.game_over:
      self.dino.jump()
    else:  
      open_form('GameForm')
      
  # 6) Update & collisions
  def _update_game(self):
    for lvl in self.levels:
      lvl.update_scroll(self.scroll_speed)

    platforms  = sum((lvl.platforms for lvl in self.levels), [])
    cacti      = sum((lvl.cacti      for lvl in self.levels), [])
    stars      = sum((lvl.stars      for lvl in self.levels), [])

    self.dino.update(platforms)

    for c in list(cacti):
      if c.is_off_screen():
        cacti.remove(c)
      elif self._collide(self.dino.get_rect(), c.get_rect()):
        self.score -= 1
        cacti.remove(c)

    for s in list(stars):
      if s.is_off_screen():
        stars.remove(s)
      elif self._collide(self.dino.get_rect(), s.get_rect()):
        self.score += 3
        stars.remove(s)

    if self.dino.y > 410 or self.score < 1:
      self.game_over = True

  # 7) Draw everything
  def _draw_game(self):
    ctx = self.canvas_1
    ctx.reset_context()

  # 1) Clear the canvas
    ctx.clear_rect(0, 0, self.canvas_1.width, self.canvas_1.height)

  # 2) Draw sky background
    ctx.fill_style = "#C5EBF0"
    ctx.fill_rect(0, 0, self.canvas_1.width, self.canvas_1.height)

  # 3) Draw all platforms
    ctx.fill_style = "#555555"
    for lvl in self.levels:
      for p in lvl.platforms:
        ctx.fill_rect(p.x, p.y, p.width, p.height)

    # 4) Draw cacti
    ctx.fill_style = "#228B22"
    for lvl in self.levels:
      for c in lvl.cacti:
        ctx.fill_rect(c.x, c.y, c.width, c.height)

    # 5) Draw stars
    ctx.fill_style = "#D2DE09"
    for lvl in self.levels:
      for s in lvl.stars:
        ctx.fill_rect(s.x, s.y, s.width, s.height)

    # 6) Draw Dino
    ctx.fill_style = "#CDA132"
    d = self.dino
    ctx.fill_rect(d.x, d.y, d.width, d.height)

    # 7) Draw Score
    ctx.fill_style = "#000000"
    ctx.font      = "20px sans-serif"
    ctx.fill_text(f"Score: {self.score}", 10, 20)

    # 8) Game Over Overlay
    if self.game_over:
      ctx.font     = "30px sans-serif"
      ctx.fill_text("GAME OVER! Click Jump to Restart", 200, 200)

  # 8) Rectangle collision
  def _collide(self, a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax+aw < bx or bx+bw < ax or ay+ah < by or by+bh < ay)

  def link_home_click(self, **event_args):
    open_form('QuizHome')
    pass
