from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    user = anvil.server.call('get_user')
    if not user:
      anvil.users.login_with_form()
      return
    
    open_form('QuizCatalogue')
    # Any code you write here will run before the form opens.
