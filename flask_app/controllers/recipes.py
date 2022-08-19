from flask import render_template,redirect,session,request, flash, url_for
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/recipe/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_recipe.html',user=User.get_by_id(data))


@app.route('/recipe/create',methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "instrucciones": request.form["instrucciones"],
        "bajotiempo": int(request.form["bajotiempo"]),
        "fecha_elaboracion": request.form["fecha_elaboracion"],
        "usuario_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_recipe.html",edit=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/recipe/update',methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(url_for("edit_recipe", id=int(request.form['id'])))
    data = {
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "instrucciones": request.form["instrucciones"],
        "bajotiempo": int(request.form["bajotiempo"]),
        "fecha_elaboracion": request.form["fecha_elaboracion"],
        "id": request.form['id']
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_recipe.html",recipe=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/recipe/destroy/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')