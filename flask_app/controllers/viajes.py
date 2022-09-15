from logging import NullHandler
from flask import render_template,redirect,session,request, flash, url_for, jsonify, make_response
from flask_app import app
import json
import calendar
from flask_app.models.viaje import Viaje
from flask_app.models.user import User
from flask_app.models.medios_transporte import MediosTransporte
from flask_app.models.roles import Rol
from flask_app.models.generos import Genero
from flask_app.models.tramos import Tramos


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
        "pasajero_identificacion": request.form["pasajero_identificacion"],
        "pasajero_nombre": request.form["pasajero_nombre"],
        "descripcion": request.form["descripcion"],
        "usuario_id": session['user_id']
    }
    
    id_viaje = Viaje.save(data)
    
    return redirect('/viaje/tramos/'+str(id_viaje))

@app.route('/viaje/tramos/<id>')
def tramos_viaje(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":int(id)
    }
    return render_template("tramos.html",viaje=Viaje.get_one(data),medios_transporte=MediosTransporte.get_all(data))

@app.route('/viaje/<int:id>/editar')
def edit_viaje(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    return render_template("edit_viaje.html",viaje=Viaje.get_one(data),user=User.get_by_id(user_data))

@app.route('/viaje/edit',methods=['POST'])
def update_viaje():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Viaje.validate_viaje(request.form):
        return redirect(url_for("update_viaje", id=int(request.form['id'])))
    data = {
        "pasajero_identificacion": request.form["pasajero_identificacion"],
        "pasajero_nombre": request.form["pasajero_nombre"],
        "descripcion": request.form["descripcion"],
        "usuario_id": session['user_id'],
        "id": request.form["id"]
    }
    Viaje.update(data)
    return redirect('/viaje/tramos/'+str(request.form['id'])+'/editar')

@app.route('/viaje/tramos/<id>/editar')
def tramos_viaje_edit(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":int(id)
    }
    
    return render_template("edit_tramos.html",viaje=Viaje.get_one(data),medios_transporte=MediosTransporte.get_all(data))

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
    Tramos.delete(data)
    Viaje.delete(data)
    return redirect('/dashboard')

@app.route('/viajes-anuales')
def viajes_totales():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data_usuario ={
        'id': session['user_id']
    }
    user=User.get_by_id(data_usuario)
    
    viajes_totales = []
    
    for mes in range(12):
        ultimo_dia_mes = calendar.monthrange(2022, mes+1)[1]
        print(ultimo_dia_mes)
        data = {
            "inicio_mes": "2022"+"-"+str(mes+1)+"-"+"01",
            "fin_mes": "2022"+"-"+str(mes+1)+"-"+str(ultimo_dia_mes),
            'id': session['user_id']
        }
        
        data_rol ={
            'id': user.rol_id
        }
        rol = Rol.get_one(data_rol).nombre
        
        if(rol != "administrador"):
            valor = Viaje.get_month_user(data)['COUNT(*)']
        else:
            valor = Viaje.get_month(data)['COUNT(*)']

        viajes_totales.append(int(valor))

    return make_response(jsonify(
            status='ok',
            message='Viajes totales correcto',
            viajes=viajes_totales
            ), 200)

@app.route('/co2-anuales')
def co2_totales():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data_usuario ={
        'id': session['user_id']
    }
    user=User.get_by_id(data_usuario)
    
    co2_totales = []

    for mes in range(12):
        ultimo_dia_mes = calendar.monthrange(2022, mes+1)[1]
        print(ultimo_dia_mes)
        data = {
            "inicio_mes": "2022"+"-"+str(mes+1)+"-"+"01",
            "fin_mes": "2022"+"-"+str(mes+1)+"-"+str(ultimo_dia_mes),
            'id': session['user_id']
        }
        
        data_rol ={
            'id': user.rol_id
        }
        rol = Rol.get_one(data_rol).nombre
        
        if(rol != "administrador"):
            valor = Viaje.get_month_co2_user(data)['SUM(co2_total)']
        else:
            valor = Viaje.get_month_co2(data)['SUM(co2_total)']
        
        if(valor is None):
            co2_totales.append(0)
        else:
            co2_totales.append(int(valor))
        

    return make_response(jsonify(
            status='ok',
            message='Viajes totales correcto',
            co2=co2_totales
            ), 200)

@app.route('/medio-transporte/<id>')
def get_medio_transporte(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":int(id)
    }
    
    medio_transporte = MediosTransporte.get_one(data)

    return make_response(jsonify(
            status='ok',
            message='Co2 por KM Medio de transporte ok',
            co2_x_km=medio_transporte.co2_x_km
            ), 200)
    
@app.route('/tramos/create',methods=['POST'])
def create_tramos():
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    datos = json.loads(request.data)
    viaje = datos['viaje']
    tramos = viaje['tramos']
    
    data_editar = {
        "km_total": viaje['km_totales'],
        "co2_total": viaje['co2_totales'],
        "id": viaje['viaje_id']
    }
    
    Viaje.edit_totales(data_editar)

    data_eliminar = {
        "id": viaje['viaje_id']
    }
    
    Tramos.delete(data_eliminar)
    
    cont = 1
    for tramo in tramos:
        data = {
            "posicion": cont,
            "origen": tramo['origen'],
            "destino": tramo['destino'],
            "km": tramo['km'],
            "co2": tramo['co2'],
            "viaje_id": viaje['viaje_id'],
            "medio_transporte_id": tramo['medio_transporte_id']
        }
        cont += 1
        
        Tramos.save(data)
    
    return make_response(jsonify(
            status='ok',
            message='Tramos guardados',
            ), 200)
    
@app.route('/tramos/update',methods=['POST'])
def update_tramos():
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    datos = json.loads(request.data)
    viaje = datos['viaje']
    tramos = viaje['tramos']
    
    data_editar = {
        "km_total": viaje['km_totales'],
        "co2_total": viaje['co2_totales'],
        "id": viaje['viaje_id']
    }
    
    Viaje.edit_totales(data_editar)

    data_eliminar = {
        "id": viaje['viaje_id']
    }
    
    Tramos.delete(data_eliminar)
    
    cont = 1
    for tramo in tramos:
        data = {
            "posicion": cont,
            "origen": tramo['origen'],
            "destino": tramo['destino'],
            "km": tramo['km'],
            "co2": tramo['co2'],
            "viaje_id": viaje['viaje_id'],
            "medio_transporte_id": tramo['medio_transporte_id']
        }
        cont += 1
        
        Tramos.save(data)
    
    return make_response(jsonify(
            status='ok',
            message='Tramos guardados',
            ), 200)

@app.route('/tramos/obtener/<id>')
def get_tramos_viaje(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "id":int(id)
    }
    
    tramos = [];
    
    tramos_viaje=Tramos.get_all_viaje(data)

    for x in tramos_viaje:
        tramo = {
            "posicion": x.posicion,
            "origen": x.origen,
            "destino": x.destino,
            "km": float(x.km),
            "co2": float(x.co2),
            "viaje_id": x.viaje_id,
            "medio_transporte_id": x.medio_transporte_id
        }
        
        tramos.append(tramo)

    return make_response(jsonify(
            status='ok',
            message='Tramos de un viaje',
            tramos= tramos
            ), 200)