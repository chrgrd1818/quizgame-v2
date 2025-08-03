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
    c = self.canvas_1
    c.reset_context()
    c.fill_rect(0, 0, 800, 400, "#FFF")         # sky
    for lvl in self.levels: 
      lvl.draw(c)           # platforms, cacti, stars
    self.dino.draw(c)                             # dino
    c.fill_text(f"Score: {self.score}", 10, 20)   # score

    if self.game_over:
      c.fill_text("GAME OVER! Click Jump to Restart", 200, 200)

  # 8) Rectangle collision
  def _collide(self, a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax+aw < bx or bx+bw < ax or ay+ah < by or by+bh < ay)

  def link_home_click(self, **event_args):
    open_form('QuizHome')
    pass
