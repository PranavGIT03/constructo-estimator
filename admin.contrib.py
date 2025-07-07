from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from flask_login import current_user

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == "admin@example.com"
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
