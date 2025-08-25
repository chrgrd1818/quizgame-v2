from ._anvil_designer import QuizPlay2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as qt
from anvil.tables import app_tables
from datetime import datetime
import random

from ..router import go_to, get_current_user
from ..ChronoHelper import ChronoHelper

# --- Utility Functions ---
def get_image_path(has_picts, file, question_id, img_folder, img_default):
  if not has_picts:
    return img_default
  img_path = f"{file}__{question_id}"
  return f"{img_folder}/{file}/{img_path}.jpg"

def get_question(levels, level_idx, q_idx, level_keys):
  current_level = level_keys[level_idx]
  questions = levels[current_level]
  return questions[q_idx]

# --- Main Class ---
class QuizPlay2(QuizPlay2Template):
  # --- Initialization ---
  def __init__(self, quiz_load, **properties):
    self.init_components(**properties)
    # User and Quiz Data
    self.user = get_current_user()
    self.quiz_data = quiz_load
    self.title = self.quiz_data['Title']
    self.file = self.quiz_data['File']
    self.quiz = self.quiz_data['Quiz']
    self.hasPicts = self.quiz_data['Quiz']['HasPicts']
    self.levels = {int(k): v for k, v in self.quiz_data['QuizDictionary'].items()} if self.quiz_data['QuizDictionary'] else {}
    self.level_keys = sorted(self.levels.keys())
    self.progress_shapes = []

    # Constants/UI Strings
    self.CORRECT = "OUI, Bravo !"
    self.NOTCORRECT = "NON, Essaye encore !"
    self.GAGNE = "Felicitations! Quiz terminé en"
    self.NEW_RECORD = "Nouveau record personel !"
    self.IMG_DEFAULT = "_/theme/dummy_img.jpg"
    self.IMG_FOLDER = "_/theme/Picts"

    # Chrono Setup
    self.chrono = ChronoHelper()
    self.timer_chrono.interval = 0
    self.timer_next.interval = 0

    # UI Initial State
    self.lbl_title.text =  self.title
    self.panel_quiz.visible = True
    self._reset_ui()

  def _reset_ui(self):
    """Initial state before quiz starts or when restarting/completing."""
    self.panel_play.visible = False
    self.panel_doafter.visible = False
    self.panel_alert.visible = True
    self.image_question.visible = False
    self.lbl_chrono.text = "00:00"
    self.progress_panel.clear()
    self.progress_shapes = []
    self.lbl_level.text = ""
    self.lbl_feedback.text = ""
    self.lbl_question.text = ""
    self.options_panel.clear()
    self.panel_quiz.border = "10px solid #FFFFFF"
    self.lbl_question.font_size = 24
    self.timer_chrono.interval = 0
    self.timer_next.interval = 0
    print("Ui reset")

  # --- Game Start/Restart ---
  def button_start_click(self, **event_args):
    self.start_game()

  def start_game(self):
    print("start")
    self.panel_alert.visible = False
    self.panel_quiz.visible = True
    self.panel_play.visible = True
    self.image_question.visible = True
    self.panel_doafter.visible = False

    self.chrono.start()
    self.timer_chrono.interval = 1

    self.current_level_idx = 0
    self.current_q_idx    = 0
    self.show_question()

  def button_refaire_click(self, **event_args):
    """Restart this quiz (play again)."""
    self._reset_ui()
    self.start_game()

  # --- UI/Timer Event Handlers ---
  def timer_chrono_tick(self, **event_args):
    elapsed = self.chrono.get_elapsed()
    self.lbl_chrono.text = self.chrono.seconds_to_min_sec(elapsed)

  def timer_next_tick(self, **event_args):
    self.timer_next.interval = 0
    self.show_question()

  # --- Question/Option Display ---
  def show_question(self):
    if self.current_level_idx >= len(self.level_keys):
      self.complete_quiz()
      return
    self.current_level = self.level_keys[self.current_level_idx]
    if self.current_q_idx == 0:
      self.update_progress_panel()
    questions = self.levels[self.current_level]
    current_q = questions[self.current_q_idx]
    self.update_UI(current_q, self.current_q_idx)

  def update_UI(self, question, q_idx):
    self.lbl_question.text = ""
    self.lbl_feedback.text = ""
    self.panel_quiz.border = "10px solid #FFFFFF"
        
    self.lbl_level.text = f"Niveau {self.current_level} / {len(self.level_keys)}"
    self.lbl_question.text = question['text']
    
    # Set question image
    self.image_question.source = get_image_path(self.hasPicts, self.file, question['id'], self.IMG_FOLDER, self.IMG_DEFAULT)
    self.image_question.visible = True

    # Option buttons
    self.options_panel.clear() 
    opts = question['options'].copy()
    random.shuffle(opts)
    for opt in opts:
      btn = Button(
        text=opt['text'],
        role="tonal-button",      
        width="full-width",    
        align="center",
        background="theme:Primary Container",
        font_size=20
      )
      btn.correct = opt['correct']
      btn.set_event_handler('click', self.answer_click)
      self.options_panel.add_component(btn)

  def update_progress_panel(self):
    self.progress_panel.clear()
    self.progress_shapes = []
    questions = self.levels[self.current_level]
    for _ in questions:
      btn = Button(
        text=" ",
        font_size=18,
        role="btn_progress",
        align="center",
        bold=True,
        spacing_above="none",
        spacing_below="none",
        enabled=False,
        foreground="#777777",
        icon="fa:check-circle"
      )
      self.progress_panel.add_component(btn)
      self.progress_shapes.append(btn)

  # --- Answer Handling ---
  def answer_click(self, **event_args):
    btn = event_args['sender']
    for sibling in self.options_panel.get_components():
      sibling.role = "default"
      sibling.enabled = False
    btn.role = "primary"
    if btn.correct:
      self.feedback_ok()
    else:
      self.feedback_ko()
    self.timer_next.interval = 0.2
    btn.enabled = True

  def feedback_ok(self):
    self.lbl_feedback.text = self.CORRECT
    self.lbl_feedback.foreground = "Green"
    self.panel_quiz.border = "10px Solid Green"
    self.progress_shapes[self.current_q_idx].foreground = "green"
    self.progress_shapes[self.current_q_idx].icon = "fa:check-circle"
    self.current_q_idx += 1
    questions = self.levels[self.current_level]
    if self.current_q_idx >= len(questions):
      self.current_level_idx += 1
      self.current_q_idx = 0

  def feedback_ko(self):
    self.lbl_feedback.text = self.NOTCORRECT
    self.lbl_feedback.foreground = "Red"
    self.panel_quiz.border = "10px Solid Red"
    for btn in self.progress_shapes:
      btn.icon = "fa:check-circle"
      btn.foreground = "#777"
    self.current_q_idx = 0

  # --- Completion/Save ---
  def complete_quiz(self):
    self.chrono.stop()
    self._reset_ui()
    self.panel_doafter.visible = True
    self.panel_alert.visible = False
    
    elapsed = self.chrono.get_elapsed()
    min_sec_format = self.chrono.seconds_to_min_sec(elapsed)
    self.lbl_chrono.text =  min_sec_format
    self.label_result.text = f" {self.GAGNE} {min_sec_format}s"
    self.save_quiz(elapsed)
    print("end")

  def save_quiz(self, elapsed):
    data = {
      's_quiz': self.quiz,
      's_time': int(round(elapsed)),
      's_user': self.user,
      's-score': len(self.level_keys)
    }
    saving = anvil.server.call("set_score_quiz", data)
    if saving and saving['status'] == "new_record":
      self.label_result.text += "\n" + self.NEW_RECORD

  # --- Navigation Buttons ---
  def link_quiz_click(self, **event_args):
    open_form("QuizHome")

  def button_scorepage_click(self, **event_args):
    open_form("Board")
