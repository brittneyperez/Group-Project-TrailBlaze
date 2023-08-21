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
# * HOME --------------------
# * LOGOUT ------------------



# @app.route('/user/register', methods=['POST'])
# def register_user():
#         if not User.registration_valid(request.form):
#             return redirect('/authenticate')

#         print('***~ in REGISTER route ~***')
#         user_id = User.save(request.form)
#         session['user_id'] = user_id
#         return redirect('/user/dashboard')

# @app.route('/user/login', methods=['POST'])
# def login_user():
#     user = User.login_valid(request.form)
    
#     if not user:
#         return redirect('/authenticate')
    
#     session['user_id'] = user.id
#     print('***~ in LOGIN route ~***')
#     return redirect('/user/dashboard')

# # ERROR 404: URL NOT FOUND  - I already checked the URLS in redirect, dunno what would be causing this error
# @app.route('/user/logout')
# def logout_user():
#     if 'user_id' in session:
#         session.pop('user_id')
#     return redirect('/authenticate')