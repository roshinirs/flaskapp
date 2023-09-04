from flask import request, redirect, url_for, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from server.server import obj


class AuthService:
    def login(self):
        if request.method == 'POST':
            users = obj.dbconnect.users
            login_user = users.find_one({'username': request.form['username']})

            if login_user:
                if check_password_hash(login_user['password'], request.form['password']):
                    session['username'] = request.form['username']
                    return redirect(url_for('auth.index'))

            return render_template("login.html", messages='Invalid username/password combination')
        return render_template("login.html")

    def logout(self):
        session.clear()
        return render_template("home.html")

    def signup(self):
        if request.method == 'POST':
            users = obj.dbconnect.users
            existing_user = users.find_one({'username': request.form['username']})

            if existing_user is None:
                hashpass = generate_password_hash(request.form['password'], method='sha256')
                users.insert_one({'username': request.form['username'], 'password': hashpass})
                session['username'] = request.form['username']
                return render_template("login.html")
            return render_template("signup.html", exist='That username already exists!')
        return render_template("signup.html", exist=None)

    def index(self):
        if 'username' in session:
            name = session['username']
            saved = obj.dbconnect.output.find()
            return render_template("index.html", output=saved, username=name)

        return render_template("home.html")

