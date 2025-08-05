import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import anvil.tz
import requests


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

@anvil.server.callable
def fetch_quiz_from_url(url):
  base_url = "https://raw.githubusercontent.com/chrgrd1818/questacademy/refs/heads/main/quizzes/"
  full_url = base_url + url + ".json"
  try:

    response = requests.get(full_url)
    response.raise_for_status() 
    quiz_dict = response.json()  
    return quiz_dict
    
  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except requests.exceptions.ConnectionError:
    print("Connection error — check your internet or the URL.")
  except requests.exceptions.Timeout:
    print("Request timed out — server might be slow or unreachable.")
  except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")
  
@anvil.server.callable
def set_score_quiz(quiz, time):
  user = anvil.users.get_user()
  if not user:
    raise Exception("No User or Login required")
  app_tables.user_quiz.add_row(User=user, Quiz=quiz, Time=time)

@anvil.server.callable
def get_score_quiz(quiz):
  user = anvil.users.get_user()
  if not user:
    raise Exception("No User or Login required")
  rows = app_tables.user_quiz.search(User=user)
  return [(r['Time']) for r in rows]

@anvil.server.callable
def get_all_score_quiz():
  user = anvil.users.get_user()
  if not user:
    raise Exception("No User or Login required")
  rows = app_tables.user_quiz.search(User=user)
  return [(r['Quiz'], r['Time']) for r in rows]

@anvil.server.callable
def get_user():
  return anvil.users.get_user()