from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Tramos:
    db_destino = 'hermes'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.posicion = db_data['posicion']
        self.origen = db_data['origen']
        self.destino = db_data['destino']
        self.km = db_data['km']
        self.co2 = db_data['co2']
        self.viaje_id = db_data['viaje_id']
        self.medio_transporte_id = db_data['medio_transporte_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO tramos (posicion, origen, destino, km, co2, viaje_id, medio_transporte_id) VALUES (%(posicion)s,%(origen)s,%(destino)s,%(km)s,%(co2)s,%(viaje_id)s,%(medio_transporte_id)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls,data):
        
        query = "SELECT * FROM tramos;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        tramos = []
        
        if len(results) >= 1:
            for row in results:
                tramos.append(cls(row))
            print(tramos)
            
        return tramos
    
    @classmethod
    def get_all_viaje(cls,data):
        
        query = "SELECT * FROM tramos WHERE viaje_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        tramos = []
        
        if len(results) >= 1:
            for row in results:
                tramos.append(cls(row))
            print(tramos)
            
        return tramos
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM tramos WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM tramos WHERE viaje_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['pasajero_identificacion']) < 3:
            is_valid = False
            flash("Identificación debe tener al menos 3 characters","tramo")
        if len(tramo['pasajero_nombre']) < 3:
            is_valid = False
            flash("Nombre debe tener al menos 3 characters","tramo")
        if len(tramo['descripcion']) < 3:
            is_valid = False
            flash("Descripción debe tener al menos 3 characters","tramo")
            
        return is_valid