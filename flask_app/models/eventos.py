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
        self.genero_id = db_data['genero_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO eventos (titulo, fecha, direccion, hora_inicio, hora_fin, opciones, genero_id) VALUES (%(titulo)s,%(fecha)s,%(direccion)s,%(hora_inicio)s,%(hora_fin)s,%(opciones)s,%(genero_id)s );"
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
        query = "UPDATE eventos SET eventos_titulo = %(eventos_titulo)s, usuario_nombre = %(eventos_titulo)s, descripcion = %(descripcion)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db( query, data )
        
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM eventos WHERE id = %(id)s"
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
            
        # if len(evento['apellidos']) < 3:
        #     mensaje = "Apellidos debe tener por lo menos 3 caracteres"
        #     is_valid= False
        #     status = 'error'
        #     code = 400
            
        # if not EMAIL_REGEX.match(evento['email']):
        #     mensaje = "Formato Email incorrecto"
        #     is_valid=False
        #     status = 'error'
        #     code = 400
            
        # if not re.search(PASSWORD_REGEX, evento['password']):
        #     mensaje = "Contraseña debe tener números, letras mayúsculas y minúculas, caracteres especiales"
        #     is_valid=False
        #     status = 'error'
        #     code = 400

        # if len(evento['password']) < 8:
        #     mensaje = "Contraseña debe tener por lo menos 8 caracteres"
        #     is_valid= False
        #     status = 'error'
        #     code = 400

        # if evento['password'] != evento['confirm']:
        #     mensaje = "Contraseñas no coinciden"
        #     is_valid= False
        #     status = 'error'
        #     code = 400
        
        # fecha_nacimiento = datetime.strptime(evento['fecha_nacimiento'], '%Y-%m-%d')

        # edad = Evento.calculate_age(fecha_nacimiento)
        
        # if(edad < 18):
        #     mensaje = "Usuario menor de edad"
        #     is_valid= False
        #     status = 'error'
        #     code = 400
            
        value = {
            "valid": is_valid,
            "message": mensaje,
            "category": categoria,
            "status": status,
            "code": code
        }
        
        return json.dumps(value)
