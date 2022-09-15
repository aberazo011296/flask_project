from flask_app.config.mysqlconnection import connectToMySQL
import re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$")
from flask import flash
import json

class User:
    
    db_name = 'music_events'
    
    def __init__( self , data ):
        self.id = data['id']
        self.identificacion = data['identificacion']
        self.nombres = data['nombres']
        self.apellidos = data['apellidos']
        self.email = data['email']
        self.password = data['password']
        self.descripcion = data['descripcion']
        self.direccion = data['direccion']
        self.celular = data['celular']
        self.fecha_nacimiento = data['fecha_nacimiento']
        self.nacionalidad = data['nacionalidad']
        self.avatar = data['avatar']
        self.video = data['video']
        self.rol_id = data['rol_id']
        self.genero_id = data['genero_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL(cls.db_name).query_db(query)
        usuarios = []
        
        for user in results:
            usuarios.append( cls(user) )
        return usuarios
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios(identificacion,nombres,apellidos,email,password,descripcion,direccion,celular,fecha_nacimiento,nacionalidad,avatar,video,rol_id,genero_id) VALUES(%(identificacion)s,%(nombres)s,%(apellidos)s,%(email)s,%(password)s,%(descripcion)s,%(direccion)s,%(celular)s,%(fecha_nacimiento)s,%(nacionalidad)s,%(avatar)s,%(video)s,%(rol_id)s,%(genero_id)s);"
        return connectToMySQL(cls.db_name).query_db( query, data )
    
    @classmethod
    def get_by_id(cls, data):
        query  = "SELECT * FROM usuarios WHERE id = %(id)s";
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def user_by_email(cls, data):
        print("EBTROOOOOOOOO")
        print(data)
        query  = "SELECT * FROM usuarios WHERE email = %(email)s"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE usuarios SET identificacion = %(identificacion)s, nombres = %(nombres)s, apellidos = %(apellidos)s, email = %(email)s, password = %(password)s, descripcion = %(descripcion)s, direccion = %(direccion)s, celular = %(celular)s, fecha_nacimiento = %(fecha_nacimiento)s, nacionalidad = %(nacionalidad)s, avatar = %(avatar)s, video = %(video)s, updated_at = NOW(), rol_id = %(rol_id)s, genero_id = %(genero_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_destino).query_db( query, data )
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM usuarios WHERE id = %(id)s"
        return connectToMySQL(cls.db_destino).query_db( query, data )

    @staticmethod
    def calculate_age(born):
        today = datetime.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    @staticmethod
    def validate_register(user):
        
        is_valid = True
        categoria = "register"
        mensaje = "Exitoso"
        status = 'ok'
        code = 200
        
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)

        if len(results) >= 1:
            mensaje = "Ya existe este email."
            is_valid=False
            status = 'error'
            code = 400

        if len(user['nombres']) < 3:
            mensaje = "Nombres debe tener por lo menos 3 caracteres"
            is_valid= False
            status = 'error'
            code = 400
            
        if len(user['apellidos']) < 3:
            mensaje = "Apellidos debe tener por lo menos 3 caracteres"
            is_valid= False
            status = 'error'
            code = 400
            
        if not EMAIL_REGEX.match(user['email']):
            mensaje = "Formato Email incorrecto"
            is_valid=False
            status = 'error'
            code = 400

        if not re.search(PASSWORD_REGEX, user['password']):
            mensaje = "Contraseña debe tener números, letras mayúsculas y minúculas, caracteres especiales"
            is_valid=False
            status = 'error'
            code = 400

        if len(user['password']) < 8:
            mensaje = "Contraseña debe tener por lo menos 8 caracteres"
            is_valid= False
            status = 'error'
            code = 400

        if user['password'] != user['confirm']:
            mensaje = "Contraseñas no coinciden"
            is_valid= False
            status = 'error'
            code = 400
        
        fecha_nacimiento = datetime.strptime(user['fecha_nacimiento'], '%Y-%m-%d')
        
        edad = User.calculate_age(fecha_nacimiento)
        
        if(edad < 18):
            mensaje = "Usuario menor de edad"
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
