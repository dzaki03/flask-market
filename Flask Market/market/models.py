from market import db, bcrypt, login_manager
from flask_login import UserMixin
from flask_security import RoleMixin

from flask_admin.contrib.sqla import ModelView



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(length=30), nullable=False, unique=True)
#     description = db.Column(db.String(length=50), nullable=False, unique=True)
#     user
#
#     def __str__(self):
#         return self.name
#
#     # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
#     def __hash__(self):
#         return hash(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    # roles = db.relationship('Role', backref='roles_users', lazy=True)

    @property
    def prettier_budget(self):
        formatted_budget = ""
        reverse_budget = str(self.budget)[::-1]
        for i in range(len(reverse_budget)):
            if ((i + 1) % 3) == 0 and (i + 1) == len(reverse_budget):
                formatted_budget = "".join([reverse_budget[i], formatted_budget])
            elif ((i + 1) % 3) == 0:
                formatted_budget = "".join([',', reverse_budget[i], formatted_budget])
            else:
                formatted_budget = "".join([reverse_budget[i], formatted_budget])
        return f"{formatted_budget}$"
        # if len(str(self.budget)) >= 4:
        #     # return f'{str(self.budget[:-3])},{str(self.budget[-3:])}$'
        #     return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        # else:
        #     return f"{self.budget}$"

    @property
    def password(self):
        return self.password



    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    # name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))



    def __repr__(self):
        return f"Item {self.name}"

    @property
    def prettier_price(self):
        formatted_price = ""
        reverse_budget = str(self.price)[::-1]
        for i in range(len(reverse_budget)):
            if ((i + 1) % 3) == 0 and (i + 1) == len(reverse_budget):
                formatted_price = "".join([reverse_budget[i], formatted_price])
            elif ((i + 1) % 3) == 0:
                formatted_price = "".join([',', reverse_budget[i], formatted_price])
            else:
                formatted_price = "".join([reverse_budget[i], formatted_price])
        return f"{formatted_price}$"

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

# from market import admin
# class ViewAdmin(admin):
#     def __init__(self):
#         self.add_view(ModelView(User, db.session))
#         self.add_view(ModelView(Item, db.session))

