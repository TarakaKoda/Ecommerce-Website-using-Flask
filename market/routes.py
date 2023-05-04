from flask import render_template, url_for, redirect
from market.models import Item, User
from market import app
from market.forms import RegisterForm
from market import db

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", title="Home page")


@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items, title="Market Page")


@app.route("/register", methods=["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("market_page"))
    if form.errors != {}: # if there are not error from the validations
        for err_mgs in form.errors.values():
            print(f"There was an error with creating a user: {err_mgs}")
    return render_template("register.html", form=form, title="Register Page")



