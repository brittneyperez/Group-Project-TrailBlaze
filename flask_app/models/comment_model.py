from flask_app import Flask
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User
from flask_app.models.post_model import Posts

class Comments:
    my_db = "trailblazer"
    def __init__(self, comment_data):
        self.id = comment_data['id']
        self.text_content = comment_data['text_content']
        self.created_at = comment_data['created_at']
        self.updated_at = comment_data['updated_at']
        self.user_id = comment_data['user_id']
        self.post_id = comment_data['post_id']
        self.creator = None

    @classmethod
    def create_comment(cls, data):
        query = "INSERT INTO comments (text_content, user_id, post_id) VALUES (%(text_content)s, %(user_id)s, %(post_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def one_comment(cls, data):
        query = "SELECT * FROM comments WHERE comments.id = %(id)s;"
        results = connectToMySQL(cls.my_db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def users_comments(cls):
        query = "SELECT * FROM comments JOIN users ON comments.user_id = users.id;"
        result = connectToMySQL(cls.my_db).query_db(query)
        if not result:
            return []
        comments = []
        for row in result:
            one_comment = cls(row)
            user_data = {
                "id": row['users.id'],
                "username": row['username'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            one_comment.creator = User(user_data)
            comments.append(one_comment)
        return comments

    @classmethod
    def posts_comments(cls):
        query = "SELECT * FROM comments JOIN posts ON comments.post_id = posts.id;"
        result = connectToMySQL(cls.my_db).query_db(query)
        if not result:
            return []
        post_comment = []
        for row in result:
            comment_from_post = cls(row)
            post_data = {
                "id": row['posts.id'],
                "title": row['title'],
                "text_content": row['text_content'],
                "image": row['image'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            comment_from_post.creator = Posts(post_data)
            post_comment.append(comment_from_post)
        return post_comment

    @classmethod
    def update_comment(cls, data):
        query = "UPDATE comments SET text_content = %(text_content)s WHERE comments.id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE comments.id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query, data)