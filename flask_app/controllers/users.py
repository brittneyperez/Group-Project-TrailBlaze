from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect('/register')

# * REGISTER ----------------

@app.route('/register')
def registration_page():
    return render_template('index.html')

# POST ROUTE -------------------

@app.route('/register/user', methods = ['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/register')
    user_id = User.create_user(request.form)
    if user_id == False:
        flash('Username/Email already exists. Please try again.', 'category7')
        return redirect('/register')
    session['user_id'] = user_id
    session['username'] = request.form['username']
    return redirect('/user/dashboard')

# * LOGIN -------------------

@app.route('/login')
def login_page():
    return render_template('login-page.html')

# POST ROUTE ----------------

@app.route('/login/user', methods = ['POST'])
def login_user():
    user_in_db = User.find_email(request.form)
    if not user_in_db:
        flash('The information entered does not match our records. Please check and try again.', 'category5')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('The information entered does not match our records. Please check and try again.', 'category5')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    session['username'] = user_in_db.username
    print(session['user_id'])
    print(session['username'])
    return redirect('/user/dashboard')

# * HOME --------------------

@app.route('/user/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/login')
    return render_template('dashboard.html')

# * LOGOUT ------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')