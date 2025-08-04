from ._anvil_designer import LogSignTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class LogSign(LogSignTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def button_check_click(self, **event_args):
    self.parent.raise_event('x-sign', data=self.item)
