from flask import render_template, redirect, flash, request, session
from flask_app.models.user_model import User
from flask_app.models.post_model import Posts
from flask_app.models.like_model import Like
from flask_app import app

@app.route("/like/<int:post_id>", methods=["POST"])
def create_like(post_id):
    # Make sure the user is logged in
    if not 'user_id' in session:
        flash("You must be logged in to like a post.")
        return redirect("/user/dashboard")
    
    # Check if the user has already liked the post
    user_id = session['user_id']
    existing_like = Like.check_user_liked_post(user_id, post_id)
    if existing_like:
        flash("You have already liked this post.")
    else:
        like_data = {
            "user_id": user_id,
            "post_id": post_id
        }
        
        # Validate the like
        if not Like.validate_like(like_data):
            flash("You can't like your own post.")
        else:
            Like.create_like(like_data)
            flash("Post liked successfully!")
    
    return redirect("/user/dashboard")


@app.route("/unlike/<int:post_id>", methods=["POST"])
def delete_like(post_id):
    # Make sure the user is logged in
    if not 'user_id' in session:
        flash("You must be logged in to unlike a post.")
        return redirect("/user/dashboard")
    
    # Delete like
    like_data = {
        "user_id": session['user_id'],
        "post_id": post_id
    }
    Like.delete_like(like_data)
    flash("Post unliked successfully!")
    
    return redirect("/user/dashboard")
