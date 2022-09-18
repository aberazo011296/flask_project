from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Evento:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.titulo = db_data['titulo']
        self.fecha = db_data['fecha']
        self.direccion = db_data['direccion']
        self.hora_inicio = db_data['hora_inicio']
        self.hora_fin = db_data['hora_fin']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO eventos (pasajero_identificacion, pasajero_nombre, descripcion, usuario_id) VALUES (%(pasajero_identificacion)s,%(pasajero_nombre)s,%(descripcion)s,%(usuario_id)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls,data):
        
        query = "SELECT * FROM eventos;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        eventos = []
        
        if len(results) >= 1:
            for row in results:
                eventos.append(cls(row))
            print(eventos)
            
        return eventos

    @classmethod
    def get_all_user(cls,data):
        
        query = "SELECT * FROM eventos WHERE usuario_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        eventos = []
        
        if len(results) >= 1:
            for row in results:
                eventos.append(cls(row))
            print(eventos)
            
        return eventos

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM eventos WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE eventos SET pasajero_identificacion = %(pasajero_identificacion)s, pasajero_nombre = %(pasajero_nombre)s, descripcion = %(descripcion)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db( query, data )
        
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM eventos WHERE id = %(id)s"
        return connectToMySQL(cls.db_destino).query_db( query, data )

    @staticmethod
    def validate_evento(evento):
        
        is_valid = True
        
        if len(evento['pasajero_identificacion']) < 3:
            is_valid = False
            flash("Identificación debe tener al menos 3 characters","evento")
        if len(evento['pasajero_nombre']) < 3:
            is_valid = False
            flash("Nombre debe tener al menos 3 characters","evento")
        if len(evento['descripcion']) < 3:
            is_valid = False
            flash("Descripción debe tener al menos 3 characters","evento")
            
        return is_valid