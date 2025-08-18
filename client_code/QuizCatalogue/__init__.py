from ._anvil_designer import QuizCatalogueTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class QuizCatalogue(QuizCatalogueTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.user = anvil.users.get_user()
    if not self.user:
      anvil.users.login_with_form()
      

    self.repeating_panel_quiz.items = app_tables.quizzes.search(tables.order_by("order", ascending=True), Enabled=True)
    self.repeating_panel_quiz.add_event_handler('x-play-quiz', self.play_quiz)

  def play_quiz(self, quiz, **event_args):
    fileId = quiz['File']
    getquiz = anvil.server.call('get_quiz', fileId)
    if getquiz:
        open_form("QuizPlay2", quiz_load=getquiz)
    else:
      print("No quiz.")
