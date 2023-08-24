from flask import Flask
from flask_bcrypt import Bcrypt
from flask_htmx import HTMX


app = Flask(__name__)
bcrypt = Bcrypt(app)
htmx = HTMX(app)
app.secret_key = 'shhhhhh'