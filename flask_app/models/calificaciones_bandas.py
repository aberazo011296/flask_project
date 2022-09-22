from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class CalificacionBanda:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.banda_id = db_data['banda_id']
        self.puntuacion = db_data['puntuacion']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO calificaciones_bandas (banda_id,puntuacion) VALUES (%(banda_id)s,%(puntuacion)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM calificaciones_bandas;"
        results = connectToMySQL(cls.db_destino).query_db(query)
        
        calificaciones_bandas = []
        
        if len(results) >= 1:
            for row in results:
                calificaciones_bandas.append(cls(row))
            print(calificaciones_bandas)
            
        return calificaciones_bandas
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM calificaciones_bandas WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_one_by_user(cls,data):
        query = "SELECT * FROM calificaciones_bandas WHERE banda_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_avg(cls,data):
        query = "SELECT AVG(puntuacion) as promedio FROM music_events.calificaciones_bandas WHERE banda_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return results
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM calificaciones_bandas WHERE viaje_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid