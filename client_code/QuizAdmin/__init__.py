from ._anvil_designer import QuizAdminTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class QuizAdmin(QuizAdminTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.user = anvil.users.get_user()
    if not self.user:
      anvil.users.login_with_form()

    open_form("QuizCatalogue")
    # Any code you write here will run before the form opens.
