from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_model import User
from flask_app.models.post_model import Posts

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
    form_data = request.form
    data = {
        "user_id" : session['user_id'],
        "title" : form_data['title'],
        "text_content" : form_data['text_content'],
        "image" : form_data['image'],
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