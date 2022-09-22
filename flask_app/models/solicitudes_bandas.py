from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Solicitud_Banda:
    db_destino = 'music_events'

    def __init__(self,db_data):
        self.usuario_id = db_data['usuario_id']
        self.banda_id = db_data['banda_id']
        self.estado = db_data['estado']
        self.nombre = db_data['nombre']
        self.num_integrantes = db_data['num_integrantes']
        self.celular = db_data['celular']    
        self.email = db_data['email']
        

    @classmethod
    def save(cls,data):
        query = "INSERT INTO solicitudes_bandas (banda_id, usuario_id, estado) VALUES (%(banda_id)s, %(usuario_id)s, %(estado)s);"
        return connectToMySQL(cls.db_destino).query_db(query, data)

    @classmethod
    def get_all(cls, data):
        
        query = "SELECT solicitudes_bandas.usuario_id, solicitudes_bandas.banda_id, solicitudes_bandas.estado, bandas.nombre, bandas.celular, bandas.num_integrantes, usuarios.email FROM bandas JOIN solicitudes_bandas ON bandas.id = solicitudes_bandas.banda_id JOIN usuarios ON usuarios.id = solicitudes_bandas.usuario_id WHERE usuarios.id = %(id)s ORDER BY solicitudes_bandas.updated_at DESC;"
        results = connectToMySQL(cls.db_destino).query_db(query, data)
        
        solicitudes_bandas = []
        
        if len(results) >= 1:
            for row in results:
                solicitudes_bandas.append(cls(row))
            print(solicitudes_bandas)
            
        return solicitudes_bandas
    
    @classmethod
    def get_all_bandas_usuario(cls, data):
        
        query = "SELECT solicitudes_bandas.usuario_id, solicitudes_bandas.banda_id, solicitudes_bandas.estado, bandas.nombre, bandas.celular, bandas.num_integrantes, usuarios.email FROM usuarios JOIN solicitudes_bandas ON usuarios.id = solicitudes_bandas.usuario_id JOIN bandas ON bandas.id = solicitudes_bandas.banda_id WHERE bandas.id IN (SELECT id FROM bandas WHERE usuario_id = %(id)s) ORDER BY solicitudes_bandas.updated_at DESC;"
        results = connectToMySQL(cls.db_destino).query_db(query, data)
        
        solicitudes_bandas = []
        
        if len(results) >= 1:
            for row in results:
                solicitudes_bandas.append(cls(row))
            print(solicitudes_bandas)
            
        return solicitudes_bandas
    
    @classmethod
    def get_all_by_banda(cls, data):
        
        query = "SELECT COUNT(*) as cont FROM solicitudes_bandas WHERE banda_id = %(id)s AND estado = 'aceptado';"
        results = connectToMySQL(cls.db_destino).query_db(query, data)
        return results[0]['cont']
    
    @classmethod
    def get_by_user(cls,data):
        query = "SELECT banda_id FROM solicitudes_bandas WHERE usuario_id = %(id)s;"
        results = connectToMySQL(cls.db_destino).query_db(query,data)
        instrumentos = []
        
        if len(results) >= 1:
            for row in results:
                instrumentos.append(cls(row))
            print(instrumentos)
            
        return instrumentos
    
    @classmethod
    def delete_by_user(cls, data):
        query  = "DELETE FROM solicitudes_bandas WHERE usuario_id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM solicitudes_bandas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE solicitudes_bandas SET estado = %(estado)s, updated_at = NOW() WHERE banda_id = %(banda_id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(cls.db_destino).query_db( query, data )
    

    
    @staticmethod
    def validate_tramo(tramo):
        
        is_valid = True
        
        if len(tramo['nombre']) < 3:
            is_valid = False
            flash("nombre debe tener al menos 3 characters","tramo")
            
        return is_valid

