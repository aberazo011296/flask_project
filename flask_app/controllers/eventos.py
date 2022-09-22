from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
import decimal
from flask_app import app
from flask_app.models.user import User
from flask_app.models.eventos import Evento
from flask_app.models.roles import Rol
from flask_app.models.generos import Genero
from flask_app.models.instrumentos import Instrumento
from flask_app.models.eventos_instrumentos import InstrumentoEvento
from flask_app.models.calificaciones_eventos import CalificacionEvento
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

@app.route("/eventos")
def eventos():
    return render_template ("eventos/index_eventos.html", eventos=Evento.get_all())

@app.route("/eventos/nuevo")
def eventos_nuevo():
    return render_template("eventos/registro_eventos.html",generos=Genero.get_all(),instrumentos=Instrumento.get_all())

@app.route('/crear/evento', methods=['POST'])
def crear_evento():
    
    datos = json.loads(request.data)
    eventos = datos['eventos']
    
    eventos['fecha'] = eventos['fecha'].split("T")[0]
    
    validacion = json.loads(Evento.validate_eventos(eventos))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 201)
    
    data = {
        "titulo" : eventos['titulo'],
        "direccion" : eventos['direccion'],
        "fecha" : eventos['fecha'],
        "hora_inicio" : eventos['hora_inicio'],
        "hora_fin" : eventos['hora_fin'],
        "opciones" : eventos['opciones'],
        "genero_id" : eventos['genero_id'],
        "usuario_id": int(session['user_id'])
    }
        
    id = Evento.save(data)

    
    for instrumento in eventos['instrumentos_ids']:
        data = {
            "instrumento_id" : int(instrumento),
            "evento_id" : int(id)
        }
        InstrumentoEvento.save(data)

    validacion['message'] = "Evento creado correctamente"
    return make_response(jsonify(validacion), 201)

@app.route('/eventos/<id>/solicitar')
def envento_usuarios_solicitud(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id": int(id),
        "usuario_id": int(session['user_id'])
    }

    return render_template("solicitudes/index.html", id_evento=id, usuarios=User.get_all_sin_solicitud(data))

    #EDIT.......

@app.route('/eventos/<int:id>/editar')
def evento_editar(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("eventos/edit_evento.html", generos=Genero.get_all(), id=id, instrumentos=Instrumento.get_all())

@app.route('/eventos/obtener/<id>')
def get_evento(id):
    print("HOLAAAA")

    
    data = {
        "id":int(id)
    }
    print("HOLAAAA")
    evento_get=Evento.get_one(data)
    
    instrumentos = InstrumentoEvento.get_by_evento(data)
    instrumentos_ids = []
    for instrumento in instrumentos:
        instrumentos_ids.append(str(instrumento.instrumento_id))
    print("HOLAAAA")
    evento = {
        "titulo" : evento_get.titulo,
        "direccion" : evento_get.direccion,
        "fecha" : str(evento_get.fecha),
        "hora_inicio" : str(evento_get.hora_inicio),
        "hora_fin" : str(evento_get.hora_fin),
        "opciones" : evento_get.opciones,
        "genero_id" : str(evento_get.genero_id),
        "instrumentos_ids" : instrumentos_ids
    }
        

    return make_response(jsonify(
            status='ok',
            message='Evento encontrado',
            evento= evento
            ), 200)
    #guardar base de datos

@app.route('/editar/eventos/<id>', methods=['POST'])
def editar_evento(id):
    print("holaaaaaa")
    print(id)
    datos = json.loads(request.data)
    evento = datos['evento']
    
    evento['fecha'] = evento['fecha'].split("T")[0]
    
    validacion = json.loads(Evento.validate_eventos(evento))
    
    if not validacion['valid']:
        return make_response(jsonify(validacion), 400)
    
    
    data = {
        "titulo" : evento['titulo'],
        "direccion" : evento['direccion'],
        "fecha" : evento['fecha'],
        "hora_inicio" : evento['hora_inicio'],
        "hora_fin" : evento['hora_fin'],
        "opciones" : evento['opciones'],
        "genero_id" : evento['genero_id'],
        "usuario_id" :int(session['user_id']),
        "id" : id
    }
        
    Evento.update(data)
    
    data_instrumentos = {
        "id":id
    }
    InstrumentoEvento.delete_by_evento(data_instrumentos)
    print("holaaaaaaaa")
    print(evento['instrumentos_ids'])
    for instrumento in evento['instrumentos_ids']:
        data = {
            "instrumento_id" : int(instrumento),
            "evento_id" : id
        }
        InstrumentoEvento.save(data)
    
    validacion['message'] = "Evento actualizado correctamente"
    return make_response(jsonify(validacion), 201)

@app.route('/eventos/<id>/eliminar')
def eliminar_evento(id):
    data = {
            "evento_id" : int(id)
        
        }
    Evento.delete(data)
    return redirect ("/eventos")

    #VER EVENTO

@app.route('/eventos/<int:id>')
def evento_ver(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
            "id":id
    }
    evento=Evento.get_one(data)
    
    data_genero = {
        "id":evento.genero_id
    }
    genero = Genero.get_one(data_genero)
    
    resultado = CalificacionEvento.get_avg(data)
    calificacion_promedio = 0
    if(resultado[0]['promedio'] is not None):
        round_num = resultado[0]['promedio']
        calificacion_promedio = decimal.Decimal(round_num).quantize(decimal.Decimal('0'), rounding=decimal.ROUND_HALF_UP)
        calificacion_promedio = int(calificacion_promedio)
    
    return render_template("eventos/view_evento.html", id=id, instrumentos=Instrumento.get_instrumentos_evento(data), evento=evento, genero=genero, calificacion=calificacion_promedio)

    #Calificar Evento

@app.route('/eventos/<int:id>/calificar')
def evento_calificar(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("eventos/rating_evento.html", id=id)

@app.route('/calificar/evento/<id>', methods=['POST'])
def calificar_evento(id):
    
    datos = json.loads(request.data)
    
    data = {
        "evento_id": int(id),
        "puntuacion" : datos['calificacion']
    }
    
    CalificacionEvento.save(data)
    
    validacion = {
        "message": "Comentario creado correctamente"
    }
    return make_response(validacion, 201)