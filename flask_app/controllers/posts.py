from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.post_model import Posts
from flask_app.models.comment_model import Comments
from werkzeug.utils import secure_filename
import uuid as uuid
import os

@app.route('/user/create_post')
def create_post():
    if "user_id" not in session:
        return redirect('/')
    return render_template('new-post.html')

@app.route('/user/submit_post', methods=['POST'])
def validate_user_post():
    if "user_id" not in session:
        return redirect('/')

    if not Posts.validate_post(request.form):
        return redirect('/user/create_post')

    # print('REQUEST FILES',request.files['image'])
    post_pic = request.files['image']
    post_filename = secure_filename(post_pic.filename)
    print('POST FILENAME',post_filename)
    if post_filename != "":
        print('MADE IT')
        if not Posts.validate_image(post_filename):
            print('FAILED IMAGE VALIDATION')
            # flash('File upload failed, please try again')
            return redirect('/user/create_post')
        pic_name = str(uuid.uuid1()) + "_" + post_filename
        print(pic_name)
        app_root = os.path.dirname(os.path.abspath(__file__))
        trim_app_root = app_root.split("controllers")
    #     print(trim_app_root)

        UPLOAD_FOLDER = os.path.join(trim_app_root[0], 'static', 'post_imgs')
        post_pic.save(os.path.join(UPLOAD_FOLDER, pic_name))
        post_pic = pic_name

        title = request.form['title']
        text_content = request.form['text_content']  # Make sure this matches the name attribute of the textarea field
        image = request.files['image'] if 'image' in request.files else None
    
        form_data = request.form
        data = {
            "user_id" : session['user_id'],
            "title" : form_data['title'],
            "text_content" : form_data['text_content'],
            "image" : pic_name
        }
    else:
        form_data = request.form
        data = {
            "user_id" : session['user_id'],
            "title" : form_data['title'],
            "text_content" : form_data['text_content'],
            "image" : None
        }

    print('DATA',data)
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

@app.route('/post/delete/<int:id>', methods=['POST', 'GET'])
def delete_one_post(id):
    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')
        Posts.delete_post({'id': id})
        return redirect('/user/dashboard')
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


