import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# game_classes.py

import random

class Dino:
  def __init__(self, x=100, width=40, height=50,
               jump_force=-15, gravity=0.8):
    self.x, self.width, self.height = x, width, height
    self.y = 300 - height
    self.vy = 0
    self.jump_force, self.gravity = jump_force, gravity
    self.is_jumping = False

  def update(self, platforms):
    self.vy += self.gravity
    self.y += self.vy

    # Determine floor from platforms
    floor_y = 300
    for p in platforms:
      px, py, pw, ph = p.get_rect()
      if (self.x + self.width > px and self.x < px + pw):
        floor_y = min(floor_y, py)

    if self.y + self.height >= floor_y:
      self.y = floor_y - self.height
      self.vy = 0
      self.is_jumping = False

  def jump(self):
    if not self.is_jumping:
      self.vy = self.jump_force
      self.is_jumping = True

  def draw(self, canvas, color="#32CD32"):
    canvas.fill_rect(self.x, self.y, self.width, self.height, color)

  def get_rect(self):
    return (self.x, self.y, self.width, self.height)


class Platform:
  def __init__(self, x, y, width, height=10, color="#555"):
    self.x, self.y, self.width, self.height = x, y, width, height
    self.color = color

  def draw(self, canvas):
    canvas.fill_rect(self.x, self.y, self.width, self.height, self.color)

  def get_rect(self):
    return (self.x, self.y, self.width, self.height)


class Cactus:
  def __init__(self, x, ground_y=300, width=20, speed=6, color="#228B22"):
    self.x = x
    self.width = width
    self.height = random.randint(40, 80)
    self.y = ground_y - self.height
    self.speed = speed
    self.color = color

  def update(self):
    self.x -= self.speed

  def draw(self, canvas):
    canvas.fill_rect(self.x, self.y, self.width, self.height, self.color)

  def is_off_screen(self):
    return self.x + self.width < 0

  def get_rect(self):
    return (self.x, self.y, 1, self.height)


class Star:
  def __init__(self, x, y, width=10, height=10, speed=6, color="#D2DE09"):
    self.x, self.y = x, y
    self.width, self.height = width, height
    self.speed = speed
    self.color = color

  def update(self):
    self.x -= self.speed

  def draw(self, canvas):
    canvas.fill_rect(self.x, self.y, self.width, self.height, self.color)

  def is_off_screen(self):
    return self.x + self.width < 0

  def get_rect(self):
    return (self.x, self.y, 1, self.height)


class Level:
  def __init__(self, start_x, platforms, cacti, stars):
    self.platforms = [Platform(p.x + start_x, p.y, p.width) for p in platforms]
    self.cacti     = [Cactus(c.x + start_x) for c in cacti]
    self.stars     = [Star(s.x + start_x, s.y) for s in stars]

  def update_scroll(self, dx):
    for p in self.platforms:
      p.x -= dx
    for c in self.cacti:
      c.update()
    for s in self.stars:
      s.update()

  def draw(self, canvas):
    for p in self.platforms: 
      p.draw(canvas)
    for c in self.cacti:     
      c.draw(canvas)
    for s in self.stars:     
      s.draw(canvas)