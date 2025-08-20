
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def get_current_user():
  """Return the currently logged-in user row, or None if no user."""
  return anvil.users.get_user()

@anvil.server.callable
def user_has_role(role):
  """Return True if the current user has the given role."""
  user = anvil.users.get_user()
  if user is None:
    return False
    # Assume user roles are stored in a column called 'role' in the Users table
    # You can adjust this as required
  return user['role'] == role

@anvil.server.callable
def require_role(role):
  """Raise error if current user does not have the given role."""
  user = anvil.users.get_user()
  if not user or user['role'] != role:
    raise anvil.server.PermissionDenied("Access denied: missing required role.")
  return True