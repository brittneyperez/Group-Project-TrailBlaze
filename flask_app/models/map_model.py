from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask_app.utility import maps_util

class Map:
    db = "trailblaze_schema"
    def __init__(self, data):
        self.id = data['id']
        self.is_public = data['is_public']
        self.name = data['name']
        self.author = data['user_id']
        self.stops = []

    @classmethod
    def create_map(cls, data):
        query = "INSERT INTO maps (name, user_id) VALUES (%(name)s, %(user_id)s);"
        connectToMySQL(cls.db).query_db(query, data)
        query = "SELECT * FROM maps ORDER BY maps.id DESC LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query)
        print(result)
        if len(result) == 0:
            return 1
        return result[0]['id']

    @classmethod
    def get_map(cls, data):
        query = "SELECT * FROM maps WHERE maps.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_all_maps_by_user(cls, data):
        query = "SELECT * FROM maps WHERE maps.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        all_user_maps = []
        for user_map in results:
            all_user_maps.append(cls(user_map))
        if len(all_user_maps) > 0:
            print('all_maps' + all_user_maps)
            return all_user_maps
        else:
            return False
    
    @classmethod
    def get_all_maps_by_user_dict(cls, data): #not using this one, but its nice
        query = "SELECT * FROM maps WHERE maps.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        all_user_maps = []

        for user_map in results:
            data = {
                'map_id': user_map['id'],
                'map_name': user_map['name'],
                'map_author': user_map['user_id'],
                'map_is_public': user_map['is_public'],
                
            }
            all_user_maps.append(data)
        return all_user_maps
    
    @classmethod
    def get_map_by_id(cls, data):
        query = "SELECT * FROM maps WHERE maps.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        current_map = cls(result[0])
        map_data = {
            'map_id': current_map.id,
            'map_name': current_map.name,
            'map_author': current_map.author,
            'map_is_public': current_map.is_public,
        }
        return map_data
    
    @classmethod
    def stops_by_map(cls, data):
        query = """
        SELECT m.id AS marker_id, m.latitude, m.longitude, m.address, mp.id AS map_id
        FROM markers m
        JOIN maps mp ON m.maps_id = mp.id
        WHERE mp.id = %(map_id)s;
        """
        all_stops = connectToMySQL(cls.db).query_db(query, data)
        stops = []
        for stop in all_stops:
            data = {
                'marker_id': stop['marker_id'],
                'address': stop['address'],
                'latitude': stop['latitude'],
                'longitude': stop['longitude'],
                'map_id': stop['map_id'],
            }
            stops.append(data)
        return stops

class Marker:
    db = "trailblaze_schema"
    def __init__(self, data):
        self.id = data['id']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.address = data['address']
        self.maps_id = data['map_id']
        self.user_id = data['user_id']

    @classmethod
    def create_marker(cls, data):
        query = """
        INSERT INTO markers 
        (latitude, longitude, address, maps_id, user_id) VALUES 
        (%(latitude)s, %(longitude)s, %(address)s, %(maps_id)s, %(user_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    
    @classmethod
    def get_markers_by_map(cls, data):
        query = "SELECT * FROM markers WHERE markers.map_id = %(map_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        markers = []
        if results == False:
            return markers
        for marker in results:
            markers.append(cls(marker))
        return markers
    
    @classmethod
    def get_marker(cls, data):
        query = "SELECT * FROM markers WHERE markers.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def delete_marker(cls, data):
        query = "DELETE FROM markers WHERE markers.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


class Route:
    db = "trailblaze_schema"
    def __init__(self, data):
        self.id = data['id']
        self.map = data['map_id']
        self.marker = data['marker_id']
        self.stop_number = data['stop_number']

    @classmethod
    def create_route(cls, data):
        query = """
        INSERT INTO routes (map_id, marker_id, stop_number) VALUES
        ((SELECT maps.id, markers.id FROM maps.id = %(map_id)s AND markers.id %(marker_id)s), %(stop_number)s);"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def sort(cls,data):
        pass
    @classmethod
    def get_route(cls, data):
        query = "SELECT * FROM routes WHERE routes.map_id = %(map_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        routes = []
        for route in results:
            routes.append(cls(route))
        return routes
    
    @classmethod
    def get_route_by_map(cls, data):
        query = "SELECT * FROM routes WHERE routes.map_id = %(map_id)s ORDER BY stop_number;"
        results = connectToMySQL(cls.db).query_db(query, data)
        stops = []
        for stop in results:
            data = {
                'marker_id': stop['marker_id'],
            }
            marker = Marker.get_marker(data)
            marker_data = {
                'marker_id': marker.id,
                'address': marker.address,
                'latitude': marker.latitude,
                'longitude': marker.longitude,
                'stop_number': stop['stop_number'],
            }
            stops.append(marker_data)
        return stops
    
    @classmethod
    def get_max_stop_number(cls, data):
        query = """
        SELECT * FROM routes WHERE map_id = %(map_id)s ORDER BY routes.stop_number DESC LIMIT 1;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        if len(result) == 0:
            print('returning 1')
            return 1
        max_stop_number = result[0]['stop_number']
        return max_stop_number + 1
