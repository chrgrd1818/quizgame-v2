import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import Timer
from datetime import datetime

class ChronoHelper:
  def __init__(self, tick_callback=None):
    self.timer = Timer(interval=1)
    self.timer.set_event_handler('tick', self._on_tick)
    self._start_time = None
    self._elapsed = 0
    self._running = False
    self._tick_callback = tick_callback  # function to call on each tick

  def start(self):
    self._start_time = datetime.utcnow()
    self._elapsed = 0
    self._running = True
    self.timer.interval = 1
    self.timer.enabled = True

  def stop(self):
    self.timer.enabled = False
    self._running = False
    if self._start_time:
      self._elapsed = int((datetime.utcnow() - self._start_time).total_seconds())

  def reset(self):
    self.timer.enabled = False
    self._start_time = None
    self._elapsed = 0
    self._running = False

  def get_elapsed(self):
    if self._running and self._start_time:
      return int((datetime.utcnow() - self._start_time).total_seconds())
    return self._elapsed

  def seconds_to_min_sec(self, seconds):
    m, s = divmod(seconds, 60)
    return "{:02}:{:02}".format(m, s)

  def _on_tick(self, **event_args):
    if self._running and self._start_time:
      self._elapsed = int((datetime.utcnow() - self._start_time).total_seconds())
      if self._tick_callback:
        self._tick_callback(self._elapsed)