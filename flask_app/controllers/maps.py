from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.map_model import Map, Marker
from flask_app.models.user_model import User
import googlemaps

key = 'AIzaSyC3wzK_IRzTkYzszfImdCmdYeU02Mbwr4A' # we gotta hide this somehow

@app.route('/maps')
def initmaps():
    #get user location through geolocation
    client = googlemaps.Client(key)
    geocode_result = client.geolocate()
    print(geocode_result)
    print(geocode_result['location'])
    data = {
        'lat': geocode_result['location']['lat'],
        'lng': geocode_result['location']['lng']
    }
    print(data)
    return render_template('maps.html', key=key, data=data)

@app.route('/maps/<int:map_id>')
def show_map(map_id):
    pass

@app.route('/newmap')
def create_map():
    print(session['user_id'])
    user_id = session['user_id']
    # if 'user_id' not in session:
    #     return redirect('/')
    existing_maps = Map.get_all_maps_by_user(user_id)
    current_user = User.single_user(user_id)
    print('before user')
    print(current_user)
    print('after user')
    # if existing_maps:
    #     name = "{}'s Map #{}".format(current_user.username, len(existing_maps) + 1)
    # else:
    #     name = "{}'s Map #1".format(current_user.username)
    # data = {
    #     'name': name,
    #     'user_id': user_id,
    # }
    # new_map = Map.create_map(data)
    # username = User.single_user(user_id).username
    return print('new map')
    return redirect(f'/maps/{username}/{new_map.id}')

@app.route('/maps/<string:username>/<int:map_id>')
def show_user_map(username, map_id):
    _map = Map.get_map_by_id({'id': map_id})
    client = googlemaps.Client(key)
    if len(_map.markers) == 0:
        geocode_result = client.geolocate()
        print(geocode_result)
        print(geocode_result['location'])
        data = {
            'lat': geocode_result['location']['lat'],
            'lng': geocode_result['location']['lng'],
        }
        return render_template('newmap.html', key=key, data=data)
    else:
        return render_template('map.html', key=key, map=_map)