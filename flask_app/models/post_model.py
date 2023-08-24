from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User


class Posts:
    my_db = "trailblaze_schemaV2"
    def __init__(self, post_data):
        self.id = post_data['id']
        self.title = post_data['title']
        self.text_content = post_data['text_content']
        self.image = post_data['image']                         #Not really sure if this is correct
        self.created_at = post_data['created_at']
        self.updated_at = post_data['updated_at']
        self.user_id = post_data['user_id']
        self.creator = None

    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (title, text_content, image, user_id) VALUES (%(title)s, %(text_content)s, %(image)s, %(user_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def one_post(cls, data):
        query = "SELECT * FROM posts WHERE posts.id = %(id)s;"
        result = connectToMySQL(cls.my_db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def all_posts(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id"
        result = connectToMySQL(cls.my_db).query_db(query)
        if not result:
            return []
        every_post = []
        for row in result:
            single_post = cls(row)
            user_data = {
                "id": row['users.id'],
                "username": row['username'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            single_post.creator = User(user_data)
            every_post.append(single_post)
        return every_post

    @classmethod
    def update_post(cls, data):
        query = "UPDATE posts SET title = %(title)s, text_content = %(text_content)s, image = %(image)s WHERE posts.id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE posts.id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @staticmethod
    def validate_post(post_data):
        is_valid = True
        if len(post_data['title']) < 3:
            flash("Title must be at least 3 characters")
            is_valid = False
        if len(post_data['text_content']) < 5:
            flash("Text content must be at least 5 characters")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_image(post_filename):
        is_valid = True
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        if post_filename.rsplit('.',1)[1].lower() not in ALLOWED_EXTENSIONS:
            flash('Incorrect file type, plase select png, jpg, jpeg, or gif file')
            is_valid = False
        return is_valid
