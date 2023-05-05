from flask import render_template, url_for, redirect, flash, request
from market.models import Item, User
from market import app
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", title="Home page")


@app.route("/market",methods=["GET","POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase item logic
        purchased_item = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulation! You purchased {p_item_object.name} for ₹{p_item_object.price}", category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category="danger")
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for("market_page"))


    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, selling_form=selling_form, owned_items=owned_items, title="Market Page")


@app.route("/register", methods=["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")
        return redirect(url_for("market_page"))
    if form.errors != {}: # if there are not error from the validations
        for err_mgs in form.errors.values():
            flash(f"There was an error with creating a user: {err_mgs}", category="danger")
    return render_template("register.html", form=form, title="Register Page")



@app.route("/login", methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Welcome {attempted_user.username} to our market website! We're thrilled to have you here. Happy shopping!", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Username and Password not matched! Please try again", category="danger")
    return render_template("login.html", form=form, title="Login Page")


@app.route("/logout")
def logout_page():
    logout_user()
    flash(f"You have been logged out!", category="success")
    return redirect(url_for("home_page"))

