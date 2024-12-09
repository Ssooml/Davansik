from flask import Flask

def create_app():
    app = Flask(__name__)

    # Регистрация блюпринтов
    from .routes import webapp_bp
    app.register_blueprint(webapp_bp)

    return app
