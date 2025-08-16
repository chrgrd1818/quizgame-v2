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
    if quiz:
      url = quiz['File']
      load = anvil.server.call('fetch_quiz_from_url', url)
      if load:
        load['quiz_selected']=quiz
        open_form("QuizPlay2", quiz_data=load)
      else:
        print("Request failed.")
    else:
      print("No quiz selected.")
