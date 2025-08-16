from ._anvil_designer import BoardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Board(BoardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.user = anvil.users.get_user()
    if not self.user:
      anvil.users.login_with_form()
      
    #print(f"user_group → {self.user['group']}")
    self.repeating_panel_users.add_event_handler('x-view-achievements', self.view_achievements)

    rows = anvil.server.call(
      'get_group_users',
      self.user['group']
    )
    #print("len(records) →", len(rows))
    self.repeating_panel_users.items = rows
    self.view_achievements(self.user)
    self.label_results.text = f"RESULTS FOR {self.user['pseudo']}"

  def view_achievements(self, selected_user, **event_args):
    _user = selected_user or self.user
    self.label_results.text = f"RESULTS FOR {_user['pseudo']}"
    entries = anvil.server.call(
      'get_quizzes_for_user',
      _user.get_id()
    )
    # print("len(records) →", len(records))
    self.repeating_panel_entries.items = entries