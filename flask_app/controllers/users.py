from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user_form(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.add_user(data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.validate_user_login(request.form)
    if not user:
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/user/account')
def read_user():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('read_user.html', games=User.get_user_with_games({'id': session['user_id']}), user=User.get_user_by_id({'id': session['user_id']}))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')