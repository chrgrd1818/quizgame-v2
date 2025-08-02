from ._anvil_designer import QuizPlayTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert
from datetime import datetime

def group_questions_by_level(questions):
  levels = {}
  for qq in questions:
    lvl = qq['difficultyLevel']
    levels.setdefault(lvl, []).append(qq)
    # Sort levels and questions within each level by ID
  for lvl in levels:
    levels[lvl] = sorted(levels[lvl], key=lambda qq: qq['id'])
  return dict(sorted(levels.items()))

class QuizPlay(QuizPlayTemplate):
  def __init__(self, quiz_data, **properties):
    self.init_components(**properties)
    # Prepare levels
    self.levels = group_questions_by_level(quiz_data['questions'])
    self.level_keys = list(self.levels.keys())
    # State trackers
    self.current_level_idx = 0
    self.current_q_idx = 0
    self.start_time = None
    self.start_time = datetime.utcnow()
    self.show_question()

  def btn_start_click(self, **event_args):
    self.current_level_idx = 0
    self.current_q_idx = 0
    self.start_time = datetime.utcnow()
    self.show_question()

  def show_question(self):
    # Check if all levels completed
    if self.current_level_idx >= len(self.level_keys):
      elapsed = (datetime.utcnow() - self.start_time).seconds
      self.lbl_question.text = "🎉 Vous avez terminé le quiz !"
      self.radio_group.items = []
      self.lbl_feedback.text = f"Temps total : {elapsed}s"
      return

    lvl = self.level_keys[self.current_level_idx]
    questions = self.levels[lvl]
    # Load question
    qq = questions[self.current_q_idx]
    self.lbl_question.text = f"Niveau {lvl} : {qq['text']}"
    self.radio_group.items = [(opt['text'], opt['correct']) for opt in qq['options']]
    self.radio_group.selected_value = None
    self.lbl_feedback.text = ""

  def btn_submit_click(self, **event_args):
    selected = self.radio_group.selected_value
    if selected is None:
      alert("Veuillez choisir une réponse !")
      return

    if selected:
      self.lbl_feedback.text = "✅ Correct !"
      self.current_q_idx += 1
      lvl = self.level_keys[self.current_level_idx]
      # If end of this level, move to next
      if self.current_q_idx >= len(self.levels[lvl]):
        self.current_level_idx += 1
        self.current_q_idx = 0
    else:
      self.lbl_feedback.text = "❌ Faux — retour au début du niveau."
      # Reset to first question of current level
      self.current_q_idx = 0

    # Slight delay then show next or retry
    self.call_later(1.0, self.show_question)
