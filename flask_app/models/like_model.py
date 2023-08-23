from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User

class Like:
    my_db = "trailblaze_schema"

    def __init__(self, like_data):
        self.id = like_data['id']
        self.created_at = like_data['created_at']
        self.updated_at = like_data['updated_at']
        self.user_id = like_data['user_id']
        self.post_id = like_data['post_id']
        self.user = None

    @classmethod
    def create_like(cls, data):
        query = "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def delete_like(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def get_likes_by_post(cls, post_id):
        query = "SELECT * FROM likes WHERE post_id = %(post_id)s;"
        results = connectToMySQL(cls.my_db).query_db(query, {"post_id": post_id})
        likes = []
        for result in results:
            likes.append(cls(result))
        return likes

    @classmethod
    def get_like_count_for_post(cls, post_id):
        query = "SELECT COUNT(id) AS like_count FROM likes WHERE post_id = %(post_id)s;"
        data = {"post_id": post_id}
        result = connectToMySQL(cls.my_db).query_db(query, data)
        return result[0]['like_count']

    @classmethod
    def check_user_liked_post(cls, user_id, post_id):
        query = "SELECT id FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        data = {"user_id": user_id, "post_id": post_id}
        result = connectToMySQL(cls.my_db).query_db(query, data)
        return bool(result)  # Return True if the user has liked the post, else False

    @staticmethod
    def validate_like(like_data):
        user_id = like_data['user_id']
        post_id = like_data['post_id']
        
        # Get the post's user ID from the database
        query = "SELECT user_id FROM posts WHERE id = %(post_id)s;"
        result = connectToMySQL(Like.my_db).query_db(query, {"post_id": post_id})
        
        if result and result[0]['user_id'] == user_id:
            flash("You can't like your own post.")
            return False
        
        return True