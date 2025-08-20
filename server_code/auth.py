import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# Define the role hierarchy (lowest to highest)
ROLE_HIERARCHY = ["user", "leader", "editor", "admin"]

def has_required_role(user_role, required_role):
  #Return True if user's role is at least the required role.
  if user_role not in ROLE_HIERARCHY or required_role not in ROLE_HIERARCHY:
    return False
  return ROLE_HIERARCHY.index(user_role) >= ROLE_HIERARCHY.index(required_role)

@anvil.server.callable
def get_required_role_for_page(page_name):
  row = app_tables.page_roles.get(page=page_name)
  if row:
    return row['required_role']
  return "user"  # default minimum

@anvil.server.callable
def user_has_role_for_page(page_name):
  user = anvil.users.get_user()
  if not user:
    return False
  required_role = get_required_role_for_page(page_name)
  user_role = user['role']
  return has_required_role(user_role, required_role)

@anvil.server.callable
def get_current_user():
  return anvil.users.get_user()