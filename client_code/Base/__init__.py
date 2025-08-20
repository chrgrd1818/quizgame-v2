from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from ..router import go_to, get_current_user

class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Get and cache the user
    self.user = get_current_user()
    self.pseudo = self.user['pseudo']
    self.role = self.user['role']
    isAdmin = ( self.role == 'admin')
    print(self.role + " : " + self.pseudo)
     
    self.link_admin.visible = True if isAdmin else False
    self.label_usercheck.text = self.pseudo
    print(self.user['role'])

  def link_home_click(self, **event_args):
    go_to("Home")
  def link_account_click(self, **event_args):
    go_to("Account2")
  def link_board_click(self, **event_args):
    go_to("Board")
  def link_game_2_click(self, **event_args):
    go_to("GameForm")
  def link_quizzes_2_click(self, **event_args):
    go_to("QuizCatalogue")
  def link_admin_click(self, **event_args):
    go_to("QuizAdmin2")
  def link_logout_click(self, **event_args):
    anvil.users.logout()
    anvil.js.window.localStorage.clear()  # Clear local storage if used
    anvil.js.window.sessionStorage.clear()  # Clear session storage
    anvil.js.window.location.reload()
    go_to('Home')


    
