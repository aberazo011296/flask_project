from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Rol:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.nombre = db_data['nombre']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO roles (nombre) VALUES (%(nombre)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM roles;"
        results = connectToMySQL(cls.db_destino).query_db(query)
        
        roles = []
        
        if len(results) >= 1:
            for row in results:
                roles.append(cls(row))
            print(roles)
            
        return roles
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM roles WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM roles WHERE viaje_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid