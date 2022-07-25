from market import app
from flask import render_template, redirect, url_for, flash, request, session
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
from market import admin
from flask_admin.contrib.sqla import  ModelView

@app.route("/")  # using css and html
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    print(current_user )
    print(session['logged_in'])
    print(session['logged_in'])
    print(session['logged_in'])
    if request.method == "POST":

        #Purchase Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.prettier_price}", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')

        #Sell Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market",
                      category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')


        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the about page of {username}</h1>'

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    #This is method for validate when we click submit
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account crated successfully!! You are {user_to_create.username}", category='success')
        #redirect is flask function that redirect to url that we want to choose
        session["logged_in"] = True
        return redirect(url_for('market_page'))
    if form.errors != {}: #if there are errors from the validations
        for err_msg in form.errors.values():
            # print(type(err_msg))
            flash(f'There was an error: {err_msg}', category='danger')


    #render_template is function that copy page from html template that work with jinja2
    # We can add variable from python code to html page
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
            # session["loggeds_in"] = True
            session['logged_in'] = f"{attempted_user}"

            return redirect(url_for('market_page'))
        else:
            flash("Username and password are not match! Please try again", category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You Hace been logged out!!", category='info')
    return redirect(url_for('home_page'))

@app.route('/aa')
def admin_page():
    # admin.add_view(ModelView(Item, db.session))
    # admin.add_view(ModelView(User, db.session))
    return render_template('admin.html')