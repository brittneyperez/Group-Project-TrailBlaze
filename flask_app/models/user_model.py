from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')
USERNAME_REGEX = re.compile(r'^[A-Za-z][A-Za-z0-9_]{4,20}$')

class User:
    my_db = "trailblaze_schema"
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        # self.about_me = data['about_me']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, form_data):
        print('CREATE USER FORM DATA', form_data) 
        hash_pass = bcrypt.generate_password_hash(form_data['password'])
        user_data = {
            'username': form_data['username'],
            'email': form_data['email'],
            'password': hash_pass
        }
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        result = connectToMySQL(cls.my_db).query_db(query, user_data)
        print('----RESULT----',result)
        return result

    @classmethod
    def all_users(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(cls.my_db).query_db(query)
        if result:
            user_object = []
            for record in result:
                single_user = cls(record)
                user_object.append(single_user)
            return user_object
        else:
            return None

    @classmethod
    def single_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.my_db).query_db(query, data)
        if result:
            one_user = cls(result[0])
            return one_user
        else:
            return False

    @classmethod
    def find_email(cls, form_data):
        print('LOGIN FORM DATA',form_data)
        if len(form_data['username']) < 1 or len(form_data['email']) < 1 or len(form_data['password']) < 1:
            flash('Please fill out email, username, and password', 'category6')
            return False
        if not PASSWORD_REGEX.match(form_data['password']):
            flash('The email and password entered does not match our records.', 'category7')
            return False
        data = {
            'email' : form_data['email'],
            'username' : form_data['username']
        }
        print(data)
        query = "SELECT * FROM users WHERE email = %(email)s AND username = %(username)s;"
        result = connectToMySQL(cls.my_db).query_db(query, data)
        if len(result) < 1:
            flash('The email and password entered does not match our records. Please check and try agian.', 'category5')
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if form_data['password'] != form_data['confirm']:
            flash('Please ensure password and confimation match', 'category1')
            print('PASSWORD AND CONFIRMATION DOES NOT MATCH')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash('Enter in the format: name@example.com', 'category2')
            print('FAILED EMAIL REGEX')
            is_valid = False
        if not PASSWORD_REGEX.match(form_data['password']):
            flash(
                '''Your password needs to include:
                at least one number,
                one uppercase and/or lowercase letter,
                one special character,
                is at least 6 characters long''', 'category3')
            print('FAILED PASSWORD REGEX')
            is_valid = False
        if not USERNAME_REGEX.match(form_data['username']):
            flash(
                '''Your username needs to:
                start with a letter,
                contain at least one number,
                can contain an underscore,
                is at least 4 characters long''', 'category4')
            print('FAILED USERNAME REGEX')
            is_valid = False
        return is_valid