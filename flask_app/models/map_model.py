from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User

class Map:
    db = "trailblaze"
    def __init__(self, data):
        self.id = data['id']
        self.is_public = data['is_public']
        self.name = data['name']
        self.author = data['user_id']
        self.stops = []

    
    @classmethod
    def create_map(cls, data):
        query = "INSERT INTO maps (is_public, name, user_id) VALUES (%(name)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_map(cls, data):
        query = "SELECT * FROM maps WHERE maps.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_all_maps_by_user(cls, data):
        query = "SELECT * FROM maps WHERE maps.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        maps = []
        for map in results:
            maps.append(cls(map))
        return maps
    
class Marker:
    db = "trailblaze"
    def __init__(self, data):
        self.id = data['id']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.address = data['address']
        self.map_id = data['map_id']

    @classmethod
    def create_marker(cls, data):
        query = "INSERT INTO markers (latitude, longitude, address, map_id) VALUES (%(latitude)s, %(longitude)s, %(address)s, %(map_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    
    @classmethod
    def get_markers_by_map(cls, data):
        query = "SELECT * FROM markers WHERE markers.map_id = %(map_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        markers = []
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

