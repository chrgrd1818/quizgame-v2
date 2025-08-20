from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Get and cache the user
    self.user = anvil.server.call('get_current_user')
    if not self.user:
      self.user = anvil.users.login_with_form()

    # Example: check for "admin" role before opening admin form
    isAdmin = anvil.server.call('user_has_role', 'admin')
     
    self.link_admin.visible = True if isAdmin else False
    self.label_usercheck.text = self.user['pseudo']
    print(self.user['role'])

    # Any code you write here will run before the form opens.

  def link_home_click(self, **event_args):
    open_form("Home")

  def link_account_click(self, **event_args):
    open_form("Account2")

  def link_board_click(self, **event_args):
    open_form("Board")

  def link_game_2_click(self, **event_args):
    open_form("GameForm")

  def link_quizzes_2_click(self, **event_args):
    open_form("QuizCatalogue")

  def link_logout_click(self, **event_args):
    anvil.users.logout()
    anvil.js.window.localStorage.clear()  # Clear local storage if used
    anvil.js.window.sessionStorage.clear()  # Clear session storage
    anvil.js.window.location.reload()
    open_form('Home')

  def link_admin_click(self, **event_args):
    open_form("QuizAdmin2")
    
