from market.routes import current_user
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask import session, abort
from flask import sessions

class SecureModelView(ModelView):
    # @login_required

    def is_accessible(self):
        # print(current_user.id)
        try:
            if current_user.id == 6:
                return True
            else:
                abort(403)
        except AttributeError as error:
            abort(403)
            print(error)
        # else:


            # if current_user == 5:
            # print(5 in session)

        # else:
        #     print("adfadf")