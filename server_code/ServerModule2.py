import anvil.server
import anvil.http
import json
from anvil.tables import app_tables
from datetime import datetime
import anvil.tz
import requests

BASE_URL = "https://raw.githubusercontent.com/chrgrd1818/questacademy/refs/heads/main/quizzes/"

def get_file_github(filename):
  full_url = BASE_URL + "" + filename + ".json"
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


def group_questions_by_level(questions):
  levels = {}
  for q in questions:
    lvl = str(q['difficultyLevel'])  # force string key
    levels.setdefault(lvl, []).append(q)
  for lvl in levels:
    levels[lvl].sort(key=lambda q: q['id'])
  return dict(sorted(levels.items()))

def _fetch_and_group(file_stub):
  # Fetch from GitHub
  quiz_data = get_file_github(file_stub)
 
  #print(quiz_data['questions'])
  # Group at save time
  grouped = group_questions_by_level(quiz_data['questions'])
  # Add metadata back in if needed
  #quiz_data['grouped_questions'] = grouped
  return grouped

@anvil.server.callable
def add_parse_quiz(quiz_data):
  title = quiz_data.get('Title')
  file_stub = quiz_data.get('File')
  if not title or not file_stub:
    raise ValueError("Title and File are required.")

  parsed_and_grouped = _fetch_and_group(file_stub)
  now = datetime.now(anvil.tz.tzlocal())

  row = app_tables.quizzes.get(Title=title)
  if row:
    row.update(
      File=file_stub,
      Date=now,
      QuizDictionary=parsed_and_grouped
    )
  else:
    app_tables.quizzes.add_row(
      Title=title,
      File=file_stub,
      Date=now,
      QuizDictionary=parsed_and_grouped
    )
  return {"ok": True, "title": title}


@anvil.server.callable
def update_quiz(quiz, quiz_data):
  if quiz_data.get('Title') and quiz_data.get('File') :
    quiz_data['Date'] = datetime.now(anvil.tz.tzlocal())
    quiz.update(**quiz_data)

@anvil.server.callable
def delete_quiz(quiz):
  quiz.delete()


@anvil.server.callable
def get_quiz(fileId=None):
  # Try exact title match first (if provided)
  row = app_tables.quizzes.get(File=fileId) if fileId else None

  if not row:
    return None
    raise ValueError("Quiz not found.")

  grouped = row['QuizDictionary'] or {}
  total = sum(len(qs) for qs in grouped.values())

  return {
    "Title": row['Title'],
    "QuizDictionary": grouped,   # grouped dict with string level keys
    "Date": row['Date'],
    "TotalQuestions": total
  }