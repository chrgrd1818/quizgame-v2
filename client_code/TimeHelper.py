import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#

from datetime import datetime


class TimeHelper:
  def __init__(self):
    self.start_time = datetime.utcnow()

  def get_elapsed_seconds(self):
    """Returns elapsed time in seconds since start_time."""
    elapsed = (datetime.utcnow() - self.start_time).seconds
    return elapsed

  @staticmethod
  def seconds_to_min_sec(seconds):
    """Converts seconds to MM:SS format."""
    if not isinstance(seconds, int) or seconds is None or seconds < 0:
      return "-:-"  # Valeur invalide ou nulle → retourne 00:00
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02}:{secs:02}"

  @staticmethod
  def min_sec_to_seconds(min_sec_str):
    """Converts MM:SS format to total seconds."""
    try:
      minutes, seconds = map(int, min_sec_str.split(":"))
      return minutes * 60 + seconds
    except ValueError:
      raise ValueError("Invalid format. Use MM:SS (e.g., '03:45')")

    """
    min_sec_format = helper.seconds_to_min_sec(elapsed_sec)
    print("Elapsed time (MM:SS):", min_sec_format)

    back_to_seconds = helper.min_sec_to_seconds(min_sec_format)
    print("Converted back to seconds:", back_to_seconds)
    """