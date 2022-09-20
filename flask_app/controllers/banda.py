from flask import render_template, redirect, session, request, flash, jsonify, make_response
import json
from flask_app import app
from flask_app.models.bandas import Bandas
from flask_app.models.user import User
from flask_app.models.eventos import Evento
from flask_app.models.roles import Rol
from flask_app.models.generos import Genero
from flask_app.models.instrumentos import Instrumento
from flask_app.models.instrumentos_usuarios import InstrumentoUsuario
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'


@app.route('/bandas')
def banda():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('bandas/index.html',bandas=Bandas.get_all())

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
    data = {
        "nombre": request.form["nombre"],
        "num_integrantes": request.form["num_integrantes"],
        "video": request.form["video"],
        "avatar": request.form["avatar"],
        "celular": request.form["celular"],
        "email": request.form["email"],
        "genero_id": request.form["genero_id"]
        
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
    return render_template("edit_banda.html",edit=Bandas.get_one(data),user=User.get_by_id(user_data),generos=Genero.get_all())


@app.route('/update/banda',methods=['POST'])
def update_banda():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bandas.validate_banda(request.form):
        return redirect('/new/banda')
    data = {

        "nombre": request.form["nombre"],
        "num_integrantes": request.form["num_integrantes"],
        "video": request.form["video"],
        "avatar": request.form["avatar"],
        "celular": request.form["celular"],
        "email": request.form["email"],
        "genero_id": request.form["genero_id"],
        "user_id": session["user_id"]
    }
    Bandas.update(data)
    return redirect('/dashboard')

@app.route('/destroy/banda/<int:id>')
def destroy_banda(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Bandas.destroy(data)
    return redirect('/dashboard')


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
    return render_template("bandas/view.html",banda=Bandas.get_one(data),user=User.get_by_id(user_data),generos=Genero.get_all())

