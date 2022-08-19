from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_nombre = 'recetas'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.nombre = db_data['nombre']
        self.descripcion = db_data['descripcion']
        self.instrucciones = db_data['instrucciones']
        self.bajotiempo = db_data['bajotiempo']
        self.fecha_elaboracion = db_data['fecha_elaboracion']
        self.usuario_id = db_data['usuario_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recetas (nombre, descripcion, instrucciones, bajotiempo, fecha_elaboracion, usuario_id) VALUES (%(nombre)s,%(descripcion)s,%(instrucciones)s,%(bajotiempo)s,%(fecha_elaboracion)s,%(usuario_id)s);"
        return connectToMySQL(cls.db_nombre).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recetas;"
        results =  connectToMySQL(cls.db_nombre).query_db(query)
        all_recetas = []
        for row in results:
            print(row['fecha_elaboracion'])
            all_recetas.append( cls(row) )
        return all_recetas
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recetas WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_nombre).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE recetas SET nombre=%(nombre)s, descripcion=%(descripcion)s, instrucciones=%(instrucciones)s, bajotiempo=%(bajotiempo)s, fecha_elaboracion=%(fecha_elaboracion)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_nombre).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recetas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_nombre).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['nombre']) < 3:
            is_valid = False
            flash("Nombre debe tener al menos 3 characters","recipe")
        if len(recipe['instrucciones']) < 3:
            is_valid = False
            flash("Instrucciones debe tener al menos 3 characters","recipe")
        if len(recipe['descripcion']) < 3:
            is_valid = False
            flash("Descripción debe tener al menos 3 characters","recipe")
        if recipe['fecha_elaboracion'] == "":
            is_valid = False
            flash("Fecha de elaboración es requerida","recipe")
        return is_valid