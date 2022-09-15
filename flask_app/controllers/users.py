from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.viaje import Viaje
from flask_app.models.roles import Rol
from flask_app.models.generos import Genero
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/registro")
def registro():
    return render_template("register.html", generos=Genero.get_all(), roles=Rol.get_all())

@app.route('/register', methods=['POST'])
def create_user():
    
    validacion = json.loads(User.validate_register(request.form))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 201)
    
    data = {
        "identificacion" : request.form['identificacion'],
        "nombres" : request.form['nombres'],
        "apellidos" : request.form['apellidos'],
        "email" : request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "descripcion" : request.form['descripcion'],
        "direccion" : request.form['direccion'],
        "celular" : request.form['celular'],
        "fecha_nacimiento" : request.form['fecha_nacimiento'],
        "nacionalidad" : request.form['nacionalidad'],
        "avatar" : request.files['avatar'].filename,
        "video" : request.files['video'].filename,
        "rol_id" : request.form['rol_id'],
        "genero_id" : request.form['genero_id']
    }
        
    id = User.save(data)
    
    session['user_id'] = id

    validacion['message'] = "Usuario ingresado correctamente"
    return make_response(jsonify(validacion), 201)


@app.route('/login',methods=['POST'])
def login():
    
    user = User.user_by_email(request.form)
    
    if not user:
        flash("Correo Incorrecto o Contraseña Incorrecta","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Correo Incorrecto o Contraseña incorrecta","login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    viajes_total = 0.00
    co2_total = 0.00
    user=User.get_by_id(data)
    
    data_rol ={
        'id': user.rol_id
    }
    rol = Rol.get_one(data_rol).nombre
    
    if(rol != "administrador"):
        viajes=Viaje.get_all_user(data)
        viajes_total=Viaje.get_all_count_user(data)['COUNT(*)']
        co2_total=Viaje.get_all_co2_count_user(data)['SUM(co2_total)']
    else:
        viajes=Viaje.get_all(data)
        viajes_total=Viaje.get_all_count(data)['COUNT(*)']
        co2_total=Viaje.get_all_co2_count(data)['SUM(co2_total)']
        
    return render_template("index.html",user=user,viajes=viajes,viajes_total=viajes_total,co2_total=co2_total,rol=rol)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')