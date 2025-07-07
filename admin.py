from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from flask_login import current_user

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == "admin@example.com"
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

def setup_admin(app, db):
    from user_schema import User
    from material_schema import Material
    from estimation_schema import Estimation
    
    admin = Admin(app, name='Constructo Admin', template_mode='bootstrap4')
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Material, db.session))
    admin.add_view(AdminModelView(Estimation, db.session))
    return admin
