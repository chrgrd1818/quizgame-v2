import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import anvil.tz


@anvil.server.callable
def add_quiz(quiz_data):
  if quiz_data.get('Title') and quiz_data.get('File') :
    quiz_data['Date'] = datetime.now(anvil.tz.tzlocal())
    app_tables.quizzes.add_row(**quiz_data)

@anvil.server.callable
def update_quiz(quiz, quiz_data):
  if quiz_data.get('Title') and quiz_data.get('File') :
    quiz_data['Date'] = datetime.now(anvil.tz.tzlocal())
    quiz.update(**quiz_data)

@anvil.server.callable
def delete_quiz(quiz):
  quiz.delete()