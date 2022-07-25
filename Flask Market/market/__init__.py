from flask import Flask, render_template
from flask_sqlalchemy import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from models import Item, User

import flask_wtf
import wtforms




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'cf14e2b2ec9c41fecb86fcc9'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
# import routes
# from market.models import ViewAdmin
from market.models import Item, User
admin = Admin(app)
# from market.models import ViewAdmin
from market.administrator import SecureModelView

admin.add_view(SecureModelView(Item, db.session))
print(current_user)

















from market import routes
from market.models import db
# import PurchaseItemForm
# from market.forms import PurchaseItemForm
# a = PurchaseItemForm()
# # print(a['submit'])

# from market.models import Item
# item = Item(name="Laptop ASUS X411M",
#     price=500,
#     barcode="124353646461",
#     description="This is Laptop ASUS with Intel I7",
#
#     )
# db.session.add(item)
# db.session.commit()

from market.models import User, Item


#NGEBUAT KELAS ITEM DATABASE
        # i2 = Item(name="Laptop", price=250, barcode='123456789013', description="this is laptop")

#POST DATA KE DATABASE.DB
        # db.session.add(i2) -> MASUKIN VARIABEL DB NYA
        # db.session.commit()


# db.session.rollback()

# CARA CEK ISI DATA BASE
        # print(User.query.all())



# item1 = Item.query.filter_by(name='Iphon 10').first()
# db.session.rollback()
# item1.owner = User.query.filter_by(username='halo').first().id
#
# i = Item.query.filter_by(name='Iphon 10').first()
#
# print(i.owned_user)

# db.sess
# db.session.add(item1)
# db.session.commit()


# print(item1.owner)
# print(item1)
# print(Item.query.all())
