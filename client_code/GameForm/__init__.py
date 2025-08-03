from ._anvil_designer import GameFormTemplate
from anvil import *
from ..game_classes import Dino, Platform, Cactus, Star, Level

class GameForm(GameFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)

    # 1) Game objects
    self.dino         = Dino()
    self.score        = 0
    self.game_over    = False
    self.scroll_speed = 5

    # 2) Build levels
    lvl1_p = [Platform(0,300,200), Platform(250,260,120)]
    lvl1_c = [Cactus(180), Cactus(350)]
    lvl1_s = [Star(300,240)]

    lvl2_p = [Platform(600,300,180), Platform(820,270,140)]
    lvl2_c = [Cactus(650)]
    lvl2_s = [Star(700,250), Star(860,240)]

    self.levels = [
      Level(0,   lvl1_p, lvl1_c, lvl1_s),
      Level(900, lvl2_p, lvl2_c, lvl2_s)
    ]

    # 3) Hook up Timer
    #self.timer_1.interval = 1000/60   # ~16ms
    self.timer_1.enabled  = True

  # 4) Timer tick event
  def timer_1_tick(self, **event_args):
    if not self.game_over:
      #print("⏱ tick")    # <-- should flood your server log at ~60/sec
      self._update_game()
    self._draw_game()

  # 5) Jump button
  def btn_jump_click(self, **event_args):
    if not self.game_over:
      self.dino.jump()

  # 6) Update & collisions
  def _update_game(self):
    for lvl in self.levels:
      lvl.update_scroll(self.scroll_speed)

    platforms = sum((lvl.platforms for lvl in self.levels), [])
    cacti      = sum((lvl.cacti      for lvl in self.levels), [])
    stars      = sum((lvl.stars      for lvl in self.levels), [])

    self.dino.update(platforms)

    for c in list(cacti):
      if c.is_off_screen():
        self.score += 1
        cacti.remove(c)
      elif self._collide(self.dino.get_rect(), c.get_rect()):
        self.game_over = True

    for s in list(stars):
      if s.is_off_screen():
        stars.remove(s)
      elif self._collide(self.dino.get_rect(), s.get_rect()):
        self.score += 5
        stars.remove(s)

    if self.dino.y > 400:
      self.game_over = True

  # 7) Draw everything
  def _draw_game(self):
    ctx = self.canvas_1
    ctx.reset_context()

  # 1) Clear the canvas
    ctx.clear_rect(0, 0, self.canvas_1.width, self.canvas_1.height)

  # 2) Draw sky background
    ctx.fill_style = "#ffffff"
    ctx.fill_rect(0, 0, 800, 400)

  # 3) Draw all platforms
    ctx.fillStyle = "#555555"
    for lvl in self.levels:
      for p in lvl.platforms:
        ctx.fill_rect(p.x, p.y, p.width, p.height)

    # 4) Draw cacti
    ctx.fill_style = "#228B22"
    for lvl in self.levels:
      for c in lvl.cacti:
        ctx.fill_rect(c.x, c.y, c.width, c.height)

    # 5) Draw stars
    ctx.fillStyle = "#FFD700"
    for lvl in self.levels:
      for s in lvl.stars:
        ctx.fill_rect(s.x, s.y, s.width, s.height)

    # 6) Draw Dino
    ctx.fill_style = "#32CD32"
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
