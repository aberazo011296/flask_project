from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
import decimal 
from flask_app import app
from flask_app.models.user import User
from flask_app.models.eventos import Evento
from flask_app.models.roles import Rol
from flask_app.models.solicitudes import Solicitud
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/solicitudes')
def get_solicitudes():
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
    
    solicitudes=User.get_all()

    return render_template("solicitudes/index.html",user=user,solicitudes=solicitudes,rol=rol)

@app.route("/solicitudes/nuevo")
def solicitudes_nuevo():
    return render_template("solicitudes/new.html")

@app.route('/crear/solicitud', methods=['POST'])
def crear_solicitud():
    
    datos = json.loads(request.data)
    solicitud = datos['solicitud']
    
    solicitud['fecha_nacimiento'] = solicitud['fecha_nacimiento'].split("T")[0]
    
    validacion = json.loads(User.validate_solicitud(solicitud))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 201)
    
    data = {
        "identificacion" : solicitud['identificacion'],
        "nombres" : solicitud['nombres'],
        "apellidos" : solicitud['apellidos'],
        "email" : solicitud['email'],
        "password": bcrypt.generate_password_hash(solicitud['password']),
        "descripcion" : solicitud['descripcion'],
        "direccion" : solicitud['direccion'],
        "celular" : solicitud['celular'],
        "fecha_nacimiento" : solicitud['fecha_nacimiento'],
        "nacionalidad" : solicitud['nacionalidad'],
        "avatar" : solicitud['avatar'],
        "video" : solicitud['video'],
        "rol_id" : solicitud['rol_id'],
        "genero_id" : solicitud['genero_id']
    }
        
    id = User.save(data)
    
    for instrumento in solicitud['instrumentos_ids']:
        data = {
            "instrumento_id" : int(instrumento),
            "solicitud_id" : int(id)
        }
    
    session['user_id'] = id

    validacion['message'] = "Solicitud ingresado correctamente"
    return make_response(jsonify(validacion), 201)

@app.route('/solicitud/<int:id>/eliminar')
def destroy_solicitud(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }   
    User.delete(data)
    return redirect('/solicitudes')

@app.route('/solicitudes/obtener/<id>')
def get_solicitud(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":int(id)
    }
    
    solicitud_get=User.get_by_id(data)
        
    solicitud = {
        "identificacion" : solicitud_get.identificacion,
        "nombres" : solicitud_get.nombres,
        "apellidos" : solicitud_get.apellidos,
        "email" : solicitud_get.email,
        "descripcion" : solicitud_get.descripcion,
        "direccion" : solicitud_get.direccion,
        "celular" : solicitud_get.celular,
        "fecha_nacimiento" : str(solicitud_get.fecha_nacimiento),
        "nacionalidad" : solicitud_get.nacionalidad,
        "avatar" : solicitud_get.avatar,
        "video" : solicitud_get.video,
        "rol_id" : str(solicitud_get.rol_id),
        "genero_id" : str(solicitud_get.genero_id)
    }
        

    return make_response(jsonify(
            status='ok',
            message='solicitud encontrado',
            solicitud= solicitud
            ), 200)
    
@app.route('/solicitud/<int:id>')
def solicitud_ver(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":id
    }
    solicitud=User.get_by_id(data)
    
    data_genero = {
        "id":solicitud.genero_id
    }
    
    return render_template("solicitudes/view.html", id=id)
