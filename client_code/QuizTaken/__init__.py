from ._anvil_designer import QuizTakenTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class QuizTaken(QuizTakenTemplate):
  def __init__(self, selected_user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.user = selected_user or anvil.users.get_user()
    print(f"user_id → {self.user.get_id()}")
    if not self.user:
      Notification("No user selected or logged in.").show()
      return

    records = anvil.server.call(
      'get_quizzes_for_user',
      self.user.get_id()
    )
    print("len(records) →", len(records))
    self.repeating_panel_1.items = records

  def link_back_click(self, **event_args):
    open_form("Account")


