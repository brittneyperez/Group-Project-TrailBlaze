from flask import redirect, flash, session
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
    like_data = {
        "user_id": user_id,
        "post_id": post_id
    }
    Like.create_like(like_data)

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
    return redirect("/user/dashboard")
