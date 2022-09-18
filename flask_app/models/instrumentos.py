from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Instrumento:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.nombre = db_data['nombre']
        self.categoria = db_data['categoria']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO instrumentos (nombre, categoria) VALUES (%(nombre)s, %(categoria)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM instrumentos;"
        results = connectToMySQL(cls.db_destino).query_db(query)
        
        instrumentos = []
        
        if len(results) >= 1:
            for row in results:
                instrumentos.append(cls(row))
            print(instrumentos)
            
        return instrumentos
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM instrumentos WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM instrumentos WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid