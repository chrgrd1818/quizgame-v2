import random

GROUND_Y = 300

class Dino:
  def __init__(self, x=100, width=40, height=50,
               jump_force=-15, gravity=0.8):
    self.x = x
    self.width = width
    self.height = height
    self.y = GROUND_Y - height
    self.vy = 0
    self.jump_force = jump_force
    self.gravity = gravity
    self.is_jumping = False

  def update(self):
    self.vy += self.gravity
    self.y  += self.vy
    if self.y + self.height >= GROUND_Y:
      self.y = GROUND_Y - self.height
      self.vy = 0
      self.is_jumping = False

  def jump(self):
    if not self.is_jumping:
      self.vy = self.jump_force
      self.is_jumping = True

  def draw(self, canvas):
    canvas.fill_style = "#CDA132"
    canvas.fill_rect(self.x, self.y, self.width, self.height)

  def get_rect(self):
    return (self.x, self.y, self.width, self.height)


class Cactus:
  def __init__(self, x, width=20, speed=6, color="#228B22"):
    self.x      = x
    self.width  = width
    self.height = random.randint(40, 80)
    self.y      = GROUND_Y - self.height
    self.speed  = speed
    self.color  = color

  def update(self):
    self.x -= self.speed

  def draw(self, canvas):
    canvas.fill_style = self.color
    canvas.fill_rect(self.x, self.y, self.width, self.height)

  def is_off_screen(self):
    return self.x + self.width < 0

  def get_rect(self):
    return (self.x, self.y, self.width, self.height)


class Star:
  def __init__(self, x, y, width=10, height=10, speed=6, color="#D2DE09"):
    self.x, self.y         = x, y
    self.width, self.height = width, height
    self.speed             = speed
    self.color             = color

  def update(self):
    self.x -= self.speed

  def draw(self, canvas):
    canvas.fill_style = self.color
    canvas.fill_rect(self.x, self.y, self.width, self.height)

  def is_off_screen(self):
    return self.x + self.width < 0

  def get_rect(self):
    return (self.x, self.y, self.width, self.height)