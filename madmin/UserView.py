from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, \
UserMixin, RoleMixin, login_required, current_user

class HashView(ModelView):

    can_create = False
    can_edit = False
    can_delete = False

    def is_accessible(self):
        print(current_user)
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        print(current_user)
        print(self.is_accessible)
        if not self.is_accessible():
            print("current_user")
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
