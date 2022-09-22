from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class CalificacionEvento:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.evento_id = db_data['evento_id']
        self.puntuacion = db_data['puntuacion']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO calificaciones_eventos (evento_id,puntuacion) VALUES (%(evento_id)s,%(puntuacion)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM calificaciones_eventos;"
        results = connectToMySQL(cls.db_destino).query_db(query)
        
        calificaciones_eventos = []
        
        if len(results) >= 1:
            for row in results:
                calificaciones_eventos.append(cls(row))
            print(calificaciones_eventos)
            
        return calificaciones_eventos
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM calificaciones_eventos WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_one_by_user(cls,data):
        query = "SELECT * FROM calificaciones_eventos WHERE evento_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_avg(cls,data):
        query = "SELECT AVG(puntuacion) as promedio FROM music_events.calificaciones_eventos WHERE evento_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return results
    

    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid