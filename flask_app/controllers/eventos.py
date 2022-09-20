from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.eventos import Evento
from flask_app.models.roles import Rol
from flask_app.models.generos import Genero
from flask_app.models.instrumentos import Instrumento
from flask_app.models.eventos_instrumentos import InstrumentoEvento
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
        "genero_id" : eventos['genero_id']
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
        "id": int(id)
    }

    return render_template("solicitudes/index.html", id_evento=id, usuarios=User.get_all_sin_solicitud(data))