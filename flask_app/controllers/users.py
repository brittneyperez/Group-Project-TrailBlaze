from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_model import User
from flask_app.models.post_model import Posts
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect('/register')

# * REGISTER ----------------

@app.route('/register')
def registration_page():
    # if 'user_id' in session:
    #     return redirect('/dashboard')
    return render_template('index.html')

# POST ROUTE -------------------

@app.route('/register/user', methods = ['POST'])
def create_user():
    if not User.validate_user(request.form):
        print('FAILED USER VALIDATION')
        return redirect('/register')
    user_id = User.create_user(request.form)
    session['user_id'] = user_id
    return redirect('/user/dashboard')

# * LOGIN -------------------

@app.route('/login')
def login_page():
    # if 'user_id' in session:
    #     return redirect('/u/dashboard')
    return render_template('login-page.html')

# POST ROUTE ----------------

@app.route('/login/user', methods = ['POST'])
def login_user():
    user_in_db = User.find_email(request.form)
    if not user_in_db:
        print('FAILED LOGIN VALIDATION')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        print('FAILED HASH PASSWORD')
        return redirect('/login')
    return redirect('/user/dashboard')

# * HOME --------------------

@app.route('/user/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect('/login')
    posts = Posts.all_posts()
    return render_template('dashboard.html', posts = posts)

# * LOGOUT ------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')