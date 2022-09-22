from flask import render_template, redirect, session, request, flash, jsonify, make_response
from flask_mail import Mail, Message
import json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.bandas import Bandas
from flask_app.models.roles import Rol
from flask_app.models.solicitudes_bandas import Solicitud_Banda
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

@app.route('/solicitudes_bandas')
def get_solicitudes_bandas():
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
    
    solicitudes_musico=Solicitud_Banda.get_all(data)
    solicitudes_creador_bandas=Solicitud_Banda.get_all_bandas_usuario(data)

    return render_template("solicitudes_banda/banda_index.html",user=user,solicitudes_musico=solicitudes_musico,solicitudes_creador_bandas=solicitudes_creador_bandas,rol=rol)

@app.route("/solicitudes_banda/nuevo")
def solicitudes_banda_nuevo():
    return render_template("solicitudes_banda/new.html")

@app.route('/editar/solicitud_banda/<banda_id>/<usuario_id>', methods=['POST'])
def editar_solicitud_banda(banda_id,usuario_id):
    
    datos = json.loads(request.data)
    estado = datos['estado']
    num_integrantes = datos['num_integrantes']
    integrantes = 0
    
    data_bandas = {
        "id": int(banda_id)
    }
    
    integrantes = Solicitud_Banda.get_all_by_banda(data_bandas)
    
    if( int(integrantes) >  int(num_integrantes) and estado == 'aceptado'):
        
        data = {
            "banda_id": int(banda_id),
            "usuario_id": int(usuario_id),
            "estado" : 'cancelado (cupo)'
        }
            
        Solicitud_Banda.update(data)
    
        return make_response(jsonify(
            status='ok',
            message='banda llenó su cupo',
            banda_id= banda_id,
            usuario_id= usuario_id,
        ), 201)
    
    data = {
        "banda_id": int(banda_id),
        "usuario_id": int(usuario_id),
        "estado" : estado
    }
        
    Solicitud_Banda.update(data)
    
    data_banda = {
        "id": int(banda_id)
    }
    banda = Bandas.get_one(data_banda)
    
    data_usuario = {
        "id": int(usuario_id)
    }
    usuario = User.get_by_id(data_usuario)
    
    data_usuario_banda = {
        "id": int(banda.usuario_id)
    }
    usuario_banda = User.get_by_id(data_usuario_banda)
    
    msg = Message('Solicitud del banda '+banda.nombre, sender = 'music_events@mailtrap.io', recipients = [usuario.email])
    msg.html = "<b>"+usuario.nombres+",</b><br><br>La solicitud se encuentra en estado: <b>"+estado+"</b><br><br><b>Datos del banda: </b><br>"+"<b>Nombre: </b>"+banda.nombre+"<br><b>Celular: </b>"+str(banda.celular)+"<br><b>Numero de Integrantes: </b>"+str(banda.num_integrantes)+"<br><br>Saludos,<br><br>MusicEvents"
    mail.send(msg)
    
    msg1 = Message('Solicitud del banda '+banda.nombre, sender = 'music_events@mailtrap.io', recipients = [usuario_banda.email])
    msg1.html = "<b>"+usuario_banda.nombres+",</b><br><br>La solicitud del usuario "+usuario.nombres+" se encuentra en estado: <b>"+estado+"</b><br><br><b>Datos de la banda: </b><br>"+"<b>Nombre: </b>"+banda.nombre+"<br><b>Numero de integrantes: </b>"+str(banda.num_integrantes)+"<br><b>Celular: </b>"+str(banda.celular)+"<br><br>Saludos,<br><br>MusicEvents"
    mail.send(msg1)
    
    return make_response(jsonify(
            status='ok',
            message='solicitud actualizada',
            banda_id= banda_id,
            usuario_id= usuario_id,
        ), 201)

@app.route('/solicitud_banda/<int:id>/eliminar')
def destroy_solicitud_banda(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }   
    User.delete(data)
    return redirect('/solicitudes_bandas')

@app.route('/solicitudes_bandas/obtener/<id>')
def get_solicitud_banda(id):
    
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
    
@app.route('/solicitud_banda/<int:id>')
def solicitud_ver_banda(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":id
    }
    solicitud=User.get_by_id(data)
    
    data_genero = {
        "id":solicitud.genero_id
    }
    
    return render_template("solicitudes_banda/view.html", id=id)



@app.route('/usuario/<int:banda_id>/<int:usuario_id>/solicitar_banda')
def banda_usuarios_solicitud_crear(banda_id,usuario_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "banda_id":banda_id,
        "usuario_id":usuario_id,
        "estado":"pendiente"
    }
    
    Solicitud_Banda.save(data)
    
    data_banda = {
        "id": int(banda_id)
    }
    banda = Bandas.get_one(data_banda)
    
    data_usuario = {
        "id": int(usuario_id)
    }
    usuario = User.get_by_id(data_usuario)
    
    data_usuario_banda = {
        "id": int(banda.usuario_id)
    }
    usuario_banda = User.get_by_id(data_usuario_banda)
    
    msg1 = Message('Solicitud del banda '+banda.nombre, sender = 'music_events@mailtrap.io', recipients = [usuario_banda.email])
    msg1.html = "<b>"+usuario_banda.nombres+",</b><br><br>El usuario "+ usuario.nombres +", "+ usuario.email +" ha solicitado unirse a: <br><br><b>Datos del banda: </b><br>"+"<b>Nombre: </b>"+banda.nombre+"<br><b>Celular: </b>"+str(banda.celular)+"<br><b>Numero de integrantes: </b>"+str(banda.num_integrantes)+"<br><br>Por favor ingresar a la aplicación para aceptar o negar la solicitud.<br><br>Saludos,<br><br>MusicEvents"
    mail.send(msg1)
    
    return redirect('/bandas/'+str(banda_id)+'/solicitar')

@app.route('/dashboard_banda/<int:banda_id>/<int:usuario_id>/solicitar')
def banda_usuarios_solicitud_dashboard(banda_id,usuario_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "banda_id":banda_id,
        "usuario_id":usuario_id,
        "estado":"pendiente"
    }
    
    Solicitud_Banda.save(data)
    
    data_banda = {
        "id": int(banda_id)
    }
    banda = Bandas.get_one(data_banda)
    
    data_usuario = {
        "id": int(usuario_id)
    }
    usuario = User.get_by_id(data_usuario)
    
    data_usuario_banda = {
        "id": int(banda.usuario_id)
    }
    usuario_banda = User.get_by_id(data_usuario_banda)
    
    msg1 = Message('Solicitud del banda '+banda.nombre, sender = 'music_events@mailtrap.io', recipients = [usuario_banda.email])
    msg1.html = "<b>"+usuario_banda.nombres+",</b><br><br>El usuario "+ usuario.nombres +", "+ usuario.email +" ha solicitado unirse a: <br><br><b>Datos del banda: </b><br>"+"<b>Nombre: </b>"+banda.nombre+"<br><b>Numero de Integrantes: </b>"+str(banda.num_integrantes)+"<br><b>Celular: </b>"+str(banda.celular)+"<br><br>Por favor ingresar a la aplicación para aceptar o negar la solicitud.<br><br>Saludos,<br><br>MusicEvents"
    mail.send(msg1)
    
    return redirect('/dashboard_bandas')

@app.route('/dashboard_bandas')
def dashboard_bandas():
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
    
    bandas_ok=Bandas.get_all_by_user_ok(data)
    bandas_new=Bandas.get_all_by_user_new(data)
        
    return render_template("index_banda.html",user=user,bandas_ok=bandas_ok,bandas_new=bandas_new,rol=rol)


@app.route('/bandas/<id>/solicitar')
def banda_usuarios_solicitud(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id": int(id),
        'usuario_id':session['user_id']
    }
    
    data_user={
        'id':session['user_id']
    }
    user=User.get_by_id(data_user)

    data_rol={
        'id':user.rol_id
    }
    rol=Rol.get_one(data_rol).nombre

    return render_template("solicitudes_banda/index.html", id_banda=id, usuarios=User.get_all_sin_solicitud_bandas(data),user=user,rol=rol)
