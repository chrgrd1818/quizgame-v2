import anvil.server
import anvil.http
import json
from anvil.tables import app_tables
from datetime import datetime
import anvil.tz

BASE_URL = "https://raw.githubusercontent.com/chrgrd1818/questacademy/refs/heads/main/quizzes/"

def group_questions_by_level(questions):
  levels = {}
  for q in questions:
    lvl = q['difficultyLevel']
    levels.setdefault(lvl, []).append(q)
  for lvl in levels:
    levels[lvl].sort(key=lambda q: q['id'])
  return dict(sorted(levels.items()))

def _fetch_and_group(file_stub):
  # Fetch from GitHub
  url = f"{BASE_URL}{file_stub}.json"
  raw_text = anvil.http.request(url, method="GET", json=False, timeout=30)
  quiz_data = json.loads(raw_text)
  # Group at save time
  grouped = group_questions_by_level(quiz_data['questions'])
  # Add metadata back in if needed
  quiz_data['grouped_questions'] = grouped
  return quiz_data

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