from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.viaje import Viaje
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/registro")
def registro():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def create_user():
    
    validacion = json.loads(User.validate_register(request.form))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 201)
    
    data = {
        "nombre": request.form["nombre"],
        "nombre_usuario" : request.form["nombre_usuario"],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "rol" : request.form["rol"],
        "area" : request.form["area"]
    }
        
    id = User.save(data)
    session['user_id'] = id

    validacion['message'] = "Usuario ingresado correctamente"
    return make_response(jsonify(validacion), 201)


@app.route('/login',methods=['POST'])
def login():
    user = User.user_by_nombre_usuario(request.form)

    if not user:
        flash("Correo Incorrecto o Contraseña incorrecta","login")
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
    
    if(user.rol != "administrador"):
        viajes=Viaje.get_all_user(data)
        viajes_total=Viaje.get_all_count_user(data)['COUNT(*)']
        co2_total=Viaje.get_all_co2_count_user(data)['SUM(co2_total)']
    else:
        viajes=Viaje.get_all(data)
        viajes_total=Viaje.get_all_count(data)['COUNT(*)']
        co2_total=Viaje.get_all_co2_count(data)['SUM(co2_total)']
        
    return render_template("index.html",user=user,viajes=viajes,viajes_total=viajes_total,co2_total=co2_total)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')