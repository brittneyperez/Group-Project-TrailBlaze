from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    my_db = "trailblazer"
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.about_me = data['about_me']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, form_data):
        hash_pass = bcrypt.generate_password_hash(form_data['password'])
        user_data = {
            'username': form_data['username'],
            'email': form_data['email'],
            'about_me': form_data['about_me'],
            'password': hash_pass
        }
        query = "INSERT INTO users (username, email, about_me, password) VALUES (%(username)s, %(email)s, %(about_me)s, %(password)s);"
        result = connectToMySQL(cls.my_db).query_db(query, user_data)
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