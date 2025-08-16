from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

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
