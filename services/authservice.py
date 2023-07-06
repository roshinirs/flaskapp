from flask import request, redirect, url_for, session, render_template

from server.server import ServerSession


class AuthService(ServerSession):
    def __init__(self):
        super().__init__()

    def login(self):
        if request.method == 'POST':
            users = self.dbconnect.users
            login_user = users.find_one({'name': request.form['username']})

            if login_user:
                if request.form['password'] == login_user['password']:
                    session['username'] = request.form['username']
                    return redirect(url_for('auth.index'))

            return 'Invalid username/password combination'
        return render_template("login.html")

    def signup(self):
        if request.method == 'POST':
            users = self.dbconnect.users
            existing_user = users.find_one({'name': request.form['username']})

            if existing_user is None:
                hashpass = request.form['password']
                users.insert_one({'name': request.form['username'], 'password': hashpass})
                session['username'] = request.form['username']
                return render_template("login.html")
            return render_template("signup.html", exist='That username already exists!')
        return render_template("signup.html", exist=None)

    def index(self):
        if 'username' in session:
            name = session['username']
            saved = self.dbconnect.output.find()
            return render_template("index.html", output=saved, username=name)

        return render_template("home.html")
