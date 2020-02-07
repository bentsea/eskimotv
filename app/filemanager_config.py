from flask_login import current_user
from .models import Permission

def can_edit_files():
    return current_user.can(Permission.WRITE)
