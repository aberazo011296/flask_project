from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Solicitud:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.usuario_id = db_data['usuario_id']
        self.evento_id = db_data['evento_id']
        self.estado = db_data['estado']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO solicitudes (evento_id, usuario_id, estado) VALUES (%(evento_id)s, %(usuario_id)s, %(estado)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM solicitudes;"
        results = connectToMySQL(cls.db_destino).query_db(query)
        
        instrumentos = []
        
        if len(results) >= 1:
            for row in results:
                instrumentos.append(cls(row))
            print(instrumentos)
            
        return instrumentos
    
    @classmethod
    def get_by_user(cls,data):
        query = "SELECT evento_id FROM solicitudes WHERE usuario_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        instrumentos = []
        
        if len(results) >= 1:
            for row in results:
                instrumentos.append(cls(row))
            print(instrumentos)
            
        return instrumentos
    
    @classmethod
    def delete_by_user(cls, data):
        query  = "DELETE FROM solicitudes WHERE usuario_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM solicitudes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE solicitudes SET evento_id = %(evento_id)s, usuario_id = %(usuario_id)s, estado = %(estado)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db( query, data )
    
    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid