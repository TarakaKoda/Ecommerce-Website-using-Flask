from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "e88f4c0d5e3eb689ced253da"
db = SQLAlchemy(app)

from market import routes