import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import open_form, alert


def get_current_user():
  return anvil.users.get_user()


def go_to(page_name):
  user = get_current_user()
  if not user:
    alert("You must be logged in to access this page.")
    return

  if not anvil.server.call('user_has_role_for_page', page_name):
    required_role = anvil.server.call('get_required_role_for_page', page_name)
    alert(f"Access denied: You need '{required_role}' privileges to open this page.")
    return

  open_form(page_name)
