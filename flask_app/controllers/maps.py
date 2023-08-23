from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.map_model import Map, Marker
from flask_app.models.user_model import User
import googlemaps

key = 'AIzaSyC3wzK_IRzTkYzszfImdCmdYeU02Mbwr4A' # we gotta hide this somehow

@app.route('/maps')
def initmaps():
    user_id = session['user_id']
    existing_maps = Map.get_all_maps_by_user({'user_id': user_id})
    existing_maps_list = []
    for _map in existing_maps:
        data = {
            'id': _map.id,
            'name': _map.name,
        }
        existing_maps_list.append(data)
    #get user location through geolocation
    client = googlemaps.Client(key)
    geocode_result = client.geolocate()

    print(geocode_result['location'])
    data = {
        'lat': geocode_result['location']['lat'],
        'lng': geocode_result['location']['lng'],
    }

    users_maps = Map.get_all_maps_by_user({'user_id': session['user_id']})
    users_maps.reverse()
    users_maps_list = []
    return render_template('maps.html', key=key, data=data, existing_maps=existing_maps_list)

@app.route('/maps/<int:map_id>')
def show_map(map_id):
    pass

@app.route('/newmap')
def create_map():
    user_id = session['user_id']
    username = session['username']
    existing_maps = Map.get_all_maps_by_user({'user_id': user_id})
    existing_maps_list = []
    for _map in existing_maps:
        data = {
            'map_id': _map.id,
            'map_name': _map.name,
        }
        existing_maps_list.append(data)
    if existing_maps_list:
        name = "{}'s Map #{}".format(username, len(existing_maps_list) + 1)
    else:
        name = "Godspeed, {}".format(username)
    data = {
        'name': name,
        'user_id': user_id,
    }
    Map.create_map(data)
    users_maps = Map.get_all_maps_by_user({'user_id': user_id})
    last_map = users_maps[-1]
    map_id = last_map.id
    return redirect(f'/maps/{username}/{map_id}')

@app.route('/maps/<string:username>/<int:map_id>')
def show_user_map(username, map_id):
    if username != session['username']:
        flash('You do not have permission to view this map' , 'invalidMapAuthor')
        return redirect('/maps')
    _map = Map.get_map_by_id({'id': map_id})
    print(_map, 'THIS IS THE MAP')
    map_data = {
        'id': _map.id,
        'name': _map.name,
        'author': _map.author,
        'is_public': _map.is_public,
    }
    print(map_data)

    stops = Map.stops_by_map({'map_id': map_id})
    client = googlemaps.Client(key)
    geocode_result = client.geolocate()
    data = {
        'lat': geocode_result['location']['lat'],
        'lng': geocode_result['location']['lng'],
    }
    if len(stops) <= 0:
        return render_template('newmap.html', key=key, data=data, map=map_data)
    else:
        stop_list = []
        for stop in stops:
            stop_data = {
                'marker_id': stop['marker_id'],
                'address': stop['address'],
                'latitude': stop['latitude'],
                'longitude': stop['longitude'],
                'map_id': stop['map_id'],
            }
            stop_list.append(stop_data)
        return render_template('newmap.html', key=key, data=data, stops=stop_list, map=map_data)
    
@app.route('/add_marker', methods=['POST'])
def add_marker():
    user_id = session['user_id']
    marker_submission = request.form
    print(marker_submission)
    data = {
        'latitude': marker_submission['lat'],
        'longitude': marker_submission['lng'],
        'address': marker_submission['address'],
        'maps_id': marker_submission['map_id'],
        'user_id': user_id,
    }
    print('DATA IS ', data)
    Marker.create_marker(data)
    map_stops_data = {
        'map_id': marker_submission['map_id'],
    }
    map_stops = Map.stops_by_map(map_stops_data)
    print('MAP STOPS ARE ', map_stops)
    return jsonify({'success': True})
