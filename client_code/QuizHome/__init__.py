from ._anvil_designer import QuizHomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class QuizHome(QuizHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_2.items = app_tables.quizzes.search()
    self.repeating_panel_2.add_event_handler('x-play-quiz', self.play_quiz) 
    
  def admin_link_click(self, **event_args):
    open_form("QuizList")

  def play_quiz(self, quiz, **event_args):
      if quiz:
        url = quiz['File']
        load = anvil.server.call('fetch_quiz_from_url', url)
        if load:
          
          open_form("QuizPlay", quiz_data=load)
        else:
          print("Request failed.")
      else:
        print("No quiz selected.")

  def link_game_click(self, **event_args):
    open_form("GameForm")
   
