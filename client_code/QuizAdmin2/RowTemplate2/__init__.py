from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_edit_click(self, **event_args):
    self.parent.raise_event('x-edit-quiz', quiz=self.item)

  def button_delete_click(self, **event_args):
    self.parent.raise_event('x-delete-quiz', quiz=self.item)

  def button_print_click(self, **event_args):
    self.parent.raise_event('x-print-quiz', quiz=self.item)
    pass

 
