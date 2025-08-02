from ._anvil_designer import QuizPlayTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

def group_questions_by_level(questions):
  levels = {}
  for qq in questions:
    lvl = qq['difficultyLevel']
    levels.setdefault(lvl, []).append(qq)
  # Sort levels and questions within each level by ID
  for lvl in levels:
    levels[lvl].sort(key=lambda qq: qq['id'])
  return dict(sorted(levels.items()))

class QuizPlay(QuizPlayTemplate):
  def __init__(self, quiz_data, **properties):
    self.init_components(**properties)

    # 1) Timer: set interval in seconds (Designer or here)
    #    In Designer, set timer_next.interval = 1.0 and repeating = False
    #    Or uncomment below to override in code:
    self.timer_next.interval = 3.0
    self.timer_next.repeating = False
    self.timer_next.enabled = False  # make sure it doesn’t start on load
    self.timer_next.interval = 0

    # Prepare levels
    self.levels = group_questions_by_level(quiz_data['questions'])
    self.level_keys = list(self.levels.keys())

    # State trackers
    self.current_level_idx = 0
    self.current_q_idx     = 0
    self.start_time        = datetime.utcnow()

    self.show_question()

  def show_question(self):
    # All levels done?
    if self.current_level_idx >= len(self.level_keys):
      elapsed = (datetime.utcnow() - self.start_time).seconds
      self.lbl_question.text = "🎉 Vous avez terminé le quiz !"
      self.radio_panel.clear()
      self.lbl_feedback.text = f"Temps total : {elapsed}s"
      return

    lvl = self.level_keys[self.current_level_idx]
    questions = self.levels[lvl]
    qq = questions[self.current_q_idx]

    # Header + feedback
    self.lbl_level.text    = f"Niveau {lvl}"
    self.lbl_question.text = qq['text']
    self.lbl_feedback.text = ""

    # Build RadioButtons dynamically
    self.radio_panel.clear()
    option_h = 30  # px per option
    n = len(qq['options'])
    # Set panel height to auto-fit all buttons (numeric px)
    self.radio_panel.height = n * option_h

    for opt in qq['options']:
      rb = RadioButton(
        text       = opt['text'],
        value      = opt['correct'],
        group_name = "answers"
      )
      rb.correct = opt['correct']

      self.radio_panel.add_component(rb)

  def btn_submit_click(self, **event_args):
    # Grab the selected value
    selected = None
    for rb in self.radio_panel.get_components():
      if rb.selected:
        selected = rb.correct
        break

    if selected is None:
      alert("Veuillez choisir une réponse !")
      return

    # Correct vs. incorrect
    if selected:
      self.lbl_feedback.text = "✅ Correct !"
      self.current_q_idx += 1
      lvl = self.level_keys[self.current_level_idx]
      if self.current_q_idx >= len(self.levels[lvl]):
        self.current_level_idx += 1
        self.current_q_idx = 0
    else:
      self.lbl_feedback.text = "❌ Faux — retour au début du niveau."
      self.current_q_idx = 0

    # Trigger the one-shot timer (interval = 1 s in seconds)
    self.timer_next.interval = 1

  def timer_next_tick(self, **event_args):
    # Auto-disabled since repeating=False; extra safety:
    self.timer_next.interval = 0
    self.show_question()