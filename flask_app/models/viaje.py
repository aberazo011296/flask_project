from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Viaje:
    db_destino = 'hermes'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.pasajero_identificacion = db_data['pasajero_identificacion']
        self.pasajero_nombre = db_data['pasajero_nombre']
        self.descripcion = db_data['descripcion']
        self.km_total = db_data['km_total']
        self.co2_total = db_data['co2_total']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO viajes (pasajero_identificacion, pasajero_nombre, descripcion, usuario_id) VALUES (%(pasajero_identificacion)s,%(pasajero_nombre)s,%(descripcion)s,%(usuario_id)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls,data):
        
        query = "SELECT * FROM viajes;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        viajes = []
        
        if len(results) >= 1:
            for row in results:
                viajes.append(cls(row))
            print(viajes)
            
        return viajes
    
    @classmethod
    def get_all_user(cls,data):
        
        query = "SELECT * FROM viajes WHERE usuario_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        viajes = []
        
        if len(results) >= 1:
            for row in results:
                viajes.append(cls(row))
            print(viajes)
            
        return viajes
    
    @classmethod
    def get_all_count(cls,data):
        query = "SELECT COUNT(*) FROM viajes"
        return connectToMySQL(cls.db_destino).query_db(query,data)[0]
    
    @classmethod
    def get_all_co2_count(cls,data):
        query = "SELECT SUM(co2_total) FROM viajes"
        return connectToMySQL(cls.db_destino).query_db(query,data)[0]
    
    @classmethod
    def get_all_count_user(cls,data):
        query = "SELECT COUNT(*) FROM viajes WHERE usuario_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query,data)[0]
    
    @classmethod
    def get_all_co2_count_user(cls,data):
        query = "SELECT SUM(co2_total) FROM viajes WHERE usuario_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query,data)[0]
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM viajes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_month(cls,data):
        query = "SELECT COUNT(*) FROM viajes WHERE updated_at >= %(inicio_mes)s AND updated_at <= %(fin_mes)s"
        return connectToMySQL(cls.db_destino).query_db(query,data)[0]
    
    @classmethod
    def get_month_co2(cls,data):
        query = "SELECT SUM(co2_total) FROM viajes WHERE updated_at >= %(inicio_mes)s AND updated_at <= %(fin_mes)s"
        return connectToMySQL(cls.db_destino).query_db(query,data)[0]
    
    @classmethod
    def edit_totales(cls, data):
        query = "UPDATE viajes SET km_total = %(km_total)s, co2_total = %(co2_total)s WHERE id = %(id)s"
        return connectToMySQL(cls.db_destino).query_db( query, data )
    
    @classmethod
    def update(cls, data):
        query = "UPDATE viajes SET pasajero_identificacion = %(pasajero_identificacion)s, pasajero_nombre = %(pasajero_nombre)s, descripcion = %(descripcion)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db( query, data )
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM viajes WHERE id = %(id)s"
        return connectToMySQL(cls.db_destino).query_db( query, data )

    @staticmethod
    def validate_viaje(viaje):
        
        is_valid = True
        
        if len(viaje['pasajero_identificacion']) < 3:
            is_valid = False
            flash("Identificación debe tener al menos 3 characters","viaje")
        if len(viaje['pasajero_nombre']) < 3:
            is_valid = False
            flash("Nombre debe tener al menos 3 characters","viaje")
        if len(viaje['descripcion']) < 3:
            is_valid = False
            flash("Descripción debe tener al menos 3 characters","viaje")
            
        return is_valid