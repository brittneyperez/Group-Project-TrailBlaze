from flask_app import app, htmx
from flask import render_template, redirect, request, session, flash, Markup
from flask_app.models.user_model import User
from flask_app.models.post_model import Posts
from flask_app.models.like_model import Like
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#* Welcome Trailblazer!
@app.route('/')
def index():
    return render_template('landing-page.html')

# ! FOR TESTING PURPOSES -- 
@app.route('/dashboard/sample')
def dashboard_test():
    return render_template("dashboard-hardcoded.html")
# ? If design is approved, funtionality will be moved here and is renamed as dashboard.html


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

@app.route('/register/cookie')
def cookie():
   
    return render_template('landing-page.html')


# * LOGIN -------------------

@app.route('/login')
def login_page():
    return render_template('login-page.html')

# POST ROUTE ----------------
@app.route('/login/user', methods = ['POST'])
def login_user():
    user_in_db = User.find_email(request.form)
    
    submission = {
        'sorting': request.form['sorting'],
    }
    if not user_in_db:
        flash('The information entered does not match our records. Please check and try again.', 'category5')
        flash('If you do not have an account, you can register for one  at the below!', 'category5')
        flash(Markup('<a href="/register/cookie" HX-Trigger-After-Settle: document.getElementById("loginBtn").click()>Join the Adventure!</a>'),'category5')

        # return redirect('/login')
        # response = render_template('landing_login_card.html', submission = submission,)
        # response.headers['HX-TRIGGER'] = 'badloginevent'

        return render_template('login-page.html', submission = submission)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('The information entered does not match our records. Please check and try again.', 'category5')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    session['username'] = user_in_db.username
    print(session['user_id'])
    print(session['username'])
    return redirect('/user/dashboard')

@app.route('/reg_request', methods = ['PUT'])
def reg_request():
    return render_template('/partials/landing_signup_card.html')

@app.route('/log_request', methods = ['PUT'])
def log_request():
    return render_template('/partials/landing_login_card.html')


# * HOME --------------------

@app.route('/user/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    posts = Posts.all_posts()
    for post in posts:
        post.like_count = Like.get_like_count_for_post(post.id)
        post.liked_by_user = Like.check_user_liked_post(user_id, post.id)
    return render_template('dashboard.html', posts = posts)

# * LOGOUT ------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')