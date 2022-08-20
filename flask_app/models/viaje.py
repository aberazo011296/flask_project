from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import time

class Viaje:
    db_destino = 'viajes'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.destino = db_data['destino']
        self.fecha_inicio = db_data['fecha_inicio']
        self.fecha_fin = db_data['fecha_fin']
        self.plan = db_data['plan']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO viajes (destino, fecha_inicio, fecha_fin, plan) VALUES (%(destino)s,%(fecha_inicio)s,%(fecha_fin)s,%(plan)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM viajes WHERE viajes.id IN ( SELECT viaje_id FROM usuarios_viajes WHERE usuario_id = %(id)s );"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        viajes = []
        for row in results:
            viajes.append(cls(row))
        print(viajes)
        return viajes
    
    @classmethod
    def get_all_others(cls,data):
        query = "SELECT * FROM viajes LEFT JOIN usuarios_viajes ON viajes.id = usuarios_viajes.viaje_id LEFT JOIN usuarios ON usuarios.id = usuarios_viajes.usuario_id WHERE usuarios.id NOT IN (%(id)s) AND usuarios_viajes.viaje_id NOT IN (SELECT viaje_id FROM usuarios_viajes WHERE usuario_id = %(id)s);"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        viajes = []

        for row in results:
            if row['usuarios.id'] == None:
                break
            data = {
                "id": row['id'],
                "destino": row['destino'],
                "fecha_inicio": row['fecha_inicio'],
                "fecha_fin": row['fecha_fin'],
                "plan": row['plan'],
                "nombre": row['nombre'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            
            viajes.append(data)

        return viajes
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM viajes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )

    @staticmethod
    def validate_viaje(viaje):
        
        is_valid = True
        
        if len(viaje['destino']) < 3:
            is_valid = False
            flash("Destino debe tener al menos 3 characters","viaje")
        if len(viaje['plan']) < 3:
            is_valid = False
            flash("Plan debe tener al menos 3 characters","viaje")
        if viaje['fecha_inicio'] == "":
            is_valid = False
            flash("Fecha Inicio es requerida","viaje")
        if viaje['fecha_fin'] == "":
            is_valid = False
            flash("Fecha Fin es requerida","viaje")
            
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%Y-%m-%d", named_tuple)
        fecha_actual = time.strptime(time_string, "%Y-%m-%d")
        fecha_inicio_time = time.strptime(str(viaje['fecha_inicio']), "%Y-%m-%d")
        fecha_fin_time = time.strptime(str(viaje['fecha_fin']), "%Y-%m-%d")
        
        if fecha_actual >= fecha_fin_time:
            is_valid = False
            flash("Fecha Fin es menor o igual a la Fecha Actual","viaje")
        if fecha_actual >= fecha_inicio_time:
            is_valid = False
            flash("Fecha Inicio es menor o igual a la Fecha Actual","viaje")
        if fecha_inicio_time > fecha_fin_time:
            is_valid = False
            flash("Fecha Inicio es mayor a la Fecha Fin","viaje")
            
        return is_valid
    
    @classmethod
    def add_usuarios_viajes(cls,data):
        query = "INSERT INTO usuarios_viajes (usuario_id,viaje_id) VALUES (%(usuario_id)s,%(viaje_id)s);"
        return connectToMySQL(cls.db_destino).query_db(query,data);