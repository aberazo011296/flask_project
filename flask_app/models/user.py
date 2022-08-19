from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$")
from flask import flash
import json

class User:
    
    db_name = 'recetas'
    
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
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
        query = "INSERT INTO usuarios ( nombre, apellido, email, password ) VALUES ( %(nombre)s, %(apellido)s, %(email)s, %(password)s );"
        return connectToMySQL(cls.db_name).query_db( query, data )
    
    @classmethod
    def get_by_id(cls, data):
        query  = "SELECT * FROM usuarios WHERE id = %(id)s";
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def user_by_email(cls, data):
        query  = "SELECT * FROM usuarios WHERE email = %(email)s";
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

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
            
        if not EMAIL_REGEX.match(user['email']):
            mensaje = "Email no válido"
            is_valid=False
            status = 'error'
            code = 400

        if len(user['nombre']) < 3:
            mensaje = "Nombre debe tener por lo menos 3 caracteres"
            is_valid= False
            status = 'error'
            code = 400

        if len(user['apellido']) < 3:
            mensaje = "Apellido debe tener por lo menos 3 caracteres"
            is_valid= False
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
            
        value = {
            "valid": is_valid,
            "message": mensaje,
            "category": categoria,
            "status": status,
            "code": code
        }
        
        return json.dumps(value)