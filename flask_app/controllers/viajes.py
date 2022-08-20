from flask import render_template,redirect,session,request, flash, url_for
from flask_app import app
from flask_app.models.viaje import Viaje
from flask_app.models.user import User


@app.route('/viaje/new')
def new_viaje():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_viaje.html',user=User.get_by_id(data))


@app.route('/viaje/create',methods=['POST'])
def create_viaje():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Viaje.validate_viaje(request.form):
        return redirect('/viaje/new')
    data = {
        "destino": request.form["destino"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"],
        "plan": request.form["plan"]
    }
    
    id_viaje = Viaje.save(data)
    
    data_usuarios_viajes = {
        "usuario_id": session["user_id"],
        "viaje_id": id_viaje
    }
    
    Viaje.add_usuarios_viajes(data_usuarios_viajes)
    
    return redirect('/dashboard')

@app.route('/viaje/edit/<int:id>')
def edit_viaje(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_viaje.html",edit=Viaje.get_one(data),user=User.get_by_id(user_data))

@app.route('/viaje/update',methods=['POST'])
def update_viaje():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Viaje.validate_viaje(request.form):
        return redirect(url_for("edit_viaje", id=int(request.form['id'])))
    data = {
        "destino": request.form["destino"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"],
        "plan": request.form["plan"],
        "fecha_elaboracion": request.form["fecha_elaboracion"],
        "id": request.form['id']
    }
    Viaje.update(data)
    return redirect('/dashboard')

@app.route('/viaje/<int:id>')
def show_viaje(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    viajes_otros = {
        "usuario_id":session['user_id'],
        "viaje_id":id
    }
    usuarios_viaje_otros = User.get_by_viaje_otros(viajes_otros)
    
    return render_template("show_viaje.html",viaje=Viaje.get_one(data),user=User.get_by_id(user_data),usuarios_viaje_otros=usuarios_viaje_otros)

@app.route('/viaje/join',methods=['POST'])
def join_viaje():

    if 'user_id' not in session:
        return redirect('/logout')
    
    data_usuarios_viajes = {
        "usuario_id": session["user_id"],
        "viaje_id": request.form["viaje_id"]
    }
    
    print('llego')
    
    Viaje.add_usuarios_viajes(data_usuarios_viajes)
    
    return redirect('/dashboard')

@app.route('/viaje/destroy/<int:id>')
def destroy_viaje(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Viaje.destroy(data)
    return redirect('/dashboard')