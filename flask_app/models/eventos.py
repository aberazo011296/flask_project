from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import json
class Evento:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.titulo = db_data['titulo']
        self.fecha = db_data['fecha']
        self.direccion = db_data['direccion']
        self.hora_inicio = db_data['hora_inicio']
        self.hora_fin = db_data['hora_fin']
        self.opciones = db_data['opciones']
        self.num_integrantes = db_data['num_integrantes']
        self.genero_id = db_data['genero_id']
        self.usuario_id = db_data['usuario_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO eventos (titulo, fecha, direccion, hora_inicio, hora_fin, opciones, num_integrantes, genero_id, usuario_id) VALUES (%(titulo)s,%(fecha)s,%(direccion)s,%(hora_inicio)s,%(hora_fin)s,%(opciones)s,%(num_integrantes)s,%(genero_id)s,%(usuario_id)s );"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM eventos;"
        results = connectToMySQL(cls.db_destino).query_db(query)
        
        eventos = []
        
        if len(results) >= 1:
            for row in results:
                eventos.append(cls(row))
            print(eventos)
            
        return eventos

    @classmethod
    def get_all_evento(cls,data):
        
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
        query = "UPDATE eventos SET titulo = %(titulo)s, fecha = %(fecha)s, direccion = %(direccion)s,hora_inicio = %(hora_inicio)s,hora_fin = %(hora_fin)s,opciones = %(opciones)s,num_integrantes = %(num_integrantes)s, genero_id = %(genero_id)s,usuario_id = %(usuario_id)s,updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db( query, data )
        
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM eventos_instrumentos WHERE evento_id = %(evento_id)s"
        connectToMySQL(cls.db_destino).query_db( query, data )
        query  = "DELETE FROM solicitudes WHERE evento_id = %(evento_id)s"
        connectToMySQL(cls.db_destino).query_db( query, data )
        query  = "DELETE FROM eventos WHERE id = %(evento_id)s"
        return connectToMySQL(cls.db_destino).query_db( query, data )


    @staticmethod
    def validate_eventos(evento):
        
        is_valid = True
        categoria = "register"
        mensaje = "Exitoso"
        status = 'ok'
        code = 200
        

        if len(evento['titulo']) < 3:
            mensaje = "El titulo debe tener por lo menos 3 caracteres"
            is_valid= False
            status = 'error'
            code = 400
            

            
        value = {
            "valid": is_valid,
            "message": mensaje,
            "category": categoria,
            "status": status,
            "code": code
        }
        
        return json.dumps(value)
    
    @classmethod
    def get_all_by_user_ok(cls,data):
        
        query = "SELECT * FROM music_events.eventos WHERE id IN (SELECT evento_id FROM solicitudes WHERE usuario_id = %(id)s);"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        eventos = []
        
        if len(results) >= 1:
            for row in results:
                eventos.append(cls(row))
            print(eventos)
            
        return eventos
    
    @classmethod
    def get_all_by_user_new(cls,data):
        
        query = "SELECT * FROM music_events.eventos WHERE id NOT IN (SELECT evento_id FROM solicitudes WHERE usuario_id = %(id)s) AND usuario_id != %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        
        eventos = []
        
        if len(results) >= 1:
            for row in results:
                eventos.append(cls(row))
            print(eventos)
            
        return eventos