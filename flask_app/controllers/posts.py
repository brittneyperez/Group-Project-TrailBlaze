from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.post_model import Posts
from flask_app.models.comment_model import Comments

@app.route('/user/create_post')
def create_post():
    if "user_id" not in session:
        return redirect('/')
    return render_template('new-post.html')

@app.route('/user/submit_post', methods=['POST'])
def validate_user_post():
    if "user_id" not in session:
        return redirect('/')
    
    title = request.form['title']
    text_content = request.form['text_content']  # Make sure this matches the name attribute of the textarea field
    image = request.form['image'] if 'image' in request.form else None

    if not Posts.validate_post(request.form):
        return redirect('/user/create_post')
    
    data = {
        "user_id": session['user_id'],
        "title": title,
        "text_content": text_content,
        "image": image,
    }
    Posts.create_post(data)
    return redirect('/user/dashboard')

@app.route('/post/edit/<int:id>')
def edit_post(id):
    # if "user_id" not in session:
    #     return redirect('/')
    post = Posts.one_post({'id' : id})
    return render_template('edit_post.html', posts=[post])

@app.route('/post/edit/validation/<int:id>', methods=['POST'])
def validate_edit(id):
    # if 'user_id' not in session:
    #     return redirect('/')
    if not Posts.validate_post(request.form):
        return redirect(f'/posts/edit/{id}')
    data = {
        'id' :id,
        'title' : request.form['title'],
        'text_content' : request.form['text_content'],
        'image' : request.form['image']
    }
    Posts.update_post(data)
    return redirect('/user/dashboard')

@app.route('/post/delete/<int:id>', methods=['DELETE'])
def delete_one_post(id):
    # if 'user_id' not in session:
    #     return redirect('/')
    Posts.delete_post({'id' : id})
    return redirect('/user/dashboard')

@app.route('/post/<int:post_id>/comments', methods=['GET', 'POST'])
def post_comments(post_id):
    if request.method == 'POST':
        text_content = request.form['text_content']
        # Add the comment to the database using the Comments model
        if not text_content or len(text_content.strip()) < 3:
            flash('Comment must be at least 3 characters long', 'error')
        else:
            Comments.create_comment({
                'user_id': session['user_id'],
                'post_id': post_id,
                'text_content': text_content
            })

    # Get the post and its comments from the database
    post = Posts.one_post({'id': post_id})
    print("Post Data:", post)
    comments = Comments.posts_comments(post_id)
    print("Comments:", comments)
    return render_template('post_comments.html', post=post, comments=comments)


