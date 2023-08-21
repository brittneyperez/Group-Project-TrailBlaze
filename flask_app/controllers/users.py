from flask_app import app
from flask import render_template, redirect, request, session
# from flask_app.models.user import User
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt


@app.route('/')
def index():
    return redirect('/register')

# * REGISTER ----------------

@app.route('/register')
def registration_page():
    # if 'user_id' in session:
    #     return redirect('/u/dashboard')
    return render_template('index.html')

# POST ROUTE


# * LOGIN -------------------

@app.route('/login')
def login_page():
    # if 'user_id' in session:
    #     return redirect('/u/dashboard')
    return render_template('login-page.html')

# POST ROUTE

# HOME --------------------
# * LOGOUT ------------------
