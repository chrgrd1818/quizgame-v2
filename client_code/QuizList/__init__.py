from ._anvil_designer import QuizListTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..QuizEdit import QuizEdit

class QuizList(QuizListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = app_tables.quizzes.search()
    #add this line to set the event handler
    self.repeating_panel_1.add_event_handler('x-edit-quiz', self.edit_quiz)
    self.repeating_panel_1.add_event_handler('x-delete-quiz', self.delete_quiz)
    self.repeating_panel_1.add_event_handler('x-print-quiz', self.print_quiz)

  def add_quiz_click(self, **event_args):
    item = {}
    editing_form = QuizEdit(item=item)

    #if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      #add the movie to the Data Table with the filled in information
      anvil.server.call('add_quiz', item)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.quizzes.search()

  def edit_quiz(self, quiz, **event_args):
    #movie is the row from the Data Table
      item = dict(quiz)
      editing_form = QuizEdit(item=item)
  
    #if the user clicks OK on the alert
      if alert(content=editing_form, large=True):
        #pass in the Data Table row and the updated info
        anvil.server.call('update_quiz', quiz, item)
        #refresh the Data Grid
        self.repeating_panel_1.items = app_tables.quizzes.search()
      
  def delete_quiz(self, quiz, **event_args):
    if confirm("Do you really want to delete ?"):
      anvil.server.call('delete_quiz', quiz)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.quizzes.search()

  def print_quiz(self, quiz, **event_args):
    if quiz:
      url = quiz['File']
      # Call your server fn
      load = anvil.server.call('fetch_quiz_from_url', url)
      if load:
        # For example: print every question to console
        for q in load['questions']:
          print(f"Q{q['id']} (Lvl {q['difficultyLevel']}): {q['text']}")
      else:
        print("Request failed.")

  def home_link_click(self, **event_args):
    open_form("QuizHome")

      

     

  
