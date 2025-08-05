from ._anvil_designer import QuizHomeTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class QuizHome(QuizHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #anvil.users.login_with_form()
    self.repeating_panel_2.items = app_tables.quizzes.search()
    self.repeating_panel_2.add_event_handler('x-play-quiz', self.play_quiz)
    if anvil.users.get_user():
      self.label_user.text = anvil.users.get_user()['email']
    else:
      self.label_user.text = ""
    
  def admin_link_click(self, **event_args):
    open_form("QuizList")

  def play_quiz(self, quiz, **event_args):
      if quiz:
        url = quiz['File']
        title = quiz['Title']
        load = anvil.server.call('fetch_quiz_from_url', url)
        if load:
          load['title']=title
          open_form("QuizPlay", quiz_data=load)
        else:
          print("Request failed.")
      else:
        print("No quiz selected.")

  def link_game_click(self, **event_args):
    open_form("GameForm")
  
  
  def set_score_quiz(self, quiz, time):
    self.server.call('set_score_quiz', quiz, time)
  
  def get_score_quiz(self, quiz):
    return self.server.call('get_score_quiz', quiz)

  def get_all_score_quiz(self, quiz):
    return self.server.call('get_all_score_quiz')

  def link_login_click(self, **event_args):
    open_form("LogSign")

  def link_account_click(self, **event_args):
    anvil.users.login_with_form()
    user = anvil.server.call('get_user')
    if user and user['role'] == 'admin':
      open_form('QuizList')
    else:
      open_form('QuizHome')
      
  def link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form('QuizHome')
    

 