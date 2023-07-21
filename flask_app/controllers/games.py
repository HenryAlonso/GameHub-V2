from flask import render_template, redirect, request, session
from trees_app import app
from trees_app.models.user import User
from trees_app.models.tree import Tree

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("dashboard.html", user = user, trees = Tree.retrieve_all())

@app.route('/new/tree')
def add_tree():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("trees_new.html", user = user)


@app.route('/tree/edit/<int:id>')
def edit_tree(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("trees_edit.html", user = user, tree = Tree.retrieve_by_id({"id": id}))

@app.route('/show/<int:id>')
def show_tree(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("trees_info.html", user = user, tree = Tree.retrieve_by_id({"id": id}))

@app.route('/new/tree/process', methods = ["POST"])
def process_new_tree():
    if 'user_id' not in session:
        return redirect('/')
    if not Tree.validate_tree_form(request.form):
        return redirect('/new/tree')
    data = {
        'user_id': session['user_id'],
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date_planted': request.form['date_planted'],
    }
    Tree.new_tree(data)
    return redirect('/dashboard')

@app.route('/tree/update/process/<int:id>', methods = ["POST"])
def process_update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Tree.validate_tree_form(request.form):
        return redirect(f'/tree/edit/{id}')
    data = {
        "id": id,
        "species": request.form['species'],
        "location": request.form['location'],
        "reason": request.form['reason'],
        "date_planted": request.form['date_planted']
    }
    Tree.re_plant(data)
    return redirect('/dashboard')

@app.route('/tree/delete/<int:id>')
def remove_tree(id):
    if 'user_id' not in session:
        return redirect('/')
    Tree.remove_tree({"id":id})
    user = User.get_user_by_id({"id": session['user_id']})
    return redirect(f'/user/account/{user.id}')