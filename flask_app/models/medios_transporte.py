from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class MediosTransporte:
    db_destino = 'hermes'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.nombre = db_data['nombre']
        self.codigo = db_data['codigo']
        self.co2_x_km = db_data['co2_x_km']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO medios_transporte (nombre, codigo, co2_x_km) VALUES (%(nombre)s,%(codigo)s,%(co2_x_km)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls,data):
        
        query = "SELECT * FROM medios_transporte;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        medios_transporte = []
        
        if len(results) >= 1:
            for row in results:
                medios_transporte.append(cls(row))
            print(medios_transporte)
            
        return medios_transporte
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM medios_transporte WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )

    @staticmethod
    def validate_medio_transporte(medio_transporte):
        
        is_valid = True
        
        if len(medio_transporte['pasajero_identificacion']) < 3:
            is_valid = False
            flash("Identificación debe tener al menos 3 characters","medio_transporte")
        if len(medio_transporte['pasajero_nombre']) < 3:
            is_valid = False
            flash("Nombre debe tener al menos 3 characters","medio_transporte")
        if len(medio_transporte['descripcion']) < 3:
            is_valid = False
            flash("Descripción debe tener al menos 3 characters","medio_transporte")
            
        return is_valid