from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Bandas:
    db_name = 'music_events'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.nombre = db_data['nombre']
        self.num_integrantes = db_data['num_integrantes']
        self.video = db_data['video']
        self.avatar = db_data['avatar']
        self.celular = db_data['celular']
        self.email = db_data['email']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.genero_id = db_data['genero_id']
        self.usuario_id = db_data['usuario_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO bandas (nombre, num_integrantes, video, avatar, celular, email, genero_id,usuario_id) VALUES (%(nombre)s,%(num_integrantes)s,%(video)s,%(avatar)s,%(celular)s,%(email)s,%(genero_id)s,%(usuario_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bandas;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_bandas = []
        for row in results:
            print(row['nombre'])
            all_bandas.append( cls(row) )
        return all_bandas
    
    @classmethod
    def get_all_by_user(cls, data):
        query = "SELECT * FROM bandas WHERE usuario_id = %(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        all_bandas = []
        for row in results:
            print(row['nombre'])
            all_bandas.append( cls(row) )
        return all_bandas
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM bandas WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE bandas SET nombre=%(nombre)s, num_integrantes=%(num_integrantes)s, video=%(video)s, avatar=%(avatar)s, celular=%(celular)s,email=%(email)s, genero_id= %(genero_id)s,usuario_id = %(usuario_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM solicitudes_bandas WHERE banda_id = %(id)s;"
        connectToMySQL(cls.db_name).query_db(query,data)
        query = "DELETE FROM calificaciones_bandas WHERE banda_id = %(id)s;"
        connectToMySQL(cls.db_name).query_db(query,data)
        query = "DELETE FROM bandas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_banda(banda):
        is_valid = True
        if len(banda['nombre']) < 3:
            is_valid = False
            flash("Introduzca un nombre de banda","banda")
        if banda['num_integrantes'] == "":
            is_valid = False
            flash("Introduzca integrantes","banda")
        if len(banda['email']) < 3:
            is_valid = False
            flash("Introduzaca un email","banda")
        if len(banda['celular']) < 3:
            is_valid = False
            flash("Introduzca un numero celular","banda")
        #if banda['genero_id'] == "":
            #is_valid = False
            #flash("Escoga un genero","banda")
        return is_valid

    @classmethod
    def get_all_by_user_ok(cls,data):
        
        query = "SELECT * FROM music_events.bandas WHERE id IN (SELECT banda_id FROM solicitudes_bandas WHERE usuario_id = %(id)s);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        
        bandas = []
        
        if len(results) >= 1:
            for row in results:
                bandas.append(cls(row))
            print(bandas)
            
        return bandas
    
    @classmethod
    def get_all_by_user_new(cls,data):
        
        query = "SELECT * FROM music_events.bandas WHERE id NOT IN (SELECT banda_id FROM solicitudes_bandas WHERE usuario_id = %(id)s ) AND usuario_id != %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        
        bandas = []
        
        if len(results) >= 1:
            for row in results:
                bandas.append(cls(row))
            print(bandas)
            
        return bandas