from ._anvil_designer import QuizPlayTemplate
from anvil import *
import anvil.users
import anvil.server
from datetime import datetime
import random

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

    self.CORRECT = "Bravo!"
    self.NOTCORRECT = "Essaye encore!"
    self.GAGNE = "Felicitations! Quiz termine en"
    # Setup timer (interval = seconds)
    self.timer_next.interval  = 0

    # Organize questions
    self.levels = group_questions_by_level(quiz_data['questions'])
    self.title = quiz_data['title']
    if not self.levels:
      print("No questions found.")
      return

    self.level_keys       = list(self.levels.keys())
    self.current_level    = self.level_keys[0]
    self.current_level_idx = 0
    self.current_q_idx    = 0
    self.start_time       = datetime.utcnow()

    self.progress_shapes = []
    self.label_title.text =  self.title
    self.show_question()

  def show_question(self):
    if self.current_level_idx >= len(self.level_keys):
      self.complete_quiz()
      return

    self.current_level = self.level_keys[self.current_level_idx]

    if self.current_q_idx == 0:
      self.update_progress_panel()

    questions = self.levels[self.current_level]
    current_q = questions[self.current_q_idx]
    self.update_UI(current_q)

  def update_UI(self, question):
    self.lbl_level.text    = f"Niveau {self.current_level} / {len(self.level_keys)}"
    self.lbl_question.text = question['text']
    self.lbl_feedback.text = ""
    
    ## butoons options
    self.options_panel.clear() 
    opts = question['options'].copy()
    random.shuffle(opts)

    for opt in opts:
      btn = Button(
        text    = opt['text'],
        role    = "tonal-button",      # you can pick "primary", "info", etc.
        width   = "full-width",         # full-width, or whatever you need
        align   = "center",
        background= "theme:Primary Container",
        font_size= 32
      )
      # stash the correctness flag
      btn.correct = opt['correct']
      btn.set_event_handler('click', self.answer_click)
      self.options_panel.add_component(btn)
      
  def update_progress_panel(self):
    # remove old shapes…
      self.progress_panel.clear()
      self.progress_shapes = []

      # …then add one circle per question in this level
      questions = self.levels[self.current_level]
      for _ in questions:
        btn = Button(
          text=" ",
          font_size = "50",
          role="btn_progress",
          align="center",
          bold= True,
          spacing_above = "none",
          spacing_below = "none",
          enabled = False,
          foreground = "#777777",
          icon = "fa:check-circle"
        )
             
        self.progress_panel.add_component(btn)
        self.progress_shapes.append(btn)

  def answer_click(self, **event_args):
    btn = event_args['sender']
    # Optional: clear previous highlights
    for sibling in self.options_panel.get_components():
      sibling.role = "default"
      sibling.enabled = False
    # Highlight the clicked button
    btn.role = "primary"
    if btn.correct:
      self.feedback_ok()
    else:
      self.feedback_ko()
    
    self.timer_next.interval  = 1
    btn.enabled= True

  def timer_next_tick(self, **event_args):
    self.timer_next.interval  = 0
    self.show_question()

  def feedback_ok(self):
    self.lbl_feedback.text = self.CORRECT
    self.lbl_feedback.foreground= "Green"
    self.progress_shapes[self.current_q_idx].foreground = "green"
    self.progress_shapes[self.current_q_idx].icon = "fa:check-circle"

    self.current_q_idx += 1
    questions = self.levels[self.current_level]
    if self.current_q_idx >= len(questions):
      self.current_level_idx += 1
      self.current_q_idx = 0

  def feedback_ko(self):
    self.lbl_feedback.text = self.NOTCORRECT
    self.lbl_feedback.foreground= "Red"
    for btn in self.progress_shapes:
       btn.icon = "fa:check-circle"
       btn.foreground = "#777"

    self.current_q_idx = 0
     
  def complete_quiz(self):
    elapsed = (datetime.utcnow() - self.start_time).seconds
    self.lbl_question.text   = f" {self.GAGNE} {elapsed}s"
    self.lbl_feedback.text   = ""
    self.options_panel.clear() 
    self.lbl_level.text = ""
    self.progress_panel.clear()
    self.progress_shapes = []

  def link_quiz_click(self, **event_args):
    open_form("QuizHome")
