from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
import decimal 
from flask_app import app
from flask_app.models.user import User
from flask_app.models.eventos import Evento
from flask_app.models.roles import Rol
from flask_app.models.generos import Genero
from flask_app.models.instrumentos import Instrumento
from flask_app.models.instrumentos_usuarios import InstrumentoUsuario
from flask_app.models.calificaciones_usuarios import CalificacionUsuario
from flask_app.models.solicitudes import Solicitud
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/registro")
def registro():
    return render_template("register.html", generos=Genero.get_all(), roles=Rol.get_all(),instrumentos=Instrumento.get_all())

@app.route('/register', methods=['POST'])
def create_user():
    
    validacion = json.loads(User.validate_register(request.form))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 400)
    
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
    
    for instrumento in request.form['instrumentos_ids']:
        print(instrumento)
        data = {
            "instrumento_id" : int(instrumento),
            "usuario_id" : int(id)
        }
        InstrumentoUsuario.save(data)
    
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

    user=User.get_by_id(data)
    
    data_rol ={
        'id': user.rol_id
    }
    rol = Rol.get_one(data_rol).nombre
    
    eventos=Evento.get_all(data)
        
    return render_template("index.html",user=user,eventos=eventos,rol=rol)

@app.route('/usuarios')
def get_usuarios():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user=User.get_by_id(data)
    
    data_rol ={
        'id': user.rol_id
    }
    rol = Rol.get_one(data_rol).nombre
    
    usuarios=User.get_all()

    return render_template("usuarios/index.html",user=user,usuarios=usuarios,rol=rol)

@app.route("/usuarios/nuevo")
def usuarios_nuevo():
    return render_template("usuarios/new.html", generos=Genero.get_all(), roles=Rol.get_all(), instrumentos=Instrumento.get_all())

@app.route('/crear/usuario', methods=['POST'])
def crear_usuario():
    
    datos = json.loads(request.data)
    usuario = datos['usuario']
    
    usuario['fecha_nacimiento'] = usuario['fecha_nacimiento'].split("T")[0]
    
    validacion = json.loads(User.validate_usuario(usuario))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 201)
    
    data = {
        "identificacion" : usuario['identificacion'],
        "nombres" : usuario['nombres'],
        "apellidos" : usuario['apellidos'],
        "email" : usuario['email'],
        "password": bcrypt.generate_password_hash(usuario['password']),
        "descripcion" : usuario['descripcion'],
        "direccion" : usuario['direccion'],
        "celular" : usuario['celular'],
        "fecha_nacimiento" : usuario['fecha_nacimiento'],
        "nacionalidad" : usuario['nacionalidad'],
        "avatar" : usuario['avatar'],
        "video" : usuario['video'],
        "rol_id" : usuario['rol_id'],
        "genero_id" : usuario['genero_id']
    }
        
    id = User.save(data)
    
    for instrumento in usuario['instrumentos_ids']:
        data = {
            "instrumento_id" : int(instrumento),
            "usuario_id" : int(id)
        }
        InstrumentoUsuario.save(data)
    
    session['user_id'] = id

    validacion['message'] = "Usuario ingresado correctamente"
    return make_response(jsonify(validacion), 201)

@app.route('/usuario/<int:id>/eliminar')
def destroy_usuario(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }   
    User.delete(data)
    return redirect('/usuarios')

@app.route('/usuario/<int:id>/editar')
def usuario_editar(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("usuarios/edit.html", generos=Genero.get_all(), roles=Rol.get_all(), id=id, instrumentos=Instrumento.get_all())

@app.route('/usuarios/obtener/<id>')
def get_usuario(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":int(id)
    }
    
    usuario_get=User.get_by_id(data)
    
    instrumentos = InstrumentoUsuario.get_by_user(data)
    instrumentos_ids = []
    for instrumento in instrumentos:
        instrumentos_ids.append(str(instrumento.instrumento_id))
        
    usuario = {
        "identificacion" : usuario_get.identificacion,
        "nombres" : usuario_get.nombres,
        "apellidos" : usuario_get.apellidos,
        "email" : usuario_get.email,
        "descripcion" : usuario_get.descripcion,
        "direccion" : usuario_get.direccion,
        "celular" : usuario_get.celular,
        "fecha_nacimiento" : str(usuario_get.fecha_nacimiento),
        "nacionalidad" : usuario_get.nacionalidad,
        "avatar" : usuario_get.avatar,
        "video" : usuario_get.video,
        "rol_id" : str(usuario_get.rol_id),
        "genero_id" : str(usuario_get.genero_id),
        "instrumentos_ids" : instrumentos_ids
    }
        

    return make_response(jsonify(
            status='ok',
            message='usuario encontrado',
            usuario= usuario
            ), 200)
    
@app.route('/editar/usuario/<id>', methods=['POST'])
def editar_usuario(id):
    
    datos = json.loads(request.data)
    usuario = datos['usuario']
    
    usuario['fecha_nacimiento'] = usuario['fecha_nacimiento'].split("T")[0]
    
    validacion = json.loads(User.validate_usuario_edit(usuario))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 400)
    
    if(usuario['password'] != ''):
        usuario['password'] = bcrypt.generate_password_hash(usuario['password'])
    else:
        data = {
            "id":int(id)
        }
        usuario_pass = User.get_by_id(data)
        usuario['password'] = usuario_pass.password
        usuario['confirm'] = usuario_pass.password
    
    data = {
        "id": int(id),
        "identificacion" : usuario['identificacion'],
        "nombres" : usuario['nombres'],
        "apellidos" : usuario['apellidos'],
        "email" : usuario['email'],
        "password": usuario['password'],
        "descripcion" : usuario['descripcion'],
        "direccion" : usuario['direccion'],
        "celular" : usuario['celular'],
        "fecha_nacimiento" : usuario['fecha_nacimiento'],
        "nacionalidad" : usuario['nacionalidad'],
        "avatar" : usuario['avatar'],
        "video" : usuario['video'],
        "rol_id" : usuario['rol_id'],
        "genero_id" : usuario['genero_id']
    }
    
    User.update(data)
    
    data_instrumentos = {
        "id":int(id)
    }
    InstrumentoUsuario.delete_by_user(data_instrumentos)
    
    for instrumento in usuario['instrumentos_ids']:
        data = {
            "instrumento_id" : int(instrumento),
            "usuario_id" : int(id)
        }
        InstrumentoUsuario.save(data)
    
    validacion['message'] = "Usuario actualizado correctamente"
    return make_response(jsonify(validacion), 201)

@app.route('/usuario/<int:id>')
def usuario_ver(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
            "id":id
    }
    usuario=User.get_by_id(data)
    
    data_genero = {
        "id":usuario.genero_id
    }
    genero = Genero.get_one(data_genero)
    
    resultado = CalificacionUsuario.get_avg(data)
    calificacion_promedio = 0
    if(resultado[0]['promedio'] is not None):
        round_num = resultado[0]['promedio']
        calificacion_promedio = decimal.Decimal(round_num).quantize(decimal.Decimal('0'), rounding=decimal.ROUND_HALF_UP)
        calificacion_promedio = int(calificacion_promedio)
    
    return render_template("usuarios/view.html", id=id, instrumentos=Instrumento.get_instrumentos_user(data), usuario=usuario, genero=genero, calificacion=calificacion_promedio)

@app.route('/usuario/<int:id>/calificar')
def usuario_calificar(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("usuarios/rating.html", id=id)

@app.route('/calificar/usuario/<id>', methods=['POST'])
def calificar_usuario(id):
    
    datos = json.loads(request.data)
    
    data = {
        "usuario_id": int(id),
        "puntuacion" : datos['calificacion']
    }
    
    CalificacionUsuario.save(data)
    
    validacion = {
        "message": "Comentario creado correctamente"
    }
    return make_response(validacion, 201)

@app.route('/usuario/<int:evento_id>/<int:usuario_id>/solicitar')
def envento_usuarios_solicitud_crear(evento_id,usuario_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "evento_id":evento_id,
        "usuario_id":usuario_id,
        "estado":"pendiente"
    }
    
    Solicitud.save(data)
    
    return redirect('/eventos/'+str(evento_id)+'/solicitar')
