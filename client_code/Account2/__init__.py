from ._anvil_designer import Account2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..router import go_to, get_current_user


class Account2(Account2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.user = get_current_user()
      
    
    print(f"user_id → {self.user.get_id()}")
    print(f"user_name → {self.user['pseudo']}")

    self.label_username.text = self.user['pseudo']
    self.label_userrole.text = self.user['role']
    self.label_usergroup.text = self.user['group']

    # Any code you write here will run before the form opens.

