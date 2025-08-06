from ._anvil_designer import AccountTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Account(AccountTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def link_admin_quizzes_click(self, **event_args):
    open_form('QuizList')

  def link_log_out_click(self, **event_args):
    anvil.users.logout()
    open_form('QuizHome')

  def link_home_click(self, **event_args):
    open_form('QuizHome')
    
