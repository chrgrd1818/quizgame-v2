import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import anvil.tz
import requests
from collections import defaultdict

@staticmethod
def seconds_to_min_sec(seconds):
  """Converts seconds to MM:SS format."""
  if not isinstance(seconds, int) or seconds is None or seconds < 0:
    return "-:-"  # Valeur invalide ou nulle → retourne 00:00
  minutes = seconds // 60
  secs = seconds % 60
  return f"{minutes:02}:{secs:02}"
    
@anvil.server.callable
def fetch_data_image(path):
  row = app_tables.images.get(ImageID=path)
  return row['Image'] if row else None

  
@anvil.server.callable
def get_quizzes_for_user(user_id):
  # 1. Look up the user
  user = app_tables.users.get_by_id(user_id)
  if user is None:
    raise Exception("User not found")

  # 2. Fetch all quizzes and this user's quiz-attempt rows
  all_quizzes = app_tables.quizzes.search(Enabled=True)              # All definitions
  taken_rows  = app_tables.user_quiz.search(User=user)   # Attempts by this user

  # 3. Group attempts by quiz_id
  attempts_map = defaultdict(list)
  for uq in taken_rows:
    quiz_id = uq['Quiz'].get_id()
    attempts_map[quiz_id].append(uq)

  # 4. Build the flat result list
  result = []
  for quiz in all_quizzes:
    quiz_id = quiz.get_id()
    attempts = attempts_map.get(quiz_id, [])

    if attempts:
      # Pick the fastest attempt (smallest Time).  
      # For latest by date, swap min() → max() and key→ lambda x: x['DateTime'].
      best = min(attempts, key=lambda x: x['Time'])
      taken = True,
      score = best['Score'],
      time  = best['Time']
      date  = best['DateTime']
    else:
      taken = False
      time  = None
      date  = None
      score = None
 
  
    result.append({
      'id'    : quiz.get_id(),       # optional, if you need it later
      'title' : quiz['Title'],
      'taken' : "Yes" if taken else "No",
      'time'  : seconds_to_min_sec(time),
      'date'  : date,
      'score': score if score else "-"
    })

  return result



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
def fetch_quiz_from_url(filename):
  base_url = "https://raw.githubusercontent.com/chrgrd1818/questacademy/refs/heads/main/quizzes/"
  full_url = base_url + filename + ".json"
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
  app_tables.user_quiz.add_row(User=user, Quiz=quiz, Score=quiz['nquests'], Time=time, DateTime=datetime.utcnow())

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

@anvil.server.callable
def get_group_users(group):
  rows = app_tables.users.search(group=group)
  return rows