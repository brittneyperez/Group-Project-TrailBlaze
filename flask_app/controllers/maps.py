from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.map_model import Map, Marker
from flask_app.models.user_model import User

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/maps')
def initmaps():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({'id': session['user_id']})
    maps = Map.get_all_maps_by_user({'user_id': session['user_id']})
    return render_template('maps.html', user=user, maps=maps)

@app.route('/maps/<int:map_id>')
def show_map(map_id):
    pass

@app.route('/maps/create', methods=['POST'])
def create_map():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'name': request.form['name'],
        'user_id': session['user_id']
    }
    Map.create_map(data)
    return redirect('/maps')
