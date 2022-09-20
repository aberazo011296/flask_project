from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Solicitud:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.usuario_id = db_data['usuario_id']
        self.evento_id = db_data['evento_id']
        self.estado = db_data['estado']
        self.titulo = db_data['titulo']
        self.direccion = db_data['direccion']
        self.fecha = db_data['fecha']
        self.hora_inicio = db_data['hora_inicio']
        self.hora_fin = db_data['hora_fin']
        self.num_integrantes = db_data['num_integrantes']
        self.email = db_data['email']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO solicitudes (evento_id, usuario_id, estado) VALUES (%(evento_id)s, %(usuario_id)s, %(estado)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls, data):
        
        query = "SELECT solicitudes.usuario_id, solicitudes.evento_id, solicitudes.estado, eventos.titulo, eventos.direccion, eventos.fecha, eventos.hora_inicio, eventos.hora_fin, eventos.num_integrantes, usuarios.email FROM eventos JOIN solicitudes ON eventos.id = solicitudes.evento_id JOIN usuarios ON usuarios.id = solicitudes.usuario_id WHERE usuarios.id = %(id)s ORDER BY solicitudes.updated_at DESC;"
        results = connectToMySQL(cls.db_destino).query_db(query, data)
        
        solicitudes = []
        
        if len(results) >= 1:
            for row in results:
                solicitudes.append(cls(row))
            print(solicitudes)
            
        return solicitudes
    
    @classmethod
    def get_all_eventos_usuario(cls, data):
        
        query = "SELECT solicitudes.usuario_id, solicitudes.evento_id, solicitudes.estado, eventos.titulo, eventos.direccion, eventos.fecha, eventos.hora_inicio, eventos.hora_fin, eventos.num_integrantes, usuarios.email FROM usuarios JOIN solicitudes ON usuarios.id = solicitudes.usuario_id JOIN eventos ON eventos.id = solicitudes.evento_id WHERE eventos.id IN (SELECT id FROM eventos WHERE usuario_id = %(id)s) ORDER BY solicitudes.updated_at DESC;"
        results = connectToMySQL(cls.db_destino).query_db(query, data)
        
        solicitudes = []
        
        if len(results) >= 1:
            for row in results:
                solicitudes.append(cls(row))
            print(solicitudes)
            
        return solicitudes
    
    @classmethod
    def get_all_by_evento(cls, data):
        
        query = "SELECT COUNT(*) as cont FROM solicitudes WHERE evento_id = %(id)s AND estado = 'aceptado';"
        results = connectToMySQL(cls.db_destino).query_db(query, data)
        return results[0]['cont']
    
    @classmethod
    def get_by_user(cls,data):
        query = "SELECT evento_id FROM solicitudes WHERE usuario_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        instrumentos = []
        
        if len(results) >= 1:
            for row in results:
                instrumentos.append(cls(row))
            print(instrumentos)
            
        return instrumentos
    
    @classmethod
    def delete_by_user(cls, data):
        query  = "DELETE FROM solicitudes WHERE usuario_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM solicitudes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE solicitudes SET estado = %(estado)s, updated_at = NOW() WHERE evento_id = %(evento_id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(cls.db_destino).query_db( query, data )
    
    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid