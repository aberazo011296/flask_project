from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def create_user():
    
    validacion = json.loads(User.validate_register(request.form))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 201)
    
    data = {
        "nombre": request.form["nombre"],
        "apellido" : request.form["apellido"],
        "email" : request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
        
    id = User.save(data)
    session['user_id'] = id

    validacion['message'] = "Usuario ingresado correctamente"
    return make_response(jsonify(validacion), 201)


@app.route('/login',methods=['POST'])
def login():
    user = User.user_by_email(request.form)

    if not user:
        flash("Correo Incorrecto o Contraseña incorrecta","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Correo Incorrecto o Contraseña incorrecta","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# @app.route('/login',methods=['POST'])
# def login():
    
#     user = User.user_by_email(request.form)

#     if not user:
#         return make_response(jsonify(
#             status='error',
#             message='Correo Incorrecto o Contraseña incorrecta'
#             ), 404)
        
#     if not bcrypt.check_password_hash(user.password, request.form['password']):
#         return make_response(jsonify(
#             status='error',
#             message='Correo Incorrecto o Contraseña incorrecta'
#             ), 404)
        
#     session['user_id'] = user.id
#     return make_response(jsonify(
#             status='ok',
#             message='Ingreso correcto'
#             ), 200)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),recipes=Recipe.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')