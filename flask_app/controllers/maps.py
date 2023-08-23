from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.map_model import Map, Marker, Route
from flask_app.models.user_model import User
import googlemaps

key = 'AIzaSyC3wzK_IRzTkYzszfImdCmdYeU02Mbwr4A' # we gotta hide this somehow

@app.route('/maps')
def initmaps():
    user_id = session['user_id']
    existing_maps = Map.get_all_maps_by_user({'user_id': user_id})
    existing_maps_list = []
    if existing_maps:
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
    return render_template('maps.html', key=key, data=data, existing_maps=existing_maps_list)

@app.route('/maps/<int:map_id>')
def show_map(map_id):
    pass

@app.route('/newmap')
def create_map():
    user_id = session['user_id']
    username = session['username']
    existing_maps = Map.get_all_maps_by_user({'user_id': user_id})
    # existing_maps_list = []
    # for _map in existing_maps:
    #     data = {
    #         'map_id': _map.id,
    #         'map_name': _map.name,
    #     }
    #     existing_maps_list.append(data)
    if existing_maps == False:
        print(user_id)
        name = "Godspeed, {}".format(username)
        data = {
        'name': name,
        'author': user_id,
        }
        new_map_id = Map.create_map(data)


        return redirect(f'/maps/{username}/{new_map_id}')
    else:
        existing_maps_list = []
        for _map in existing_maps:
            existing_maps_list.append(_map.id)
        name = "{}'s Map #{}".format(username, len(existing_maps_list) + 1)
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
    markers = Marker.get_markers_by_map({'map_id': map_id})
    client = googlemaps.Client(key)
    if len(markers) == 0:
        geocode_result = client.geolocate()
        print(geocode_result)
        print(geocode_result['location'])
        data = {
            'lat': geocode_result['location']['lat'],
            'lng': geocode_result['location']['lng'],
        }
        return render_template('newmap.html', key=key, data=data)
    else:
        for marker in markers: 
            pass
        
        return 'show user map'
    
@app.route('/add_marker', methods=['POST'])
def add_marker():
    user_id = session['user_id']
    marker_submission = request.form
    data = {
        'latitude': marker_submission['lat'],
        'longitude': marker_submission['lng'],
        'address': marker_submission['address'],
        'maps_id': marker_submission['map_id'],
        'user_id': user_id,
    }
    stop = Marker.create_marker(data)
    print(stop)
    stop_order = Route.get_max_stop_number({'map_id': marker_submission['map_id']})
    stop_data = {
        'marker_id': stop,
        'map_id': marker_submission['map_id'],
        'stop_number': stop_order,
    }
    Route.create_route(stop_data)
    return jsonify({'success': True})
