from ._anvil_designer import QuizPlayTemplate
from anvil import *
import anvil.server
from datetime import datetime

def group_questions_by_level(questions):
  levels = {}
  for q in questions:
    lvl = q['difficultyLevel']
    levels.setdefault(lvl, []).append(q)
  for lvl in levels:
    levels[lvl].sort(key=lambda q: q['id'])
  return dict(sorted(levels.items()))

class QuizPlay(QuizPlayTemplate):
  def __init__(self, quiz_data, **properties):
    self.init_components(**properties)

    # Setup timer (interval = seconds)
    self.timer_next.interval  = 0

    # Organize questions
    self.levels = group_questions_by_level(quiz_data['questions'])
    if not self.levels:
      print("No questions found.")
      return

    self.level_keys       = list(self.levels.keys())
    self.current_level    = self.level_keys[0]
    self.current_level_idx = 0
    self.current_q_idx    = 0
    self.start_time       = datetime.utcnow()

    self.show_question()

  def show_question(self):
    if self.current_level_idx >= len(self.level_keys):
      self.complete_quiz()
      return

    self.current_level = self.level_keys[self.current_level_idx]
    questions = self.levels[self.current_level]
    current_q = questions[self.current_q_idx]
    self.update_UI(current_q)

  def update_UI(self, question):
    self.lbl_level.text    = f"Niveau {self.current_level}"
    self.lbl_question.text = question['text']
    self.lbl_feedback.text = ""
    self.radio_panel.clear()

    option_h = 30
    self.radio_panel.height = len(question['options']) * option_h

    for opt in question['options']:
      rb = RadioButton(
        text       = opt['text'],
        group_name = "answers"
      )
      rb.correct = opt['correct']
      self.radio_panel.add_component(rb)

  def btn_submit_click(self, **event_args):
    selected = next(
      (rb.correct for rb in self.radio_panel.get_components() if rb.selected), None
    )
    if selected is None:
      return

    if selected:
      self.feedback_ok()
    else:
      self.feedback_ko()

    self.timer_next.interval  = 1

  def timer_next_tick(self, **event_args):
    self.timer_next.interval  = 0
    self.show_question()

  def feedback_ok(self):
    self.lbl_feedback.text = "✅ Correct !"
    self.current_q_idx += 1
    questions = self.levels[self.current_level]
    if self.current_q_idx >= len(questions):
      self.current_level_idx += 1
      self.current_q_idx = 0

  def feedback_ko(self):
    self.lbl_feedback.text = "❌ Faux — retour au début du niveau."
    self.current_q_idx = 0
     
  def complete_quiz(self):
    elapsed = (datetime.utcnow() - self.start_time).seconds
    self.lbl_question.text   = "🎉 Vous avez terminé le quiz !"
    self.lbl_feedback.text   = f"Temps total : {elapsed}s"
    self.radio_panel.clear()
    self.btn_submit.visible = False
     self.lbl_level.text = ""