from datetime import timedelta
from os import environ

# django axes config
AXES_ENABLED = False if environ.get('AXES_ENABLED') == '0' else True
AXES_LOCKOUT_CALLABLE = "users.views.user_lockout.lockout"
AXES_COOLOFF_TIME = timedelta(minutes=15)
AXES_FAILURE_LIMIT = 5
AXES_LOCKOUT_PARAMETERS = [["username"]]
AXES_RESET_ON_SUCCESS = True
