from flask import render_template, redirect, session, request, flash, jsonify, make_response
from flask_mail import Mail, Message
import json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.eventos import Evento
from flask_app.models.roles import Rol
from flask_app.models.solicitudes import Solicitud
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '1871b9f82c95e8'
app.config['MAIL_PASSWORD'] = '57386b31c1dd4f'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

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
    
    solicitudes_musico=Solicitud.get_all(data)
    solicitudes_creador_eventos=Solicitud.get_all_eventos_usuario(data)

    return render_template("solicitudes/usuario_index.html",user=user,solicitudes_musico=solicitudes_musico,solicitudes_creador_eventos=solicitudes_creador_eventos,rol=rol)

@app.route("/solicitudes/nuevo")
def solicitudes_nuevo():
    return render_template("solicitudes/new.html")

@app.route('/editar/solicitud/<evento_id>/<usuario_id>', methods=['POST'])
def editar_solicitud(evento_id,usuario_id):
    
    datos = json.loads(request.data)
    estado = datos['estado']
    num_integrantes = datos['num_integrantes']
    integrantes = 0
    
    data_eventos = {
        "id": int(evento_id)
    }
    
    integrantes = Solicitud.get_all_by_evento(data_eventos)
    
    if( int(integrantes) >  int(num_integrantes) and estado == 'aceptado'):
        estado = 'cancelado (cupo)'
        data = {
            "evento_id": int(evento_id),
            "usuario_id": int(usuario_id),
            "estado" : estado
        }
            
        Solicitud.update(data)
    
        return make_response(jsonify(
            status='ok',
            message='Evento llenó su cupo',
            evento_id= evento_id,
            usuario_id= usuario_id,
        ), 201)
    
    data = {
        "evento_id": int(evento_id),
        "usuario_id": int(usuario_id),
        "estado" : estado
    }
        
    Solicitud.update(data)
    
    data_evento = {
        "id": int(evento_id)
    }
    evento = Evento.get_one(data_evento)
    
    data_usuario = {
        "id": int(usuario_id)
    }
    usuario = User.get_by_id(data_usuario)
    
    data_usuario_evento = {
        "id": int(evento.usuario_id)
    }
    usuario_evento = User.get_by_id(data_usuario_evento)
    
    msg = Message('Solicitud del evento '+evento.titulo, sender = 'music_events@mailtrap.io', recipients = [usuario.email])
    msg.html = "<b>"+usuario.nombres+",</b><br><br>La solicitud se encuentra en estado: <b>"+estado+"</b><br><br><b>Datos del Evento: </b><br>"+"<b>Nombre: </b>"+evento.titulo+"<br><b>Fecha: </b>"+str(evento.fecha)+"<br><b>Hora Inicio: </b>"+str(evento.hora_inicio)+"<br><b>Hora Fin: </b>"+str(evento.hora_fin)+"<br><br>Saludos,<br><br>MusicEvents"
    mail.send(msg)
    
    msg1 = Message('Solicitud del evento '+evento.titulo, sender = 'music_events@mailtrap.io', recipients = [usuario_evento.email])
    msg1.html = "<b>"+usuario_evento.nombres+",</b><br><br>La solicitud del usuario "+usuario.nombres+" se encuentra en estado: <b>"+estado+"</b><br><br><b>Datos del Evento: </b><br>"+"<b>Nombre: </b>"+evento.titulo+"<br><b>Fecha: </b>"+str(evento.fecha)+"<br><b>Hora Inicio: </b>"+str(evento.hora_inicio)+"<br><b>Hora Fin: </b>"+str(evento.hora_fin)+"<br><br>Saludos,<br><br>MusicEvents"
    mail.send(msg1)
    
    return make_response(jsonify(
            status='ok',
            message='solicitud actualizada',
            evento_id= evento_id,
            usuario_id= usuario_id,
        ), 201)

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
