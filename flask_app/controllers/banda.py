from flask import render_template, redirect, session, request, flash, jsonify, make_response, url_for
import json
import os
# import urllib.request
import decimal
from flask_app import app
from flask_app.models.bandas import Bandas
from flask_app.models.user import User
from flask_app.models.eventos import Evento
from flask_app.models.roles import Rol
from flask_app.models.generos import Genero
from flask_app.models.instrumentos import Instrumento
from flask_app.models.instrumentos_usuarios import InstrumentoUsuario
from werkzeug.utils import secure_filename
from flask_app.models.calificaciones_bandas import CalificacionBanda
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'

UPLOAD_FOLDER = 'flask_app/static/imgs/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) #ya esta en el front/no


@app.route('/bandas')
def banda():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    usuario = User.get_by_id(data)
    data_rol = {
        "id": usuario.rol_id
    }
    rol = Rol.get_one(data_rol).nombre
    
    if(rol != 'administrador'):
        bandas=Bandas.get_all_by_user(data)
        print(rol)
    else:
        bandas=Bandas.get_all()
    
    return render_template('bandas/index.html',bandas=bandas,rol=rol,user=usuario)

@app.route('/new/banda')
def new_banda():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('bandas/new_banda.html',user=User.get_by_id(data),generos=Genero.get_all())


@app.route('/create/banda',methods=['POST'])
def create_banda():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bandas.validate_banda(request.form):
        return redirect('/new/banda')
    
    if 'avatar' not in request.files:
        flash('No file part')

    file = request.files['avatar']
    if file.filename == '':
        flash ('No hay imagen selecionada para subir')

    if file and allowed_file_bandas (file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    else:
        flash('Imagenes aceptadas - png, etc')

    data = {
        "nombre": request.form["nombre"],
        "num_integrantes": request.form["num_integrantes"],
        "video": request.files["video"].filename,
        "avatar": request.files["avatar"].filename,
        "celular": request.form["celular"],
        "email": request.form["email"],
        "genero_id": request.form["genero_id"],
        "usuario_id": session["user_id"]
        
    }
    Bandas.save(data)
    return redirect('/bandas')

@app.route('/edit/banda/<int:id>')
def edit_banda(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("bandas/edit_banda.html",edit=Bandas.get_one(data),user=User.get_by_id(user_data),generos=Genero.get_all())


@app.route('/update/banda',methods=['POST'])
def update_banda():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bandas.validate_banda(request.form):
        return redirect('/new/banda')

    if 'avatar' not in request.files:
        flash('No file part')

    file = request.files['avatar']
    if file.filename == '':
        flash ('No hay imagen selecionada para subir')

    if file and allowed_file_bandas (file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    else:
        flash('Imagenes aceptadas - png, etc')
    data = {
        "nombre": request.form["nombre"],
        "num_integrantes": request.form["num_integrantes"],
        "avatar": request.files["avatar"].filename,
        "video": request.files["video"].filename,
        "celular": request.form["celular"],
        "email": request.form["email"],
        "genero_id": request.form["genero_id"],
        "id": int(request.form["id"]),
        "usuario_id": session["user_id"]
    }
    Bandas.update(data)
    return redirect('/bandas')

@app.route('/destroy/banda/<int:id>')
def destroy_banda(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Bandas.destroy(data)
    return redirect('/bandas')


@app.route('/banda/<int:id>')
def show_banda(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    resultado = CalificacionBanda.get_avg(data)
    calificacion_promedio = 0
    if(resultado[0]['promedio'] is not None):
        round_num = resultado[0]['promedio']
        calificacion_promedio = decimal.Decimal(round_num).quantize(decimal.Decimal('0'), rounding=decimal.ROUND_HALF_UP)
        calificacion_promedio = int(calificacion_promedio)

    return render_template("bandas/view.html",banda=Bandas.get_one(data),user=User.get_by_id(user_data),generos=Genero.get_all(),calificacion=calificacion_promedio)

#--------------------CALIFICACION--------------------------------

@app.route('/banda/<int:id>/calificar')
def banda_calificar(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("bandas/rating_banda.html", id=id)

@app.route('/calificar/banda/<id>', methods=['POST'])
def calificar_banda(id):
    
    datos = json.loads(request.data)
    
    data = {
        "banda_id": int(id),
        "puntuacion" : datos['calificacion']
    }
    
    CalificacionBanda.save(data)
    
    validacion = {
        "message": "Comentario creado correctamente"
    }
    return make_response(validacion, 201)

#imagenes:
def allowed_file_bandas(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/display_bandas/<filename>')
def display_image_bandas(filename):
    return redirect(url_for('static', filename = 'imgs/' + filename), code=301)
