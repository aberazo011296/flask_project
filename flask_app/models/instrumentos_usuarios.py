from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class InstrumentoUsuario:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.instrumento_id = db_data['instrumento_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO instrumentos_usuarios (instrumento_id, usuario_id) VALUES (%(instrumento_id)s, %(usuario_id)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM instrumentos_usuarios;"
        results = connectToMySQL(cls.db_destino).query_db(query)
        
        instrumentos = []
        
        if len(results) >= 1:
            for row in results:
                instrumentos.append(cls(row))
            print(instrumentos)
            
        return instrumentos
    
    @classmethod
    def get_by_user(cls,data):
        query = "SELECT instrumento_id FROM instrumentos_usuarios WHERE usuario_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        instrumentos = []
        
        if len(results) >= 1:
            for row in results:
                instrumentos.append(cls(row))
            print(instrumentos)
            
        return instrumentos
    
    @classmethod
    def delete_by_user(cls, data):
        query  = "DELETE FROM instrumentos_usuarios WHERE usuario_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid