from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..router import go_to, get_current_user
from ..Base import Base


class Home(HomeTemplate):
  def __init__(self, **properties):
    
    self.init_components(**properties)
    self.user = get_current_user()

    go_to("QuizCatalogue")