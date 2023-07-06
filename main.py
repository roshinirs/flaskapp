from routes.route import app

from routes.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(port=8080, debug=True)
