from ._anvil_designer import QuizAdmin2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..QuizEdit import QuizEdit


class QuizAdmin2(QuizAdmin2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.user = anvil.users.get_user()
    if not self.user:
      anvil.users.login_with_form()


    self.repeating_panel_1.items = app_tables.quizzes.search()
    #add this line to set the event handler
    self.repeating_panel_1.add_event_handler('x-edit-quiz', self.edit_quiz)
    self.repeating_panel_1.add_event_handler('x-delete-quiz', self.delete_quiz)
    self.repeating_panel_1.add_event_handler('x-print-quiz', self.print_quiz)

  def add_quiz(self, **event_args):
    item = {}
    editing_form = QuizEdit(item=item)

    #if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      #add  to the Data Table with the filled in information
      saving = anvil.server.call('add_parse_quiz', item)
      print(saving)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.quizzes.search()

  def edit_quiz(self, quiz, **event_args):
    #item is the row from the Data Table
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
    fileId = quiz['File']
    getquiz = anvil.server.call('get_quiz', fileId)
    print(getquiz or "Request failed.")


  def home_link_click(self, **event_args):
    open_form("QuizHome")

  def button_add_click(self, **event_args):
    self.add_quiz(**event_args)
